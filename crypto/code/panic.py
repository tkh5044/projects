#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 15:06:43 2018

@author: tkh5044
"""

import pandas as pd
import seaborn as sns

sns.set_style('darkgrid')
sns.set_context('poster', font_scale=1)

from time import sleep, time
from datetime import timedelta, datetime, date, timezone
import requests
pd.options.display.max_columns = 30
pd.options.display.max_colwidth = 60

## READ IN RESULTS OF LAST API REQUEST
old = pd.read_csv('~/Documents/projects/crypto/exported_csvs/cryptopanic-api-results.csv', encoding='utf-8')

def get_cryptopanic_data(old_df):
    df = pd.DataFrame(columns=['published_at', 'important', 'positive', 'negative', 'BTC', 'ETH', 'XRP', 'BCH', 'LTC',
                               'XLM', 'EOS', 'NEO', 'MIOTA', 'DASH', 'XMR', 'VEN', 'source', 'title', 'domain', 'id', 'url'])

    url = 'https://cryptopanic.com/api/posts/?auth_token=ac311fed02ded0604b0d9a8aade566ffcc619a23&currencies=BTC&filter=trending'
    
    for i in range(10):
        cp = requests.get(url)
        assert cp.status_code == 200
        cp = cp.json()
        results = cp['results']

        for entry in results:    #iterates through each results
            domain = entry['domain']
            important = entry['votes']['important']
            positive = entry['votes']['positive']
            negative = entry['votes']['negative']
            source = entry['source']['title']
            title = entry['title']
            published_at = entry['published_at'].replace('T', ' ').replace('Z', '')

            cryptos = [code['code'] for code in entry['currencies']]
            crypto_cols = ['BTC', 'ETH', 'XRP', 'BCH', 'LTC', 'XLM', 'EOS', 'NEO', 'MIOTA', 'DASH', 'XMR', 'VEN']
            crypto_dummies = [1 if i in cryptos else 0 for i in crypto_cols]

            id_number = entry['id']
            url = entry['url']

            new_row = [published_at, important, positive, negative]
            new_row.extend(crypto_dummies)
            new_row.extend([source, title, domain, id_number, url])

            df.loc[len(df)] = new_row
       
        url = cp['next']
        sleep(1.5)
    
    df.published_at = pd.to_datetime(df.published_at)
    df = pd.concat([df, old_df])
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df

df = get_cryptopanic_data(old)

new_count = (len(df) - len(old))
unique_new_titles = (len(df.title.drop_duplicates()) - len(old))

print ('Number of records imported:    ', len(old))
print ('Number of new results = 200:   ', (new_count == 200))
print ('Number of new unique titles:   ', unique_new_titles)
print ('Number of indices to drop:     ', (new_count - unique_new_titles))

## DROP DUPLICATED TITLE - KEEP NEWEST RESULTS (SHOWS UPDATED NUMBER OF TAGS)

def drop_duplicate_titles(df, new_count, unique_new_titles):
    all_drop_indices = []
    for i in list(df[df.title.duplicated()].title):
        temp_df = df[(df.title == i)]
    
        max_tag_count = 0
        for j in temp_df.index:
            if temp_df.loc[j, 'important':'negative'].sum() > max_tag_count:
                max_tag_count = temp_df.loc[j, 'important':'negative'].sum()
                max_tag_count_index = j
    
        drop_indices = [i for i in list(temp_df.index) if i != max_tag_count_index]
        all_drop_indices.extend(drop_indices)
        
    #assert len(all_drop_indices) == (new_count - unique_new_titles)  # checks if number of indices to drop is correct
    
    df.drop(all_drop_indices, inplace=True)
    # assert len(df) == (len(old) + unique_new_titles)  # checks if size of df is correct
    print ('Total number of records:', len(df))
    
    return df

df = drop_duplicate_titles(df, new_count, unique_new_titles)

## EXPORT TO CSV
df.to_csv('~/Documents/projects/crypto/exported_csvs/cryptopanic-api-results.csv', index=False)