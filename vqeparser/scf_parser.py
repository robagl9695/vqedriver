#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 15:20:31 2021

@author: rgonzalez
"""

from qiskit.chemistry.drivers import HFMethodType
import sys

def _scf(blocks, spin):
    spin = int(spin)
    scf_block = [block for block in blocks if block.startswith('%scf')]
    if len(scf_block) == 0:
        if spin == 0:
            scfmethod = HFMethodType.RHF
        else:
            scfmethod = HFMethodType.ROHF
        scfconv = 9
        scfiter = 50
    else: 
        scf_block = scf_block[0]
    
        scf_opts = scf_block.split(' ')
    
        scf_conv = [opt for opt in scf_opts if opt.startswith('conv')]
        if len(scf_conv) != 0:
            scfconv = int(scf_conv[0].split('=')[1].strip('\n'))
        else:
            scfconv = 9
        
        scf_cycles = [opt for opt in scf_opts if opt.startswith('maxcycles')]
        if len(scf_cycles) != 0:
            scfiter = int(scf_cycles[0].split('=')[1].strip('\n'))
        else:
            scfiter = 50
            
        scf_core = [opt for opt in scf_opts if opt.startswith('maxcore')]
        if len(scf_core) != 0:
            scfcore = int(scf_core[0].split('=')[1].strip('\n'))
        else:
            scfcore = 1000
    
        scf_method = [opt for opt in scf_opts if opt.startswith('method')]
        if len(scf_method) != 0:
            scfmethod = str(scf_method[0].split('=')[1].strip('\n'))
            if scfmethod == 'rhf':
                if spin != 0:
                    print('SCFError: Open-shell molecule, select between UHF and ROHF')
                    sys.exit(1)
                else:
                    scfmethod = HFMethodType.RHF
            elif scfmethod == 'uhf':
                scfmethod = HFMethodType.UHF
            elif scfmethod == 'rohf':
                scfmethod = HFMethodType.ROHF
            else:
                print('SCFError: Invalid HF method')
                sys.exit(1)
        else:
            if spin == 0:
                scfmethod = HFMethodType.RHF
            else:
                scfmethod = HFMethodType.ROHF
    
    return scfmethod, scfconv, scfiter, scfcore