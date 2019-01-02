#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 23:01:13 2018

@author: rbhole
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()

#http://archive.ics.uci.edu/ml/machine-learning-databases/00352/
data=pd.read_csv("Online Retail.csv",encoding='utf-8')

data.head(10)

data['Total_Price']=data['Quantity']*data['UnitPrice']
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
data['date'] = data.InvoiceDate.dt.strftime('%Y-%m-%d')

#data['date']=data['InvoiceDate'].str.extract('(.*)/').str.extract('(.*)/')
#data['date']=data.date.astype(str).str.zfill(2)
#data['date']=data['InvoiceDate'].str.extract('/(.*)').str.extract('/(.*)') + data['date']
#data.date = pd.to_numeric(data.date, errors='coerce')



Cust_country=data[['Country','CustomerID']].drop_duplicates()
#Calculating the distinct count of customer for each country
Cust_country_count=Cust_country.groupby(['Country'])['CustomerID'].\
aggregate('count').reset_index().sort_values('CustomerID', ascending=False)
#Plotting the count of customers
country=list(Cust_country_count['Country'])
Cust_id=list(Cust_country_count['CustomerID'])
plt.figure(figsize=(12,8))
sns.barplot(country, Cust_id, alpha=0.8, color=color[2])
plt.xticks(rotation='60')
plt.show()

Cust_date_UK=data[data['Country']=='United Kingdom']
Cust_date_UK=Cust_date_UK[['CustomerID','date']].drop_duplicates()

def recency(row):
   if row['date'] > '2011-10-09':
    val = 5
   elif row['date'] <= '2011-10-09' and row['date'] > '2011-08-09':
    val = 4
   elif row['date'] <= '2011-08-09' and row['date'] > '2011-06-09':
    val = 3
   elif row['date'] <= '2011-06-09' and row['date'] > '2011-04-09':
    val = 2
   else:
    val = 1
   return val

Cust_date_UK['Recency_Flag'] = Cust_date_UK.apply(recency, axis=1)
#Cust_date_UK = Cust_date_UK.groupby('CustomerID',as_index=False)['Recency_Flag'].max()


#Let us check the distribution of Recency flags:

plt.figure(figsize=(12,8))
sns.countplot(x='Recency_Flag', data=Cust_date_UK, color=color[1])
plt.ylabel('Count', fontsize=12)
plt.xlabel('Recency_Flag', fontsize=12)
plt.xticks(rotation='vertical')
plt.title('Frequency of Recency_Flag', fontsize=15)
plt.show()


Cust_freq=data[['Country','InvoiceNo','CustomerID']].drop_duplicates()
#Calculating the count of unique purchase for each customer
Cust_freq_count=Cust_freq.groupby(['Country','CustomerID'])['InvoiceNo'].aggregate('count').\
reset_index().sort_values('InvoiceNo', ascending=False)

Cust_freq_count_UK=Cust_freq_count[Cust_freq_count['Country']=='United Kingdom']
unique_invoice=Cust_freq_count_UK[['InvoiceNo']].drop_duplicates()
# Dividing in 5 equal parts
unique_invoice['Freqency_Band'] = pd.qcut(unique_invoice['InvoiceNo'], 5)
unique_invoice=unique_invoice[['Freqency_Band']].drop_duplicates()
unique_invoice

#Tagging customers in the range of 1 to 5 based on the count of their unique invoice 
#where 5 corresponds to those customers who visit the store most often:


def frequency(row):
  if row['InvoiceNo'] <= 13:
    val = 1
  elif row['InvoiceNo'] > 13 and row['InvoiceNo'] <= 25:
    val = 2
  elif row['InvoiceNo'] > 25 and row['InvoiceNo'] <= 38:
    val = 3
  elif row['InvoiceNo'] > 38 and row['InvoiceNo'] <= 55:
    val = 4
  else:
    val = 5
  return val
Cust_freq_count_UK['Freq_Flag'] = Cust_freq_count_UK.apply(frequency, axis=1)


#Let us check the distribution of Frequency flags:

plt.figure(figsize=(12,8))
sns.countplot(x='Freq_Flag', data=Cust_freq_count_UK, color=color[1])
plt.ylabel('Count', fontsize=12)
plt.xlabel('Freq_Flag', fontsize=12)
plt.xticks(rotation='vertical')
plt.title('Frequency of Freq_Flag', fontsize=15)
plt.show()

#==============================================================================
# It can be seen that most of the customers are visiting the 
#store less than 13 times a year. Therefore, now it will be interesting to see
# what the variation is in the Monetary value that these customers contribute.
# 
#==============================================================================


#Calculating the Sum of total monetary purchase for each customer
Cust_monetary = data.groupby(['Country','CustomerID'])['Total_Price'].aggregate('sum').\
reset_index().sort_values('Total_Price', ascending=False)
Cust_monetary_UK=Cust_monetary[Cust_monetary['Country']=='United Kingdom']

#Notice that there are some negative values in the total price column. This is the case because when a customer returns the product it purchased, it is stored as a negative value in the quantity column.

#Before splitting Total price in 5 parts, we will remove these negative quantities.

unique_price=Cust_monetary_UK[['Total_Price']].drop_duplicates()
unique_price=unique_price[unique_price['Total_Price'] > 0]
unique_price['monetary_Band'] = pd.qcut(unique_price['Total_Price'], 5)
unique_price=unique_price[['monetary_Band']].drop_duplicates()
unique_price

#Tagging customers in the range of 1 to 5 based on their Total price value, where 5 corresponds the customers having highest monetary value:

def mont(row):
  if row['Total_Price'] <= 243:
    val = 1
  elif row['Total_Price'] > 243 and row['Total_Price'] <= 463:
    val = 2
  elif row['Total_Price'] > 463 and row['Total_Price'] <= 892:
    val = 3
  elif row['Total_Price'] > 892 and row['Total_Price'] <= 1932:
    val = 4
  else:
    val = 5
  return val
Cust_monetary_UK['Monetary_Flag'] = Cust_monetary_UK.apply(mont, axis=1)


#Let us check the distribution of Monetary flags:

plt.figure(figsize=(12,8))
sns.countplot(x='Monetary_Flag', data=Cust_monetary_UK, color=color[1])
plt.ylabel('Count', fontsize=12)
plt.xlabel('Monetary_Flag', fontsize=12)
plt.xticks(rotation='vertical')
plt.title('Frequency of Monetory_Flag', fontsize=15)
plt.show()


#Combining all the three flags :

Cust_UK_All=pd.merge(Cust_date_UK,Cust_freq_count_UK[['CustomerID','Freq_Flag']],\
on=['CustomerID'],how='left')
Cust_UK_All=pd.merge(Cust_UK_All,Cust_monetary_UK[['CustomerID','Monetary_Flag']],\
on=['CustomerID'],how='left')
Cust_UK_All.head(10)