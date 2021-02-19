#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 11:41:00 2021

@author: rgonzalez
"""

from qiskit.providers.aer import QasmSimulator, StatevectorSimulator
import sys

simulators_avail = ['statevector', 'qasm']

qasm_methods = ['statevector', 
                'density_matrix', 
                #'stabilizer', 
                #'extended_stabilizer',
                'matrix_product_state',
                'automatic']

sv_methods = ['statevector']

def set_qasm(sim_opts):
    
    sim_method = [opt for opt in sim_opts if opt.startswith('method')]

    if len(sim_method) == 0:
        backend = QasmSimulator(method='automatic',
                                max_memory_mb=2048)
        sim_method = 'automatic'
    else:
        sim_method = sim_method[0].split('=')[1].strip('\n')
        
        if sim_method not in qasm_methods:
            print('SimulationError: simulation method not available. Available options: "statevector", "density_matrix", "matrix_product_state", "automatic"')
            sys.exit()
        else:
            backend = QasmSimulator(method=sim_method,
                                max_memory_mb=2048)
        
    return backend, sim_method

def set_sv(sim_opts):
    
    sim_method = [opt for opt in sim_opts if opt.startswith('method')]

    if len(sim_method) == 0:
        backend = StatevectorSimulator(max_memory_mb = 2048,
                                       statevector_parallel_threshold=8)
        sim_method = 'statevector'
    else:
        sim_method = sim_method[0].split('=')[1].strip('\n')
        
        if sim_method not in sv_methods:
            print('SimulationError: simulation method not available. Available options: "statevector"')
            sys.exit()
        else:
            backend = StatevectorSimulator(max_memory_mb = 2048,
                                       statevector_parallel_threshold=8)
        
    return backend, sim_method

def set_backend(sim_opts):
    
    sim_backend = [opt for opt in sim_opts if opt.startswith('backend')]
    
    if len(sim_backend) != 0:
        sim_backend = sim_backend[0].split('=')[1].strip('\n')
        if sim_backend not in simulators_avail:
            print('SimulationError: simulator not available, choose between "qasm" and "statevector"')
            sys.exit()
        elif sim_backend == 'qasm':
            backend, method = set_qasm(sim_opts)
            
        elif sim_backend == 'statevector':
            backend, method = set_sv(sim_opts)

    else:
        backend, method = set_sv(sim_opts)
        
    return backend, sim_backend, method

def _simulation(blocks):
    sim_block = [block for block in blocks if block.startswith('%sim')]
    
    if len(sim_block) == 0:
        backend = QasmSimulator()
        sim_backend = 'qasm'
    else:
        sim_block = sim_block[0]
        sim_opts = sim_block.split(' ')
        
        backend, sim_backend, method = set_backend(sim_opts)
            
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
        
        sim_shots = [opt for opt in sim_opts if opt.startswith('shots')]    
        
        if len(sim_shots) != 0:
            sim_shots = sim_shots[0].split('=')[1].strip('\n')
            try:
                sim_shots = int(sim_shots)
            except:
                print('SimulationError: the number of shots have to be an integer number')
        else:
            sim_shots = 8192
        
    return backend, sim_backend, method, sim_shots, sim_exact