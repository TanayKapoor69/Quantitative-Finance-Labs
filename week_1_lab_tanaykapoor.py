# -*- coding: utf-8 -*-
"""Week 1 Lab_TanayKapoor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JfLq6TDGnzDavUM7MPMA570dYoIgPWRD

# Week 1 Lab - due by 11:59pm CDT on July 9th

## Objective: to perform Exploratory Data Analysis (EDA) on a multiple-asset portfolio

### Setup and Loading Packages
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import yfinance as yf
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import scipy.stats as stats
from datetime import datetime, timedelta
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
from matplotlib.ticker import FuncFormatter

"""Months following the COVID-19 pandemic recovery, the stock market seems to slow down on its ralley and the cryptocurrency market continues to show volatility. As a quantitative analyst and an investor, you want to understand the empirical behaviors of the assets before building a predictive model and investing in them, since you believe that this can give you a statistical edge in your portfolio. You have several assets in mind and would like to conduct an initial analysis on their historical performances to see if they are a good makeup for your portfolio.<br><br>
Please complete the following problems to perform full EDA on your stock selection.

## Problem 1: Preliminary Visualization

a) Select 3-5 assets of your prefernce, then specify their ticker(s), start and end dates of their price data you want to explore.<br><br>
Notice that any assets can be selected, and not just stocks. For example, cryptocurrency and foreign exchange instruments can be suggested as well. Some relatively new cryptocurrencies (e.g., Solana, USD Coin) only have complete data dating back to three or four years ago, so setting the duration of data further back than these dates may result in inaccurate representation of their relationships.
"""

################ EDIT CODE LINES HERE #################

symbolList =  ['IVV', 'EEM', 'SHY', 'VNQ', 'GLD'] # asset ticker symbols
START_DATE = '2018-07-07' # asset data start date
END_DATE = '2023-07-07' # asset data end date
#####################################################

"""Run the following code chunk to extract the adjusted close prices and compute log returns of your chosen assets from Yahoo Finance.<br>
<p style="color:red;">PLEASE DO NOT CHANGE THIS CODE !!!</p>
"""

stockPxList = yf.download(symbolList, START_DATE, END_DATE)['Adj Close'] # retreiving asset price data from yahoo finance
# converting prices to log returns and removing NaN values
stockLogRetList = np.log(stockPxList).diff().dropna()

"""b) Please write a code piece to perform 2 visualizaitons on each assets' log returns you extracted from a). <br><br>
Since there are 3-5 assets, you wiil need 6-10 plots to evaluate each asset.

Visualization #1:
"""

################ EDIT CODE LINES HERE #################



# Plotting the log returns separately for each stock
for symbol in symbolList:
    plt.figure(figsize=(12, 8)) # Set the figure size
    plt.plot(stockLogRetList[symbol]) # Plotting the log returns for the current stock
    plt.title(f'Log Returns of {symbol}')
    plt.xlabel('Date')
    plt.ylabel('Log Return')
    plt.show()
#####################################################

"""Visualization #2:"""

################ EDIT CODE LINES HERE #################



# Plotting the boxplots separately for each stock
for symbol in symbolList:
    plt.figure(figsize=(8, 6)) # Set the figure size
    plt.boxplot(stockLogRetList[symbol], vert=False) # Plotting the boxplot for the current stock
    plt.title(f"Boxplot of {symbol}'s Stock Log Return")
    plt.xlabel("Log Return")
    plt.show()


#####################################################

"""Visualization #3:"""

# visualizing correlation heatmap
fig, ax = plt.subplots(figsize=(15,10))
sns.heatmap(stockLogRetList.corr(),annot=True)
plt.title("Correlations Between Stock Log Returns")

