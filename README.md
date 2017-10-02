# Some standard python project
Preassumtions:
Description: Privacy: Rob is clever, he has knowledge of the historically Airbnb data.
Assumption: "..never shares his current address.." -> Queries that result in exactly one solution can be ignored (complexity reduction)
Description: Rob lives in Berlin.
Assumption: Rob lives in an Airbnb that is listed in the data used. The data used is correct (some location are far off).
Description: Rob changes locations, not rooms at the same location
Assumption: One host count as one possible location. The probability for Rob to stay at a certain host is independent of  the number of rooms offered. (hold only for the base model)
Description: Rob does not stay longer than a week.
Assumption: Weekly and monthly prices are not considered

General information:
The data used: data.insideairbnb.com/germany/be/berlin/2017-05-08/data/listings.csv.gz
Other data leaks the bathroom information
Each model has three types of methods.
get_score_dense_location:
Returns the score for a giving location, overlapping scores add up.
The area of the score is defined by a given radius r.
The score is the same along the radius r.
get_score_sparse_location:
Returns the score of the first match if there is one.
This is considered as the wanted function. As locations should not overlap. 
get_score_sparse_total:
Returns all possible location with porbability (for heatmap)
Model assumptions:
Base model:
Description: The given features are elements of the data.
Assumption: The score is calculated as one divided by the number of possible locations
Price uncertainty model  - derived from base model:
Description: From the point in time Rob invites his colleges to the point in time the colleges check for the possible location. The price could possible change.
Assumption: There is a fix percentage range in which the price can grow or fall. Furthermore there are two probabilities. One that specify the chance the price was correct and is now wrong and a second that specify the chance the price was wrong  and is now right.
Personality model - derived from base model:
Description: An evening dinner is quite personal. Rob only invites colleges he know a little better. The colleges know that he prefers Airbnb with good ratings. 
Assumption: The score is correlated with the Airbnb rating (it is not done, but could be a parameter that decides what rating Rob prefers)



