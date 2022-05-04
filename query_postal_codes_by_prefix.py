#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  4 15:21:13 2022

@author: amandatay
"""

import pandas as pd
import numpy as np
import requests
import itertools
import time
import os

os.chdir('/Users/amandatay/doc/ds/02_postal_code_api')


#postal_list = ['528540','380013','520840','000000']

#ref: https://en.wikipedia.org/wiki/Postal_codes_in_Singapore


def generate_postal_list(prefix):
    postal_list = []
    for combination in itertools.product(range(10), repeat=4):
        out = prefix + (''.join(map(str, combination)))
        postal_list.append(out)
    return postal_list
    
def getcoordinates(address):
    req = requests.get('https://developers.onemap.sg/commonapi/search?searchVal='+address+'&returnGeom=Y&getAddrDetails=Y&pageNum=1')
    resultsdict = eval(req.text)
    if len(resultsdict['results'])>0:
#        return resultsdict['results'][0]['LATITUDE'], resultsdict['results'][0]['LONGITUDE']
        return resultsdict['results'][0], None
    else:
        return None, address
        pass
    
def get_all_postal_codes_by_prefix(prefix):
    start_time = time.time()
    postal_lists = generate_postal_list(prefix)
    
    # splitting postal list into half (5000) to reduce timeout errors
    l = len(postal_lists)//2
    postal_list_1 = postal_lists[:l]
    postal_list_2 = postal_lists[l:]
    
    for postal_list in [postal_list_1, postal_list_2]:
        print('Running for {}'.format(postal_list[0][:3]))
        results_list = []
        error_list = []
        for _ in postal_list:
            res, error = getcoordinates(_)
            if res is not None:
                results_list.append(res)
            if error is not None:
                error_list.append(error)
        
        postal_df = pd.DataFrame(results_list)
        postal_df.to_csv('data/postal_list_{}.csv'.format(postal_list[0][:3]), index = False)

        with open('data/errors_{}.csv'.format(postal_list[0][:3]), 'w') as f:
          for item in error_list:
              f.write("%s\n" % item)
              
        end_time = time.time()
        time_taken = end_time - start_time
        print('Saved result to postal_list_{}.csv. (Time taken: {}ms'.format(postal_list[0][:3], time_taken))
        
        
if __name__ == "__main__":
    import sys

    prefix = sys.argv[1]
    prefix = str(prefix)
    
    get_all_postal_codes_by_prefix(prefix)

#get_all_postal_codes_by_prefix('02')
# postal district 01
#get_all_postal_codes_by_prefix('01')
# get_all_postal_codes_by_prefix('02')
#get_all_postal_codes_by_prefix('03')
# get_all_postal_codes_by_prefix('04')
# get_all_postal_codes_by_prefix('05')
# get_all_postal_codes_by_prefix('06')
# postal district 02
# get_all_postal_codes_by_prefix('07')
# get_all_postal_codes_by_prefix('08')
# postal district 03
# get_all_postal_codes_by_prefix('14')
# get_all_postal_codes_by_prefix('15')
# get_all_postal_codes_by_prefix('16')
# postal district 04
# get_all_postal_codes_by_prefix('09')
# get_all_postal_codes_by_prefix('10')
# postal_district 05
# get_all_postal_codes_by_prefix('11')
# get_all_postal_codes_by_prefix('12')
# get_all_postal_codes_by_prefix('13')
# postal_district 06
# get_all_postal_codes_by_prefix('17')
# postal_district 07
# get_all_postal_codes_by_prefix('18')
# get_all_postal_codes_by_prefix('19')
# postal_district 08
# get_all_postal_codes_by_prefix('20')
# get_all_postal_codes_by_prefix('21')
# postal_district 09
# get_all_postal_codes_by_prefix('22')
# get_all_postal_codes_by_prefix('23')
# postal district 10
# get_all_postal_codes_by_prefix('25')
# get_all_postal_codes_by_prefix('26')
# get_all_postal_codes_by_prefix('27')