"""c) Interpret the visualizations that you performed above. What can you say about them?

[Write your answer here]

I visualized my 5 stocks using a Log Return plot, box plot, and a correlation heatmap. A quick description of my 5 stocks:

IVV: iShares Core S&P 500 ETF. This fund tracks the performance of the S&P 500 index fund.

EEM: iShares MSCI Emerging Markets ETF. This fund tracks the performance of companies from a global market.

SHY: iShares 1-3 Year Treasury Bond ETF. This fund tracks the performance of U.S. Treasury 1-3 Bond Index.

VNQ: Vanguard Real Estate Index Fund ETF. This fund tracks the performance of the MSCI US Investable Market Real Estate 25/50 Index.

GLD: SPDR Gold Trust. This fund tracks the performance of the gold bullion.

Analyzing the Log Return Graphs:
The Log Return graph for IVV shows pretty constant log returns between 0.05 and -0.05. In early 2020, around when the COVID-19 pandemic started, this fund had unusual log returns of 0.10 and -0.10. However, the log returns have remained relatively constant since. I can tell that there will be some outlier data already.

The Log Return graph for EEM shows a similar trend. Toward the start of the pandemic, log returns increased in magnitude to about 0.10 and -0.10. Since then, the log returns have stayed pretty constant. Again, I see outliers, but I also sense a high correlation between IVV and EEM. This hypothesis makes sense.

The Log Return graph for SHY was relatively constant, and has very low returns. The outlier high return was around 0.010, while the low was around -0.004. The log returns have been pretty constant around 0.002 and -0.002, but just in the past year they were more consistent around 0.004 and -0.004. As a fund for bonds, it makes sense that the log returns should not vary much, and that the stock should not be too volatile.

The Log Return graph for VNQ showed fairly constant returns around 0.05 and -0.05. However, during the start of the pandemic, there was a huge -0.20 log return, most likely because of the effect the pandemic had on the real estate market

The Log Return graph for GLD was very volatile, and there is no real range it sat at consistently.

Analyzing the Box Plots:
All graphs had a median at 0. An interesting pattern was the width of the box. SHY and VNQ had boxes with the least width and were the most narrow, indicating the 25th and 75th percentile log returns were closer together, meaning the stocks are not as volatile. GLD, on the other hand, had a very wide box, indicating high volatility. IVV and EEM both had similar sized boxes, indicating similar volatility, which makes sense as both are index funds. All the box plots had outliers, so now I know I will have to take out these outliers during pre-processing,

Analyzing the Correlation Heatmap:
In my opinion, the most interesting chart, this heatmap revealed a few patterns. IVV had high correlations of around 0.8 to VNQ and EEM. This means a combination of IVV with any of the other two stocks could be risky due to the high positive correlation. SHY and GLD did not show much correlation to any of the stocks.

## Problem 2: Preliminary Normality Testing

You realized that within the date range you specified, there may be some days when the assets make big directional swings, hence skewing the data or thickening the probabilities of extreme values. To keep your minds in peace, you decided to perform normality testing to understand how your assets' distribution compare to what's considered 'normal'.<br><br>
(e.g., If your date range spans the COVID-19 pandemic, you may see more extreme tail values or outliers in your log returns, which deviates from a normal distribution because the market fluctuates a lot during this time.)<br><br>
a) Please write a code piece to perform 1 normality test on the assets' returns you extracted from problem 1.
"""

################ EDIT CODE LINES HERE #################

from scipy import stats

# Perform Shapiro-Wilk normality test for each stock's log returns
shapiro_pvalues = {}
for symbol in symbolList:
    shapiro_test = stats.shapiro(stockLogRetList[symbol])
    shapiro_pvalues[symbol] = shapiro_test.pvalue

# Print the p-values
for symbol, pvalue in shapiro_pvalues.items():
    print(f"Shapiro-Wilk p-value for {symbol}: {pvalue}")


#####################################################

"""b) Interpret the result you obtained from the normality test you chose in part a). What can you say about it?

[Write your answer here]

For the time period I selected over the last 5 years, all of the stocks had a p value < 0.05. This means we must reject the null hypothesis and that the log returns of these stocks do not follow normal distribution.

## Problem 3: Preliminary Pre-processing

Imbalanced labels is a classification predictive modeling problem where the distribution of examples across the classes is not equal. For example, we may collect measurements of cats and have 80 samples of one cat species and 20 samples of a second cat species. This represents an example of an imbalanced classification problem. A 50-50 or a near-50-50 sample species would form a balanced classification problem.<br/>

As a quantitative analyst, you are curious as to how the list of assets you chose above helps predict the direction of another asset. But before diving into the modeling portion, you want to investigate any label imbalance problems. <br>

Please read this blog before jumping into this question: https://machinelearningmastery.com/what-is-imbalanced-classification/

a) Specify the ticker of an asset whose direction you are interested in predicting. This stock shall be different than the ones you chose in problem 1.
"""

TICKER = 'ZS' # asset ticker symbol

