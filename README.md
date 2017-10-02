# Rob Invites
## Install information:
Project created and tested with python 2.7.10

### Step 1:
Download the data from [here](https://data.insideairbnb.com/germany/be/berlin/2017-05-08/data/listings.csv.gz).

### Step 2:
One may want to create a virtuel env first.
Run ``` setup.py install ```

## General information:
Each model has three types of methods:

```get_score_dense_location(...)```
Return: the score for a giving location, overlapping scores add up
The area of the score is defined by a given radius r.
The score is the same along the radius r.

```get_score_sparse_location(...)```
Return: the score of the first match if there is one, else 0.0
This is considered as the wanted function. As locations should not overlap.

```get_score_sparse_total(...)```
Return: all possible locations with corresponding score (for heatmap)

*test_params.csv* contains a list of host_id with feature sets leading to more than one possible location

*example.py* contains an example how to use the classes/models


## Preassumtions:
### I
Description: Privacy: Rob is clever, he has knowledge of the historically Airbnb data.
Assumption: "..never shares his current address.." -> Queries that result in exactly one solution can be ignored (complexity reduction)

### II
Description: Rob lives in Berlin.
Assumption: Rob lives in an Airbnb that is listed in the data used. The data used is correct (some location are far off).

### III
Description: Rob changes locations, not rooms at the same location
Assumption: One host count as one possible location. The probability for Rob to stay at a certain host is independent of  the number of rooms offered. (hold only for the base model)

### IV
Description: Rob does not stay longer than a week.
Assumption: Weekly and monthly prices are not considered

## Model assumptions:
### Base model:
Description: The given features are elements of the data.
Assumption: The score is calculated as one divided by the number of possible locations

### Price uncertainty model  - derived from base model:
Description: From the point in time Rob invites his colleges to the point in time the colleges check for the possible location. The price could possible change.
Assumption: There is a fix percentage range in which the price can grow or fall. Furthermore there are two probabilities. One that specify the chance the price was correct and is now wrong and a second that specify the chance the price was wrong  and is now right.

### Personality model - derived from base model:
Description: An evening dinner is quite personal. Rob only invites colleges he know a little better. The colleges know that he prefers Airbnb with good ratings. 
Assumption: The score is correlated with the Airbnb rating (it is not done, but could be a parameter that decides what rating Rob prefers)




