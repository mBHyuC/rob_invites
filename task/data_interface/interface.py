import pandas as pd
import numpy as np

# get module specific logger
import logging
log = logging.getLogger(__name__)

def to_numpy_type(some_data):
    # el is already a numpy element
    if hasattr(some_data, 'dtype'):
        return some_data
    # if not try to convert it
    else:
        if type(some_data) == float:
            return np.float64(some_data)
        elif type(some_data) == long:
            return np.int64(some_data)
        elif type(some_data) == int:
            return np.int64(some_data)
        else:
            raise AttributeError("Unknown data type %s" % type(some_data))


class abnb_interface:
    def __init__(self, data_path):
        #input_file_name = data_path#'C:/Users/Friedrich/Desktop/listings.csv'
        self.acc_data = pd.read_csv(data_path)  # powerful pandas

        # check if the expected data is present and has the format
        # the user input and table format is:
        # on failure warn user and try custom conversion function (if given)
        # key - (type, conversion fkt)
        self.expected_type_dict = {
            'price': (np.float64, lambda x: np.float64(x[1:].replace(',',''))),
            'room_type': (object,),
            'accommodates': (np.int64,),
            'bedrooms': (np.float64,),
            'bathrooms': (np.float64,)
        }
        self.type_check()

        #give the room_type 'string' a fixed integer id
        self.room_dict = {}
        self.add_room_type_id()

        # do this in a logging module
        #print(self.acc_data.info())

    def add_room_type_id(self):
        '''
            Romm_type is given as string.
            This function adds a integer column to identify the room_type
            Associated data is stored in dict() self.room_dict

            return: None
        '''
        ctr = 0
        room_type_id_list = []
        for el in self.acc_data.room_type.values:
            if not el in self.room_dict:
                self.room_dict[el] = ctr
                ctr += 1
            room_type_id_list.append(self.room_dict[el])
        self.acc_data = self.acc_data.assign(room_type_id=pd.Series(room_type_id_list).values)

    def type_check(self, **kwargs):
        '''
            Function checks the data types of the table.
            If no argument is given
            Else checks the data of the given keyword arguments to match the expected data types
            ** relevant data types are defined in self.expected_type_dict

            :return: If checking the table contents: None
                    Else if checking arguments: Bool
        '''

        # if there are no given input to check, test the table itself
        if not kwargs:
            for k,v in self.expected_type_dict.iteritems():
                if not self.acc_data[k].dtype == v[0]:
                    # try for custom conversion functions
                    if v[1]:
                        log.warning('Type mismatch of column "%s" trying to convert type "%s" in "%s". In function %s' % (
                            k,self.acc_data[k].dtype, v[0], self.type_check.__name__))
                        try:
                            self.acc_data[k] = self.acc_data[k].map(v[1])
                        except:
                            raise ValueError('Type of column "%s" is "%s". Expected "%s"' % (k, self.acc_data[k].dtype, v[0]))
                    else:
                        raise ValueError('Type of column "%s" is "%s". Expected "%s"' % (k, self.acc_data[k].dtype, v[0]))

        # this part is for user input
        else:
            for k, v in self.expected_type_dict.iteritems():
                try:
                    if k == 'room_type': # dirty hack type for different type string <-> object
                        if not kwargs[k] in self.room_dict:
                            log.warning('Cannot find "%s" in self.room_dict. In function %s' % (
                                kwargs[k], self.type_check.__name__))
                            return False
                    elif not type(to_numpy_type(kwargs[k])) == v[0]:
                        log.warning('Type of column "%s" is "%s". Expected "%s". In function %s' % (k, type(to_numpy_type(kwargs[k])), v[0], self.type_check.__name__))
                        return False
                except:
                    log.warning('type_check failed. Unknown reason. In function %s' %
                        self.type_check.__name__)
                    return False
            return True #accept argumnts

    def get_data_from_features(self, price=None, room_type=None, accommodates=None, bedrooms=None, bathrooms=None, **kwargs):
        '''
            Function rus a query in the data, if input is of the correct data type

            return: If correct data type: Query result as pandas.Dataframe
                    Else: Empty pandas.Dataframe
        '''
        # runs a query if input types are correct - TODO: build up query generally to allow missing arguments
        if self.type_check(price=price, room_type=room_type, accommodates=accommodates, bedrooms=bedrooms, bathrooms=bathrooms):
            return self.acc_data.query('price==%f&room_type_id==%d&accommodates==%d&bedrooms==%f&bathrooms==%f' % (price, self.room_dict[room_type], accommodates, bedrooms, bathrooms))
        else:
            log.warning('type_check failed. No value is returned. In function %s' %
                        self.get_data_from_features.__name__)
            return pd.DataFrame()

    def get_data_from_features_ucp(self, price=None, room_type=None, accommodates=None, bedrooms=None, bathrooms=None, price_uncertainty=0.1,
                               **kwargs):
        '''
            Function rus a query in the data, if input is of the correct data type

            return: If correct data type: Query result as pandas.Dataframe
                    Else: Empty pandas.Dataframe
        '''
        # runs a query if input types are correct - TODO: build up query generally to allow missing arguments
        if self.type_check(price=price, room_type=room_type, accommodates=accommodates, bedrooms=bedrooms,
                           bathrooms=bathrooms):
            qdata =  self.acc_data.query('price>=%f&price<=%f&room_type_id==%d&accommodates==%d&bedrooms==%f&bathrooms==%f' % (
                price*(1-price_uncertainty), price*(1+price_uncertainty), self.room_dict[room_type], accommodates, bedrooms, bathrooms))
            price_difference = np.abs(qdata['price'].values-price)
            qdata = qdata.assign(price_difference=pd.Series(price_difference).values)
            return qdata
        else:
            log.warning('type_check failed. No value is returned. In function %s' %
                        self.get_data_from_features.__name__)
            return pd.DataFrame()






