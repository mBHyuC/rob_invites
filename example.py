import pandas as pd
import numpy as np
from task.data_interface.interface import abnb_interface
from task.model.model import abnb_flexible_price_model,abnb_personality_model,abnb_base_model
import logging

if __name__ == "__main__":
    logging.basicConfig()

    i = abnb_interface('data/listings.csv') # get an interface to the data of our choice
    m = abnb_flexible_price_model(i, location_uncertainty=10) # pass the interface to the model class (it will internally check for compatibility)

    test_data = pd.read_csv('data/test_params.csv') # testfile - containing all host data with
    #['price'],['room_type'], ['accommodates'],['bedrooms'],['bathrooms'], that do not result in a single solution

    for index, row in test_data.iterrows():
        #data = i.get_data_from_features(price=row['price'], room_type=row['room_type'], accommodates=row['accommodates'], bedrooms=row['bedrooms'], bathrooms=row['bathrooms'])
        sparse_score = m.get_score_sparse_total(price=row['price'], room_type=row['room_type'], accommodates=row['accommodates'],
                          bedrooms=row['bedrooms'], bathrooms=row['bathrooms'])

        meana = []
        meanb = []
        for a,b,c in (sparse_score[['latitude', 'longitude','score']].values):
            meana.append(a)
            meanb.append(b)


            print "          {location: new google.maps.LatLng(%.12f, %.12f), weight: %f}," % (a,b,c*1000)


        print(np.mean(meana), np.mean(meanb))

        break


        #,location=(53,13)
        #abnb_personality_model
        #abnb_flexible_price_model

        # print(sparse_score['score'].values)
        # print(sparse_score['host_id'].values)

        print(sparse_score)