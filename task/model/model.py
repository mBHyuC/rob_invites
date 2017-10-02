import pandas as pd
import numpy as np
from task.utils import *

# get module specific logger
import logging
log = logging.getLogger(__name__)

class abnb_base_model(object):
    def __init__(self, interface, location_uncertainty, is_derived=False):
        self.interface = interface
        self.max_dist = location_uncertainty
        self.required_functions = {'query_fun': 'get_data_from_features'}
        if not is_derived:
            self.c_init()

    def c_init(self, **kwargs):
        # first check that the interface comes with the needed functions
        is_error = False
        for k,req_fun in self.required_functions.iteritems():
            if not hasattr(self.interface, req_fun):
                is_error = True
                log.warning('Interface is missing mathod "%s"' % req_fun)
        if is_error:
            raise AttributeError('Interface error in class %s. See previous logs' % abnb_base_model.__name__)

        self.query_data = eval('self.interface.' + self.required_functions['query_fun'])
        self.query_additional_args = {}
        if kwargs:
            self.query_additional_args = kwargs

    def calculate_score(self, ldata):
        # scores based on the assumptions of this model
        #for this model see PreAssumtion 3
        ldata = ldata.drop_duplicates(subset='host_id')
        scores = [1./ldata.shape[0]]*ldata.shape[0]
        return ldata.assign(score=pd.Series(scores).values)

    def get_score_sparse_total(self,price, room_type, accommodates, bedrooms, bathrooms):
        '''
            Function calculate
            :param price: float
            :param room_type: string
            :param accommodates: int
            :param bedrooms: float
            :param bathrooms: float
            :param location: tulpe/array/list of l[0]:lat l[1]:lon

            this can be used to draw dense scores in google heatmaps
            -> no need for a "get_score_dense_total" function

            :return: pandas.Dataframe with colums (host_id, score, latitude, longitude)
        '''
        qdata = self.query_data(price=price, room_type=room_type, accommodates=accommodates,
                                                      bedrooms=bedrooms, bathrooms=bathrooms, **self.query_additional_args)
        qdata = self.calculate_score(qdata)
        return qdata[['host_id', 'score', 'latitude', 'longitude']]

    def get_score_sparse_location(self,price, room_type, accommodates, bedrooms, bathrooms, location):
        '''
            Function calculate
            :param price: float
            :param room_type: string
            :param accommodates: int
            :param bedrooms: float
            :param bathrooms: float
            :param location: tulpe/array/list of location[0]:lat location[1]:lon

            returns the score for exactly one and the first host host found, matching the "check_lat_lon" condition

            :return: float
        '''

        qdata = self.query_data(price=price, room_type=room_type, accommodates=accommodates,
                                                      bedrooms=bedrooms, bathrooms=bathrooms, **self.query_additional_args)
        qdata = self.calculate_score(qdata)
        #host_list = qdata['host_id'].values
        host_locations = qdata[['latitude', 'longitude']].values
        host_scores = qdata['score']
        is_host =  check_lat_lon(host_locations,np.array([location]),self.max_dist)
        for i,bval in enumerate(is_host): #return the first host found
            if bval:
                return host_scores.values[i]
        return 0.

    def get_score_dense_location(self,price, room_type, accommodates, bedrooms, bathrooms, location):
        '''
            Function calculate
            :param price: float
            :param room_type: string
            :param accommodates: int
            :param bedrooms: float
            :param bathrooms: float
            :param location: tulpe/array/list of location[0]:lat location[1]:lon

            also calculate dense scores

            :return: float
        '''

        qdata = self.query_data(price=price, room_type=room_type, accommodates=accommodates,
                                                      bedrooms=bedrooms, bathrooms=bathrooms, **self.query_additional_args)
        qdata = self.calculate_score(qdata)
        #host_list = qdata['host_id'].values
        host_locations = qdata[['latitude', 'longitude']].values
        host_scores = qdata['score']
        is_host =  check_lat_lon(host_locations,np.array([location]),self.max_dist)
        final_score = 0.
        for i,bval in enumerate(is_host): #return the first host found
            if bval:
                final_score += host_scores.values[i]
        return final_score


class abnb_personality_model(abnb_base_model):
    '''
        as an employee you know rob quite well
        deos he cares about the place he is staying itself
        does he want other people to find his place attractive
    '''
    def __init__(self, interface, location_uncertainty, influenced_by_others=True, is_derived=False):
        abnb_base_model.__init__(self,interface, location_uncertainty, is_derived=True)
        # overwrite required_functions
        self.influenced_by_others = influenced_by_others
        self.required_functions = {'query_fun': 'get_data_from_features'}
        if not is_derived:
            self.c_init()

    def calculate_score(self, ldata):
        ldata = super(abnb_personality_model, self).calculate_score(ldata)
        if  self.influenced_by_others:
            r_data = ldata[['score', 'review_scores_value']].values
            r_data = np.nan_to_num(r_data).astype(np.float64)
            scores = r_data[:,0]*np.exp(r_data[:,1]/2)
            # normalize scores
            scores = scores/np.sum(scores)

            # overwrite score with new values
            ldata =  ldata.assign(score=pd.Series(scores).values)
        return ldata



class abnb_flexible_price_model(abnb_base_model):
    '''
        price is now is now allowed to be in a certain range
        :param prob_to_wrong: porbability that the price has changed
                                  since Rob's invitation from the correct to a false price
        :param prob_to_right: porbability that the price has changed
                                  since Rob's invitation from wrong to the right price
        :param price_uncertainty: the percentage a price can vary since Rob's invitation


    '''
    def __init__(self, interface, location_uncertainty, price_uncertainty=0.1, prob_to_wrong=0.01, prob_to_right=0.08, is_derived=False):
        abnb_base_model.__init__(self,interface, location_uncertainty, is_derived=True)
        # overwrite required_functions
        self.price_uncertainty = price_uncertainty
        self.prob_to_wrong = prob_to_wrong
        self.prob_to_right = prob_to_right
        self.required_functions = {'query_fun': 'get_data_from_features_ucp'}
        if not is_derived:
            self.c_init(price_uncertainty=price_uncertainty)

    def calculate_score(self, ldata):
        # get_data_from_features_ucp, will add if column "price_difference" with the absulote difference between the wanted and the actual price
        # do not drop duplicates this time, add weighted probabilities of the same host
        # for the same host_id


        ldata = ldata.sort('host_id')
        p_diffs = ldata.price_difference.values
        host_ids = ldata.host_id.values

        t_scores = [1./ldata.shape[0]]*ldata.shape[0]
        for i,val in enumerate(t_scores):
            if p_diffs[i] < 0.00001: #price is the same
                t_scores[i] = val * (1-self.prob_to_right)
            else:
                t_scores[i] = val * (self.prob_to_wrong)

        # normalize sores
        t_scores = t_scores/np.sum(t_scores)

        # remove double host_id entries (for same host_id score is added up)
        scores = [t_scores[0]]
        for i in range(1,len(host_ids)):
            if host_ids[i-1] != host_ids[i]:
                scores.append(t_scores[i])
            else:
                scores[-1] += t_scores[i]

        # remove host id from data
        ldata = ldata.drop_duplicates(subset='host_id')

        # assign the calculated score values
        ldata = ldata.assign(score=pd.Series(scores).values)

        return ldata






