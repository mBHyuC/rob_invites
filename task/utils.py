import numpy as np

def great_cycle_distance_rad(lat1, lon1 ,lat2, lon2):
    '''
        calculates the great_cycle_distance in rad

        :params: lat1 float/np.array of floats
        :params: lon1 float/np.array of floats
        :params: lat2 float/np.array of floats
        :params: lon2 float/np.array of floats

        !requirement: size(lat1) == size(lon1) == size(lat1) == size(lon2)
                      or lat1 == lon1 == single float or lat2 == lon2 == single float

        source: https://en.wikipedia.org/wiki/Great-circle_distance
        # r is approximated with 6371000m
    '''
    return np.arccos(np.sin(lat1) * np.sin(lat2) + np.cos(lat1) * np.cos(lat2) * np.cos(lon1 - lon2)) * 6371000

def great_cycle_distance_deg(lat1, lon1 ,lat2, lon2):
    '''
        great_cycle_distance in deg
        :params: see: great_cycle_distance_rad
    '''
    return great_cycle_distance_rad(np.deg2rad(lat1), np.deg2rad(lon1), np.deg2rad(lat2), np.deg2rad(lon2))

def check_lat_lon(l1,l2,max_dist):
    '''
        Function checks if two coordinates lie within a certain range
        :param l1: np.array[[lat1, lon1], [lat2, lon2], ..]
        :param l2: np.array[[lat1, lon1], [lat2, lon2], ..]
        :param max_dist: distance in metern, int/float

        !requirement: size(l1) == size(l2) or l1.shape[0] == 1 or l2.shape[0] == 1

        :return: True if max_d >= distance(l1,l2) else False
    '''
    return great_cycle_distance_deg(l1[:,0],l1[:,1],l2[:,0],l2[:,1]) <= max_dist

def get_lat_lon(data):
    '''
        Return lat and lon as numpy.array from pandas.Dataframe
        :param data: information with column latitude and longitude
        :return: numpy array with shape [data.shape[0],2] (axis 1 is for lat,lon
    '''
    return np.vstack((np.array(data['latitude']),np.array(data['longitude']))).transpose()