# price = 10.
# room_type = {}
# host_id = 10
# accommodates = 0
# bedrooms = 0
#
# count_dict = {}
#
# room_dict = {}
# ctr = 0
# new_int_list = []
# acc_data = m.acc_data
# for el in acc_data.room_type.values:
#     if not room_dict.has_key(el):
#         room_dict[el] = ctr
#         ctr+=1
#     new_int_list.append(room_dict[el])
#
# acc_data = acc_data.assign(room_type_id=pd.Series(new_int_list).values)
#
#
#
#
# prices = acc_data.price
# for p in prices.values:
#     if not count_dict.has_key(p):
#         count_dict[p] = acc_data.query('price==%f' % p)
#
# non_unique_list = []
#
# for k,v in count_dict.iteritems():
#     if v.shape[0]>1:
#         slist = v.host_id.values
#         slist.sort()
#         for i in range(len(slist)-1):
#             if slist[i] == slist[i+1]:
#                 non_unique_list.append((slist[i+1],k))
#
# #remove double elements
# non_unique_list = set(non_unique_list)
#
#
# non_unique_list2 = []
# for el in non_unique_list:
#     this_data = acc_data.query('price==%f&host_id==%d' % (el[1],el[0]))
#     slist = this_data.bedrooms.values
#     slist.sort()
#     for i in range(len(slist) - 1):
#         if slist[i] == slist[i + 1]:
#             non_unique_list2.append((el[0],el[1],slist[i + 1]))
#
# non_unique_list2 = set(non_unique_list2)
#
# non_unique_list3 = []
# for el in non_unique_list2:
#     this_data = acc_data.query('price==%f&host_id==%d&bedrooms==%f' % (el[1],el[0],el[2]))
#     slist = this_data.accommodates.values
#     slist.sort()
#     for i in range(len(slist) - 1):
#         if slist[i] == slist[i + 1]:
#             non_unique_list3.append((el[0],el[1],el[2],slist[i + 1]))
#
# non_unique_list3 = set(non_unique_list3)
#
# non_unique_list4 = []
# for el in non_unique_list3:
#     this_data = acc_data.query('price==%f&host_id==%d&bedrooms==%f&accommodates==%d' % (el[1],el[0],el[2],el[3]))
#     slist = this_data.room_type_id.values
#     slist.sort()
#     for i in range(len(slist) - 1):
#         if slist[i] == slist[i + 1]:
#             non_unique_list4.append((el[0],el[1],el[2],el[3],slist[i + 1]))
#
# non_unique_list4 = set(non_unique_list4)
#
# non_unique_list5 = []
# for el in non_unique_list4:
#     this_data = acc_data.query('price==%f&host_id==%d&bedrooms==%f&accommodates==%d&room_type_id==%d' % (el[1],el[0],el[2],el[3],el[4]))
#     slist = this_data.bathrooms.values
#     slist.sort()
#     for i in range(len(slist) - 1):
#         if slist[i] == slist[i + 1]:
#             non_unique_list5.append((el[0],el[1],el[2],el[3],el[4],slist[i + 1]))
#
# non_unique_list5 = set(non_unique_list5)
#
#
#
#
# for el in list(non_unique_list5):
#     print(el)








