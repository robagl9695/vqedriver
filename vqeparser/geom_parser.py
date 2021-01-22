#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 21:36:20 2021

@author: rgonzalez
"""

from qiskit.chemistry.drivers import UnitsType
import os
import sys

def read_xyzfile(filename):
    
    prefix = os.getcwd()
    
    xyzcoords = open(prefix + '/' + filename, 'r')
    if xyzcoords.mode == 'r':
        contents = xyzcoords.readlines()
    xyzcoords.close()
    
    for i in reversed(range(2, len(contents), 1)):
        if contents[i] == '\n':
            contents.pop(i)
    
    try:
        numatoms = int(contents[0])
    except:
        TypeError('Invalid XYZ file format')
        
    if len(contents) != numatoms+2:
        raise TypeError('Invalid XYZ file format')
    
    coords = ''
    
    for i in range(2, len(contents)-1, 1):
        contents[i] = ' '.join(contents[i].split())
        coords += contents[i].strip('\n') + '; '
    
    contents[-1] = ' '.join(contents[-1].split())
    coords += contents[-1].strip('\n')
    coords = coords.replace('\t', ' ')
    
    return coords


def _geom(blocks):
    geom_block = [block for block in blocks if block.startswith('%geometry')]
    
    if len(geom_block) == 0:
        print('GeometryInputError: Geometry specification missing')
        sys.exit(1)
    elif len(geom_block) > 1:
        print('GeometryInputError: More than geometry specified')
        sys.exit(1)
    
    geom_block = geom_block[0]
    
    geom_opts = geom_block.split(' ')
    
    geom_xyzfile = [opt for opt in geom_opts if opt.startswith('xyzfile')][0]
    xyzfile = geom_xyzfile.split('=')[1]
    coords = read_xyzfile(xyzfile)
    
    geom_charge = [opt for opt in geom_opts if opt.startswith('charge')]
    if len(geom_charge) != 0:
        charge = int(geom_charge[0].split('=')[1])
    else:
        charge = 0
        
    geom_spin = [opt for opt in geom_opts if opt.startswith('spin')]
    if len(geom_spin) != 0:
        spin = int(geom_spin[0].split('=')[1])
    else:
        spin = 0
        
    geom_units = [opt for opt in geom_opts if opt.startswith('units')]
    if len(geom_units) != 0:
        if geom_units[0].split('=')[1] == 'angstrom':
            units = UnitsType.ANGSTROM
        elif geom_units[0].split('=')[1] == 'bohr':
            units = UnitsType.BOHR
        else:
            print('GeometryInputError: Invalid Units on Input, please select between "angstrom" and "bohr" (Default = angstrom)')
            sys.exit(1)
    else:
        units = UnitsType.ANGSTROM

    return coords, charge, spin, units