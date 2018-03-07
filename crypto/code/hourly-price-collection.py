#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 13:38:33 2018

@author: tkh5044
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline
%config InlineBackend.figure_format = 'retina'
sns.set_style('darkgrid')
sns.set_context('poster', font_scale=1)

from time import sleep, time
from datetime import timedelta, datetime, date, timezone
import requests
pd.options.display.max_columns = 100
pd.options.display.max_rows = 100
pd.options.display.max_colwidth = 60

import coinmarketcap
import json


def get_all_coin_symbols():
    a = requests.get('https://www.cryptocompare.com/api/data/coinlist/')
    a = a.json()['Data']
    coins = [i for i in a]
    print (len(coins), 'coins on the market, today!')
    return coins

def get_top_100_coins():
    market = coinmarketcap.Market()
    cmc = market.ticker()
    df = pd.DataFrame(cmc)
    top_100_coins = list(df.symbol)
    return top_100_coins
    

coins = get_all_coin_symbols()
saved_hourly = pd.read_csv('../exported_csvs/hourly_prices.csv')
current_top100 = get_top_100_coins()

for i in list(saved_hourly.columns):
    print ('Assets that have fallen out of top 100:')
    if i not in current_top100:
        print (i)

print ()

for i in current_top100:
    print ('Assets that have entered the top 100:')
    if i not in list(saved_hourly.columns):
        print (i)