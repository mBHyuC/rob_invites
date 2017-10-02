import pandas as pd
import numpy as np
from task.data_interface.interface import abnb_interface
from task.model.model import abnb_flexible_price_model,abnb_personality_model,abnb_base_model
import logging

if __name__ == "__main__":
    logging.basicConfig()

    # get an interface to the data of our choice
    i = abnb_interface('data/listings.csv')

    # pass the interface to the model class of out choice
    ## models: abnb_flexible_price_model or abnb_personality_model or abnb_base_model
    # NOTE: if the score is always zero one might choose a higher value for the "location_uncertainty"
    # This parameter specifies the r in meter where a location matches
    m = abnb_flexible_price_model(i, location_uncertainty=10)


    # load test data with columns ['price'], ['room_type'], ['accommodates'], ['bedrooms'], ['bathrooms']
    test_data = pd.read_csv('data/test_params.csv')

    for index, row in test_data.iterrows():
        pass


        ## EXAMPLE 1 - Returns the sparse score
        ## location=(52.457551, 13.371678) for a match in the first row
        # sparse_score = m.get_score_sparse_location(price=row['price'], room_type=row['room_type'],
        #                                         accommodates=row['accommodates'],
        #                                         bedrooms=row['bedrooms'], bathrooms=row['bathrooms'],location=(53,13))
        # print(sparse_score['score'].values)
        # print(sparse_score['host_id'].values)
        ## EXAMPLE 1 - END



        ## EXAMPLE 2 - Returns the dense score
        ## if increasing the "location_uncertainty" to see the dense value change (5km to 20km)
        # sparse_score = m.get_score_dense_location(price=row['price'], room_type=row['room_type'],
        #                                         accommodates=row['accommodates'],
        #                                         bedrooms=row['bedrooms'], bathrooms=row['bathrooms'],location=(52.506938,13.393644))
        # print(sparse_score['score'].values)
        # print(sparse_score['host_id'].values)
        ## EXAMPLE 2 - END



        ## EXAMPLE 3 - Heatmap (I know this is a shit method, but after 5 hours of finding a suitable method for python/js interaction, I gave up)
        # outputs the data to copy into the google example heatmap file
        #
        # sparse_score = m.get_score_sparse_total(price=row['price'], room_type=row['room_type'],
        #                                         accommodates=row['accommodates'],
        #                                         bedrooms=row['bedrooms'], bathrooms=row['bathrooms'])
        #
        # mean_lat = []
        # mean_lon = []
        # for a,b,c in (sparse_score[['latitude', 'longitude','score']].values):
        #     mean_lat.append(a)
        #     mean_lon.append(b)
        #     print "          {location: new google.maps.LatLng(%f, %f), weight: %f}," % (a,b,c*1000)
        # print("Data center is at (%f, %f)" % (np.mean(mean_lat), np.mean(mean_lon)))
        # break
        ## EXAMPLE 3 - END

