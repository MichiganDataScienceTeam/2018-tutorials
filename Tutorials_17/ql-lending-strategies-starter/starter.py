# MDST / QL Lending Strategies Prediction Challenge Starter code
#
# Description:
#
# Loads data and trains several simple classifiers. Generates
# submission files in the correct Kaggle format.
#
# Usage:
#
# python starter.py
# Make sure that your data is saved in ./data . This code will need
# to be modified if you use a different location.
#
# Authors:
#
# Arya Farahi, Jonathan Stroud

import os, sys
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from sklearn.cross_validation import train_test_split
from sklearn.metrics import auc, roc_curve, roc_auc_score

##### Load data tables

# Change if you use a different data location.
path = "./data/"
dtypes = {'id': str, 'zip': str}
          

train = pd.read_csv(os.path.join(path,'loan_table_train.csv'), dtype=dtypes).set_index('id')
test = pd.read_csv(os.path.join(path,'loan_table_test.csv'), dtype=dtypes).set_index('id')

##### Drop some columns

# We won't use these for now, but they might be useful later.
todrop = ['zip', 'state']

train.drop(todrop, axis=1, inplace=True)
test.drop(todrop, axis=1, inplace=True)

##### Convert date strings to numerical values

for column_name in ['datekey', 'largest_open_mortgage_open_date']:
    ###########################################
    if column_name == 'datekey':
        day_time = pd.to_datetime(test[column_name], format='%Y%m%d')
    else:
        day_time = pd.to_datetime(test[column_name], infer_datetime_format=True, yearfirst=True)
    test.drop(column_name, axis=1, inplace=True)
    test[column_name+'_month'] = np.array(day_time.dt.month)
    test[column_name+'_year'] = np.array(day_time.dt.year)
    test[column_name+'_day'] = np.array(day_time.dt.day)
    test[column_name+'_dayofweek'] = np.array(day_time.dt.dayofweek)
    ###########################################
    if column_name == 'datekey':
        day_time = pd.to_datetime(train[column_name], format='%Y%m%d')
    else:
        day_time = pd.to_datetime(train[column_name], infer_datetime_format=True, yearfirst=True)
    train.drop(column_name, axis=1, inplace=True)
    train[column_name+'_month'] = np.array(day_time.dt.month)
    train[column_name+'_year'] = np.array(day_time.dt.year)
    train[column_name+'_day'] = np.array(day_time.dt.day)
    train[column_name+'_dayofweek'] = np.array(day_time.dt.dayofweek)


##### Convert categorical variables to dummy variables

cols = test.select_dtypes(exclude=['float', 'int']).columns
train = pd.get_dummies(train, columns=cols)
test = pd.get_dummies(test, columns=cols)

##### Impute Missing Values

# For now, we just fill in a default value. Better solutions will
# improve performance.

train.fillna(value=-10.0, inplace=True)
test.fillna(value=-10.0, inplace=True)

# select features and the response 
features = list( test.columns )
response = ['result']

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble     import RandomForestClassifier

classifiers = {
    "LR": LogisticRegression(),#solver='sag', tol=1e-1, C=1.e4 / train[features].shape[0]),
    "RF": RandomForestClassifier(max_depth=25),
}

X = train[features]
Y = np.array(train[response]).ravel()
mask = Y > -1
Y[mask] = 1.0
Y[~mask] = 0.0


##### Fit the model

if not os.path.exists('./submission/'):
    os.makedirs('./submission/')

for classifier_label in classifiers.keys():
    clf = classifiers[classifier_label]

    clf.fit(X, Y)

    y_pred = np.array(clf.predict_proba(test[features])[:, 1])

    df = {"id":test.index.values, "target":y_pred}
    df = pd.DataFrame(df, columns=["id", "target"])

    df.to_csv("./submission/Submission_%s.csv"%classifier_label, index=False)
