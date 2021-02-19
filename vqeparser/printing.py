#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 21:03:06 2021

@author: rgonzalez
"""

from pandas import DataFrame

def print_opts_block(opts):
    
    if type(opts) == dict:
        opts = list(map(list, opts.items()))
        
        for i in range(len(opts)):
            opts[i][0] = str(opts[i][0]) + ': '
        
    
    l1, l2 = len(opts), len(opts[0])
    opts = DataFrame(opts, index=['']*l1, columns=['']*l2)
    print(opts)
    
