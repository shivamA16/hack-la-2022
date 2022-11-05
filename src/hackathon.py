#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 10:10:18 2022

@author: shivamaggarwal
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori


dataset = pd.read_csv('navigation.csv')
dataset["event_time"] = pd.to_datetime(dataset["event_time"]).dt.date
dataset = dataset.drop_duplicates(keep='first')
dataset = dataset.sort_values(['event_time', 'actor_id'])

dataset = dataset[ (dataset['actor_id'] != 'INSTRUCTOR')]
dataset = dataset[ (dataset['actor_id'] != 'UNKN_1')]
dataset = dataset[ (dataset['actor_id'] != 'UNKN_2')]
dataset = dataset[ (dataset['actor_id'] != 'UNKN_3')]
dataset = dataset[ (dataset['actor_id'] != 'UNKN_5')]
dataset = dataset[ (dataset['actor_id'] != 'UNKN_4')]
dataset = dataset[ (dataset['actor_id'] != 'UNKN_6')]
dataset = dataset[ (dataset['actor_id'] != 'UNKN_7')]
dataset = dataset[ (dataset['actor_id'] != 'UNKN_8')]
dataset = dataset[ (dataset['actor_id'] != 'UNKN_9')]
dataset = dataset[ (dataset['actor_id'] != 'UNKN_10')]
dataset = dataset[ (dataset['actor_id'] != 'UNKN_11')]
dataset = dataset[ (dataset['actor_id'] != 'UNKN_12')]
dataset = dataset[ (dataset['actor_id'] != 'UNKN_13')]


dataset = dataset.drop(['event__eventTime'], axis=1)


# learning_dataset = pd.DataFrame()


# # grouped = dataset


# for date in dataset['event_time'].unique():
#     sample = dataset[(dataset['event_time'] == date)]
#     learners = sample['actor_id'].unique()
    
#     files = []
    
#     for learner in learners:
#         sample_learner = sample[(sample['actor_id'] == learner)]
#         files = sample_learner['object_id']
#         learning_dataset = learning_dataset.append(files)


# grouped = dataset.groupby(['event_time','actor_id'])

# df  = pd.DataFrame()
# # print(grouped.apply(print))

# for object_id in grouped:
#     list = []
#     for i in (grouped['object_id']):
#         list.append(i)
#     df = df.append([list], ignore_index = True)

# print(df)


grouped = dataset.sort_values(['event_time', 'actor_id']).groupby(['event_time', 'actor_id'])['object_id'].apply(list)



learning_data = pd.DataFrame()

for i in range(0, grouped.shape[0]):
    files = set(grouped[i])
    learning_data = learning_data.append(pd.DataFrame([files]))
    
    
access = []
for i in range(0, len(learning_data)):
  access.append([str(learning_data.values[i,j]) for j in range(0, 132)])
  
  
rules = apriori(transactions = access, min_support = 0.003, min_confidence = 0.2, min_lift = 3, min_length = 2, max_length = 2)

results = list(rules)
#print(results)

## Putting the results well organised into a Pandas DataFrame
def inspect(results):
    lhs         = [tuple(result[2][0][0])[0] for result in results]
    rhs         = [tuple(result[2][0][1])[0] for result in results]
    supports    = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lifts       = [result[2][0][3] for result in results]
    return list(zip(lhs, rhs, supports, confidences, lifts))
resultsinDataFrame = pd.DataFrame(inspect(results), columns = ['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence', 'Lift'])

## Displaying the results non sorted
#resultsinDataFrame

## Displaying the results sorted by descending lifts
largest = resultsinDataFrame.nlargest(n = len(resultsinDataFrame), columns = 'Lift')


print("Enter file name: ")
filename = input()
print('\n')

# inputfile = "948d61de4855316ddbd9c9ac4eb635c0"
inputfile = dataset.loc[dataset['event__object_extensions_asset_name'] == filename, 'object_id'].iloc[0]




section = largest[(largest['Left Hand Side'] == inputfile)][0:3]['Right Hand Side']


name_dict = {}

for count, assign in enumerate(dataset['object_id'].unique()):
    column=  dataset['event__object_extensions_asset_name']
    
    
dataset.loc[dataset['object_id'] == inputfile, 'event__object_extensions_asset_name'].iloc[0]

for file in section:
    print(dataset.loc[dataset['object_id'] == file, 'event__object_extensions_asset_name'].iloc[0])