"""Run the following code chunk. This will binarize the returns for the asset that you're trying to predict over the period specified above. In other words, the asset's price will be transformed into 0's and 1's - 0 if price did not go up, 1 if price went up. A bar plot is produced to show the label distribution. For instance, there should be one bar showing how many days the stock goes up and another showing how many days the stock goes down.<br/>

<p style="color:red;">PLEASE DO NOT CHANGE THIS CODE CHUNK!!!</p>
"""

FEATURES = symbolList.copy()
stockPx = yf.download(TICKER, START_DATE, END_DATE)['Adj Close'] # storing adjusted stock prices into a variable
stockPx01 = (stockPx.pct_change().dropna() > 0).astype(int)
# visualize directional label distribution
ax = sns.countplot(x = stockPx01)
plt.title('Directional (Up=1/Down=0) Distribution')
plt.xlabel(TICKER + ' Direction')
plt.ylabel('Count')
total = len(stockPx01)
for p in ax.patches:
        percentage = '{:.2f}%'.format(100 * p.get_height()/total)
        x_coord = p.get_x()
        y_coord = p.get_y() + p.get_height()+0.02
        ax.annotate(percentage, (x_coord, y_coord))

"""b) Are the lables balanced or imbalanced? Why?<br/>

[Write your answer here]

Yes, for ZS the directional distribution over the last 5 years is balanced. The percentages are balanced.

c) How do you think they can affect our prediction?

[Write your answer here]
If these percentages were imbalanced, the predictions we would make would not be accurate. The prediction would be biased to the majority class.

d) Please suggest one way to handle imbalanced data?

[Write your answer here]

One technique I would use to handle imbalanced data is oversampling. I would randomly replicate cases from the minority class to increase the representation in my dataset.

e) What are the features in this problem?

[Write your answer here]

The features in this problem are the log returns of the 5 stocks I picked earlier: IVV, EEM, SHY, VNQ, GLD. We want to know if the log returns of these stocks have any correlation or impact on the log returns of my respone variable, ZS.

f) Please write a code piece to split the data into 80% training set and 20% testing set.
"""

################ EDIT CODE LINES HERE #################

# Concatenating stockPxList and stockPx01 into a single DataFrame
combined_df = pd.concat([stockPx01, stockLogRetList], axis=1)



# Rename the first column to 'ZS'
combined_df = combined_df.rename(columns={'Adj Close': 'ZS'})
print(combined_df)


#####################################################

# Function to remove outlying values that lie > 3 standard deviations away from the mean
def remove_outliers(df, columns, n_std):
    for col in columns:
        print('Working on column: {}'.format(col))

        mean = df[col].mean() # mean
        sd = df[col].std() # standard deviation

        df = df[(df[col] <= mean+(n_std*sd))] # criteria

    return df

df_no_outliers = remove_outliers(combined_df, FEATURES, 3)

RESPONSE = 'ZS' # Replace 'ZS' with the actual column name representing the response variable
X_train, X_test, y_train, y_test = train_test_split(df_no_outliers.loc[:, FEATURES], df_no_outliers.loc[:, RESPONSE], test_size=0.2, random_state=0)

# Print the shapes of the training and testing sets
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)
print(y_train)
print(X_train)

from sklearn.ensemble import RandomForestClassifier # importing the random forest module

rf_model = RandomForestClassifier(random_state=0) # define the random forest model

rf_model.fit(X_train, y_train) # fit the random forest model

importances = rf_model.feature_importances_ # get importance

indices = np.argsort(importances) # sort the features' index by their importance scores

print(importances)

"""g) Please write a code piece to visualize the feature importance ranking of with a bar plot. How are the features ranked by their importance scores?<br><br>
(Hint: you would need to split the data first in part f) before computing the importance scores here)
"""

################ EDIT CODE LINES HERE #################

plt.title('Feature Importances in the Random Forest Model')
plt.barh(range(len(indices)), importances[indices], align='center')
plt.yticks(range(len(indices)), [FEATURES[i] for i in indices])
plt.xlabel('Importance Score')

#####################################################

"""[Write your answer here]

IVV is the most important feature. This means the log returns of IVV strongly correlate to those of ZS. This makes sense as ZS is a tech stock, and IVV is tracking the S&P 500 index comprised of tech stocks. SHY and GLD are the least important features, meaning their log returns have low correlation to the log returns of ZS. This makes sense as a tech stock should not be related to gold or bonds. These two features could probably be dropped to improve the accuracy of my prediction model
"""