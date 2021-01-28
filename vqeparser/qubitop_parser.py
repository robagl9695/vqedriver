#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 15:05:20 2021

@author: rgonzalez
"""

import sys

def _qubitop(blocks):
    qubitop_block = [block for block in blocks if block.startswith('%qubitop')]
    
    if len(qubitop_block) == 0:
        qubitop_map = 'parity'
        qubitop_threshold = 8
        qubitop_z2red = False
    else:
        qubitop_block = qubitop_block[0]
        qubitop_opts = qubitop_block.split(' ')
        
        qubitop_map = [opt for opt in qubitop_opts if opt.startswith('map')]
        
        map_avail = ['jordan_wigner', 'parity', 'bravyi_kitaev']
        
        if len(qubitop_map) != 0:
            qubitop_map = qubitop_map[0].split('=')[1].strip('\n')
            if qubitop_map not in map_avail:
                print('MappingError: Invalid fermionic operator mapping selected')
                sys.exit(1)
            else:
                qubitop_map = qubitop_map
            
        qubitop_threshold = [opt for opt in qubitop_opts if opt.startswith('threshold')]
            
        if len(qubitop_threshold) != 0:
            qubitop_threshold = int(qubitop_threshold[0].split('=')[1].strip('\n'))
        else:
            qubitop_threshold = 8
            
        qubitop_z2red = [opt for opt in qubitop_opts if opt.startswith('z2red')]
            
        if len(qubitop_z2red) != 0:
            qubitop_z2red = qubitop_z2red[0].split('=')[1].strip('\n')
            if qubitop_z2red == 'true':
                qubitop_z2red = True
            elif qubitop_z2red == 'false':
                qubitop_z2red = False
            else:
                print('MappingError: Invalid option for Z2 symmetries')
                sys.exit(1)
        else:
            qubitop_z2red = False
        
    return qubitop_map, qubitop_threshold, qubitop_z2red