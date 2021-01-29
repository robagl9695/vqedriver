#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 22:46:10 2021

@author: rgonzalez
"""
from pyscf.gto.basis import parse
import os
import sys
from collections import Counter

prefix = os.getcwd()

basen_path = prefix + '/basen/'

basis_dict = {'6-21G': '6-21g.1.nw',
              '6-311+G': '6-311+g.0.nw', 
              '6-311G': '6-311g.0.nw',
              '6-311++G': '6-311++g.0.nw', 
              '6-311++G(2d,2p)': '6-311++g(2d,2p).0.nw', 
              '6-311+G(2d,p)':'6-311+g(2d,p).0.nw',
              '6-311+G(3df,3pd)':'6-311++g(3df,3pd).0.nw',
              '6-311+G(d,p)':'6-311g(d,p).0.nw',
              '6-311+G*':'6-311+g_st_.0.nw', 
              '6-311G*':'6-311g_st_.0.nw',
              '6-311++G*':'6-311++g_st_.0.nw',
              '6-311+G**':'6-311+g_st__st_.0.nw',
              '6-311G**':'6-311g_st__st_.0.nw',
              '6-311++G**':'6-311++g_st__st_.0.nw',
              '6-31+G':'6-31+g.1.nw',
              '6-31++G':'6-31++g.1.nw',
              '6-31+G*':'6-31+g_st_.1.nw',
              '6-31++G*':'6-31++g_st_.1.nw',
              '6-31+G**':'6-31+g_st__st_.1.nw',
              '6-31++G**':'6-31++g_st__st_.1.nw',
              'aug-cc-pVDZ':'aug-cc-pvdz.1.nw',
              'aug-cc-pVQZ':'aug-cc-pvqz.1.nw', 
              'aug-cc-pVTZ':'aug-cc-pvtz.1.nw', 
              'cc-pVDZ':'cc-pvdz.1.nw',
              'cc-pVQZ':'cc-pvqz.1.nw',
              'cc-pVTZ':'cc-pvtz.1.nw',
#              'def2-ECP':'def2-ecp.1.nw',
              'def2-QZVP':'def2-qzvp.1.nw',
              'def2-QZVPP':'def2-qzvpp.1.nw',
              'def2-SV(P)':'def2-sv(p).1.nw',
              'def2-SVP':'def2-svp.1.nw',
              'def2-TZVP':'def2-tzvp.1.nw',
              'def2-TZVPP':'def2-tzvpp.1.nw',
              'DZ':'dz (dunning-hay).0.nw',
              'DZP+d':'dzp + diffuse (dunning-hay).0.nw',
              'DZP':'dzp (dunning-hay).0.nw',
              'LANL2DZ':'lanl2dz.0.nw',
              'MINI':'mini.0.nw',
              'STO-2G':'sto-2g.1.nw',
              'STO-3G':'sto-3g.1.nw',
              'STO-4G':'sto-4g.1.nw',
              'STO-5G':'sto-5g.1.nw',
              'STO-6G':'sto-6g.1.nw',
              'SV':'sv (dunning-hay).0.nw',
              'SVP+d':'svp + diffuse (dunning-hay).0.nw',
              'SVP':'svp (dunning-hay).0.nw',
              'TZ':'tz (dunning-hay).0.nw',
              'UGBS':'ugbs.0.nw'}

def unique(list1): 
  
    # initialize a null list 
    unique_list = [] 
      
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x) 
            
    return unique_list
    

def get_atoms(coords):
    
    coords = coords.split(';')
    
    atoms = []
    
    for i in range(len(coords)):
        atom = coords[i].split()[0]
        atoms.append(atom)
        
    #atoms = unique(atoms)
    
    atoms = Counter(atoms)
    
    return atoms

def get_atoms_avail(basisblocks):
        
    atoms = []
    
    for i in range(len(basisblocks)):
        atom = basisblocks[i].split()[0]
        atoms.append(atom)
        
    atoms = unique(atoms)
    
    return atoms

def read_basisset(basisset, coords):
    basis_file = basen_path + basis_dict[basisset]
   
    #read the basis set file
    
    basis_file = open(basis_file, 'r')
    
    if basis_file.mode == 'r':
        contents = basis_file.read()
        
    basis_file.close()
    
    #read each block

    key = '#'
    key_indexes = []
    
    index = 0

    while index < len(contents):
        index = contents.find(key, index)
        if index == -1:
            break
        else:
            key_indexes.append(index)
            
        index += len(key)
    
    basis_blocks = []
    
    for i in range(0, len(key_indexes),1):
        start = key_indexes[i]
        if i == len(key_indexes)-1:
            end = len(contents)
        else:
            end = key_indexes[i+1]-1
        block = contents[start:end]
        
        basis_blocks.append(block)
    
    #clean each block from extra info
    
    basisblocks = []
    
    for i in range(0, len(basis_blocks), 1):
        block = basis_blocks[i]
        
        if block.startswith('#BASIS SET'):
            block = block.split('\n', 1)[1]
            basisblocks.append(block)
            
    del basis_blocks
    
    basisblocks[-1] = basisblocks[-1].split('END')[0]
    
    atoms = get_atoms(coords)
    atoms_avail = get_atoms_avail(basisblocks)
    
    unavailable = []
    
    for atom in atoms:
        if atom not in atoms_avail:
            unavailable.append(atom)
    
    if len(unavailable) != 0:
        print('BasisSetError: ' + basisset + ' unavailable for the following elements:')
        print(unavailable)
        sys.exit()
    
    basis = {}
    
    for atom in atoms:
        index = atoms_avail.index(atom)
        basis[atom] = parse(basisblocks[index])
        
    basisdim = 0
    basistotal = 0
    
    for atom in atoms:
        index = atoms_avail.index(atom)
        atom_block = basisblocks[index]
        atom_block = atom_block.split('\n')
        
        for i in reversed(range(0, len(atom_block), 1)):
            if atom_block[i].startswith(atom):
                atom_block.pop(i)
                
        numatoms = atoms[atom]
        
        basisdim += len(atom_block)
        basistotal += len(atom_block)*numatoms
    
    return basis, basisdim, basistotal
    
    
def _basis(blocks, coords):
    basis_block = [block for block in blocks if block.startswith('%basis')]

    if len(basis_block) == 0:
        print('BasisSetError: Basis set missing')
        sys.exit()
    elif len(basis_block) > 1:
        print('BasisSetError: More than one basis set specified')
        sys.exit()
    
    basis_block = basis_block[0]
    
    basis_opts = basis_block.split(' ')
    
    basis_all = [opt for opt in basis_opts if opt.startswith('all')][0]
    basisset = basis_all.split('=')[1]
    
    if basisset not in basis_dict:
        print('BasisSetError: Basis set not available')
        sys.exit()
    
    basis, basisdim, basistotal = read_basisset(basisset, coords)
    
    return basis, basisset, basisdim, basistotal