# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 14:23:30 2014

@author: rob
"""

import wiot as wt

wiot = wt.wiot
fd = wiot.final_demand

#%%
# Chinese Vehicles (sector 15)
before = wiot.total_production().copy()
fd.ix['CHN', 15] = fd.ix['CHN', 15] - 1
after = wiot.total_production().copy()
deltas = after - before
country_totals = deltas.sum(level='from_iso3')

#%%
deltas.to_csv('wiot_2010_chnvec.csv', header=True)
country_totals.to_csv('wiot_2010_chnvec_totals.csv', header=True)