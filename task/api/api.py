from task.data_interface.interface import abnb_interface
from task.model.model import abnb_flexible_price_model,abnb_personality_model,abnb_base_model
import logging

def get_lat_lon_scores(price, room_type, accommodates, bedrooms, bathrooms,
              location_uncertainty=10, prob_to_wrong=0.01, prob_to_right=0.08):
    '''
    Example API function
    :param price: float
    :param room_type: string
    :param accommodates: int
    :param bedrooms: float
    :param bathrooms: float
    :param location_uncertainty: float/int
    :param prob_to_wrong: float
    :param prob_to_right: float
    :return: 'latitude', 'longitude', 'score' for all possible locations
              np.array(n,3) with n is number of locations
    '''
    logging.basicConfig() # logging might be set to a high output level for an api function

    # get an interface to the data of our choice
    i = abnb_interface('data/listings.csv')

    # pass the interface to the model
    m = abnb_flexible_price_model(i, location_uncertainty=location_uncertainty,
                                     prob_to_wrong=prob_to_wrong,
                                     prob_to_right=prob_to_right)

    sparse_score = m.get_score_sparse_total(price=price, room_type=room_type,
                                            accommodates=accommodates,
                                            bedrooms=bedrooms, bathrooms=bathrooms)

    return sparse_score[['latitude', 'longitude', 'score']].values
