# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 11:22:14 2022

@author: nithin
"""
#Importing the necessary
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import pickle

#Reading the csv file using pandas
df = pd.read_csv(r"C:\Users\nithi\OneDrive\Documents\Sentiment Analysis NLP\balanced_reviews25.csv")
df.shape
df.columns.tolist()
print('Reading the File')

#Removing the Nan Values
df.isnull().any(axis = 0)
df.dropna(inplace = True)
df.shape
print("Droping the Nan Values")

#Droping the neutral values
df['overall'] !=3
df = df[df['overall']!=3]
df.shape
df['overall'].value_counts()
print('Dropped neural reviews')

#Creating a column for positivity or as label
df['Positivity'] = np.where(df['overall'] > 3,1,0)
df['Positivity'].value_counts()
print('Created Labels')

print('Features and Labels Declared')

features = df['reviewText']
labels = df['Positivity']


print('Splitting the test and train data')
features_train , features_test , labels_train , labels_test = train_test_split(features , labels , train_size = 0.2 ,test_size = 0.2)

#Vectorization
vect = TfidfVectorizer(min_df = 5).fit(features_train)
len(vect.get_feature_names())
features_train_vectorized = vect.transform(features_train)
print('Vectorizzation Complete')





