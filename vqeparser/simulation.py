#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 11:41:00 2021

@author: rgonzalez
"""

from qiskit.providers.aer import QasmSimulator, StatevectorSimulator
import sys

simulators_avail = ['statevector', 'qasm']

def _simulation(blocks):
    sim_block = [block for block in blocks if block.startswith('%sim')]
    
    if len(sim_block) == 0:
        backend = QasmSimulator()
        sim_backend = 'qasm'
    else:
        sim_block = sim_block[0]
        sim_opts = sim_block.split(' ')
        
        sim_backend = [opt for opt in sim_opts if opt.startswith('backend')]
        
        if len(sim_backend) != 0:
            sim_backend = sim_backend[0].split('=')[1].strip('\n')
            if sim_backend not in simulators_avail:
                print('SimulationError: simulator not available, choose between "qasm" and "statevector"')
                sys.exit()
            elif sim_backend == 'qasm':
                backend = QasmSimulator()
            elif sim_backend == 'statevector':
                backend = StatevectorSimulator()

        else:
            backend = QasmSimulator()
            
        sim_exact = [opt for opt in sim_opts if opt.startswith('exact')]
        
        if len(sim_exact) != 0:
            sim_exact = sim_exact[0].split('=')[1].strip('\n')
            if sim_exact == 'true':
                sim_exact = True
            elif sim_exact == 'false':
                sim_exact = False
            else:
                print('SimulationError: Invalid option for exact calculations')
                sys.exit()
        else:
            sim_exact = True
        
    return backend, sim_backend, sim_exact