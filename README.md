# House_Rocket_Insight_Project

<i>Se quiser ler sobre esse projeto em português, [clique aqui](https://github.com/felipefvasconcelos/House_Rocket_Insight_Project/blob/main/README_POR_BR.md).</i>

In this repository I use Python basics to provide business insights on house market in King County (USA), based on public data. <br>
All information below is fictional.

## 1. Business Problem

House Rocket's business model is basically buy-and-sell properties by using technology to maximize its revenue. The biggest challenge is to find the best business oportunities available in the real state market based on several attributes of each property.

Therefore, the main questions this project aim to answer is:
   * Which properties should House Rocket buy?
   * For how much should they be sold?
   * When should it be sold?
   * What is the expected profit?<br><br>

## 2. Business Assumptions
* When a property is bought and sold more than once within the data timeline (2014-2015), it results in duplicated information. Only the most recent information will be kept.
* Inconsistencies between properties attributes are considered as input errors. Lines with such inconsistencies were removed.
* Properties recommended to buy must have 'condition' greater or equal to 3, and price below the median price of the properties on its region.
* Properties price are affected by seasonality according to the seasons of the year only.
* The recommended selling price for each property will be:
  * The buying price plus 30%, if the buying price is lower than the median price of properties in the region at specific season;
  * The buying price plus 10%, if the buying price is greater than the median price of properties in the region at specific season;
* Seasons of the year:
   * Spring starts on March, end on May
   * Summer starts on June, end on Auguts
   * Fall starts on September, end on November
   * Winter starts on December, end on February


## 3. Data

The data used in this project can be found at:<br>
https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885
<br><br>
The table below list each property attribute and respective definition in the data:<br>

<details><summary>Click here to see the attibutes table</summary><br>
  
Attribute | Definition
------------ | -------------
|id | Unique ID for each property available|
|date | Date that the property was available|
|price | Sale price of each property |
|bedrooms | Number of bedrooms|
|bathrooms | Number of bathrooms, where .5 accounts for a room with a toilet but no shower, and .75 or ¾ bath is a bathroom that contains one sink, one toilet and either a shower or a bath.|
|sqft_living | Square footage of the apartments interior living space|
|sqft_lot | Square footage of the land space|
|floors | Number of floors|
|waterfront | A dummy variable for whether the apartment was overlooking the waterfront or not|
|view | An index from 0 to 4 of how good the view of the property was|
|condition | An index from 1 to 5 on the condition of the apartment|
|grade | An index from 1 to 13, where 1-3 falls short of building construction and design, 7 has an average level of construction and design, and 11-13 have a high quality level of construction and design.|
|sqft_above | The square footage of the interior housing space that is above ground level|
|sqft_basement | The square footage of the interior housing space that is below ground level|
|yr_built | The year the property was initially built|
|yr_renovated | The year of the property’s last renovation|
|zipcode | What zipcode area the property is in|
|lat | Lattitude|
|long | Longitude|
|sqft_living15 | The square footage of interior housing living space for the nearest 15 neighbors|
|sqft_lot15 | The square footage of the land lots of the nearest 15 neighbors|
</details>


## 4. Solution Strategy
1. Understanding business model and busines problem;
2. Collecting data from Kaggle;
3. Process Data;
4. Clean Data;
5. Explore data;
6. Answer business questions (section 1);
7. Deploy [dashboard](https://house-rocket-insights-db.herokuapp.com/);
8. Validate hypotesis;
9. Provide relevant insights.
<br>

## 5. Tools
* Python 3.10.2
* Jupyter Notebook
* Pycharm

## 6. Business Results
Based on the previously established criteria, there are 10,500 properties that should be bought from the total of 21,421.<br>
If the selling recommendations are followed, expected results are:
* Maximun Value Invested: $ 4,078,617,894.0
* Minimum Expected Profit: $ 694,433,672.2
* Maximum Expeted Profit: $ 839,540,926.8
<br><br>
Information of which property should be bought and when to sell it can be found on the online [dashboard](https://house-rocket-insights-db.herokuapp.com/).

## 7. Most Relevant Data Insights
1. Properties with condition equal to 4 are the most profitable, followed by properties with condition equal to 3, and 5.
2. Most properties (58%) became available for sale during summer and spring.
3. 50% of the houses recommended to buy are within a 15km from the lake


## 8. Conclusion
The objective of this project was to apply Python basic concepts to solve a hypotetical business problem of an fictional company (House Rocket). After following the steps listed in the solution strategy, and considering the business assumptions that were made, it was possible to classify each property in "buy" or "no buy" recommendation. Also, for those properties recommended to be bought, it was suggested a selling price and the best season to sell it. Finally, it was built an online dashboard to visualize all recommendations made along this project.
<br><br>

---
## References:
* Dataset House Sales in King County (USA) from [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction)
* Variables meaning on [Kaggle discussion](https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885)
* Python from Zero to DS lessons on [Youtube](https://www.youtube.com/watch?v=1xXK_z9M6yk&list=PLZlkyCIi8bMprZgBsFopRQMG_Kj1IA1WG&ab_channel=SejaUmDataScientist)
* Blog [Seja um Data Scientist](https://sejaumdatascientist.com/os-5-projetos-de-data-science-que-fara-o-recrutador-olhar-para-voce/)
