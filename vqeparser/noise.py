#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 21:18:14 2021

@author: rgonzalez
"""

import qiskit.providers.aer.noise as noise
import sys
import numpy as np

noise_avail = ['none',
               'depolarizing',
               'readout',
               'dephasing',
               'thermal',
               'bonet12',
               'bonet23',
               'bonet']

qasm_1qubit_gates = ['u1',
 'u2',
 'u3',
 'u',
 'p',
 'r',
 'rx',
 'ry',
 'rz',
 'id',
 'x',
 'y',
 'z',
 'h',
 's',
 'sdg',
 'sx',
 't',
 'tdg']

qasm_2qubit_gates = ['swap',
 'cx',
 'cy',
 'cz',
 'csx',
 'cp',
 'cu1',
 'cu2',
 'cu3']

#noise model initialization

noise_model = noise.NoiseModel()

def none(backend):
    if backend.name() == 'qasm_simulator':
        noise_model = noise.NoiseModel()
    else:
        print('SimulationError: Invalid option for noisy simulator')
        sys.exit()
        
    return noise_model

def depolarizing(backend, p = 0.001):
    if backend.name() == 'qasm_simulator':
        qubit1 = p/10
        qubit2 = p
        
        error_qubit1 = noise.depolarizing_error(qubit1, 1)
        error_qubit2 = noise.depolarizing_error(qubit2, 2)
        
        noise_model.add_all_qubit_quantum_error(error_qubit1, qasm_1qubit_gates)
        noise_model.add_all_qubit_quantum_error(error_qubit2, qasm_2qubit_gates)
    else:
        print('SimulationError: Invalid option for noisy simulator')
        sys.exit()
        
    return noise_model

def readout(backend, p = 0.01):
    if backend.name() == 'qasm_simulator':
        
        error_bitflip = noise.errors.pauli_error([('X',p), ('I', 1 - p)])
        noise_model.add_all_qubit_quantum_error(error_bitflip, 'measure')
        
    else:
        print('SimulationError: Invalid option for noisy simulator')
        sys.exit()
        
    return noise_model

def dephasing(backend, p = 0.01):
    if backend.name() == 'qasm_simulator':

        #1-qubit kraus operators
        A0 = np.sqrt(p/100)*np.array([[1,0],
                                      [0,0]])
        A1 = np.sqrt(p/100)*np.array([[0,0], 
                                      [0,1]])
        A2 = np.sqrt(1-p/100)*np.array([[1,0],
                                          [0,1]])
        
        kraus_ops = [A0, A1, A2]
    
        dephase_error = noise.kraus_error(kraus_ops)
        noise_model.add_all_qubit_quantum_error(dephase_error, qasm_1qubit_gates)

        #2-qubit kraus operators
        A0 = np.sqrt(p)*np.array([[1,0,0,0],
                                  [0,0,0,0],
                                  [0,0,0,0],
                                  [0,0,0,0]])
        A1 = np.sqrt(p)*np.array([[0,0,0,0],
                                  [0,1,0,0],
                                  [0,0,0,0],
                                  [0,0,0,0]])
        A2 = np.sqrt(p)*np.array([[0,0,0,0],
                                  [0,0,0,0],
                                  [0,0,1,0],
                                  [0,0,0,0]])
        A3 = np.sqrt(p)*np.array([[0,0,0,0],
                                  [0,0,0,0],
                                  [0,0,0,0],
                                  [0,0,0,1]])
        A4 = np.sqrt(1-p)*np.array([[1,0,0,0],
                                    [0,1,0,0],
                                    [0,0,1,0],
                                    [0,0,0,1]])

        kraus_ops = [A0, A1, A2, A3, A4]

        dephase_error = noise.kraus_error(kraus_ops)
        noise_model.add_all_qubit_quantum_error(dephase_error, qasm_2qubit_gates)
        
    else:
        print('SimulationError: Invalid option for noisy simulator')
        sys.exit()
        
    return noise_model

def thermal(backend, T1 = 20000, T2 = 20000, t = 20):
    
    #times in ns
    if backend.name() == 'qasm_simulator':
        
        thermal_error = noise.thermal_relaxation_error(T1, T2, t)
        noise_model.add_all_qubit_quantum_error(thermal_error, qasm_1qubit_gates)
        
    else:
        print('SimulationError: Invalid option for noisy simulator')
        sys.exit()
        
    return noise_model

def bonet(backend, p = 0.01, q = 0.01, T1 = 20000, T2 = 20000, t = 20):
    
    #times in ns
    if backend.name() == 'qasm_simulator':
        
        #dephasing component
        A0 = np.sqrt(p/100)*np.array([[1,0], [0,0]])
        A1 = np.sqrt(p/100)*np.array([[0,0], [0,1]])
        A2 = np.sqrt(1-p/100)*np.array([[1,0], [0,1]])
        
        kraus_ops = [A0, A1, A2]
    
        dephase_error = noise.kraus_error(kraus_ops)
        noise_model.add_all_qubit_quantum_error(dephase_error, qasm_1qubit_gates)

        #2-qubit kraus operators
        A0 = np.sqrt(p)*np.array([[1,0,0,0],
                                  [0,0,0,0],
                                  [0,0,0,0],
                                  [0,0,0,0]])
        A1 = np.sqrt(p)*np.array([[0,0,0,0],
                                  [0,1,0,0],
                                  [0,0,0,0],
                                  [0,0,0,0]])
        A2 = np.sqrt(p)*np.array([[0,0,0,0],
                                  [0,0,0,0],
                                  [0,0,1,0],
                                  [0,0,0,0]])
        A3 = np.sqrt(p)*np.array([[0,0,0,0],
                                  [0,0,0,0],
                                  [0,0,0,0],
                                  [0,0,0,1]])
        A4 = np.sqrt(1-p)*np.array([[1,0,0,0],
                                    [0,1,0,0],
                                    [0,0,1,0],
                                    [0,0,0,1]])

        kraus_ops = [A0, A1, A2, A3, A4]

        dephase_error = noise.kraus_error(kraus_ops)
        noise_model.add_all_qubit_quantum_error(dephase_error, qasm_2qubit_gates)

        
        #readout component
        error_bitflip = noise.errors.pauli_error([('X',q), ('I', 1 - q)])
        noise_model.add_all_qubit_quantum_error(error_bitflip, 'measure')
        
        #thermal component
        thermal_error = noise.thermal_relaxation_error(T1, T2, t)
        noise_model.add_all_qubit_quantum_error(thermal_error, qasm_1qubit_gates)
        
    else:
        print('SimulationError: Invalid option for noisy simulator')
        sys.exit()
        
    return noise_model

def bonet12(backend, p = 0.01, q = 0.01, T1 = 20000, T2 = 20000, t = 20):
    
    #times in ns
    if backend.name() == 'qasm_simulator':
        
        #dephasing component
        A0 = np.sqrt(p/100)*np.array([[1,0], [0,0]])
        A1 = np.sqrt(p/100)*np.array([[0,0], [0,1]])
        A2 = np.sqrt(1-p/100)*np.array([[1,0], [0,1]])
        
        kraus_ops = [A0, A1, A2]
    
        dephase_error = noise.kraus_error(kraus_ops)
        noise_model.add_all_qubit_quantum_error(dephase_error, qasm_1qubit_gates)
        
        #2-qubit kraus operators
        A0 = np.sqrt(p)*np.array([[1,0,0,0],
                                  [0,0,0,0],
                                  [0,0,0,0],
                                  [0,0,0,0]])
        A1 = np.sqrt(p)*np.array([[0,0,0,0],
                                  [0,1,0,0],
                                  [0,0,0,0],
                                  [0,0,0,0]])
        A2 = np.sqrt(p)*np.array([[0,0,0,0],
                                  [0,0,0,0],
                                  [0,0,1,0],
                                  [0,0,0,0]])
        A3 = np.sqrt(p)*np.array([[0,0,0,0],
                                  [0,0,0,0],
                                  [0,0,0,0],
                                  [0,0,0,1]])
        A4 = np.sqrt(1-p)*np.array([[1,0,0,0],
                                    [0,1,0,0],
                                    [0,0,1,0],
                                    [0,0,0,1]])

        kraus_ops = [A0, A1, A2, A3, A4]

        dephase_error = noise.kraus_error(kraus_ops)
        noise_model.add_all_qubit_quantum_error(dephase_error, qasm_2qubit_gates)


        #readout component
        error_bitflip = noise.errors.pauli_error([('X',q), ('I', 1 - q)])
        noise_model.add_all_qubit_quantum_error(error_bitflip, 'measure')
        
        #thermal component
        #thermal_error = noise.thermal_relaxation_error(T1, T2, t)
        #noise_model.add_all_qubit_quantum_error(thermal_error, qasm_1qubit_gates)
        
    else:
        print('SimulationError: Invalid option for noisy simulator')
        sys.exit()
        
    return noise_model

def bonet23(backend, p = 0.01, q = 0.01, T1 = 20000, T2 = 20000, t = 20):
    
    #times in ns
    if backend.name() == 'qasm_simulator':
        
        #dephasing component
        #A0 = np.sqrt(p)*np.array([[1,0], [0,0]])
        #A1 = np.sqrt(p)*np.array([[0,0], [0,1]])
        #A2 = np.sqrt(1-p)*np.array([[1,0], [0,1]])
        
        #kraus_ops = [A0, A1, A2]
    
        #dephase_error = noise.kraus_error(kraus_ops)
        #noise_model.add_all_qubit_quantum_error(dephase_error, qasm_1qubit_gates)
        
        #readout component
        error_bitflip = noise.errors.pauli_error([('X',q), ('I', 1 - q)])
        noise_model.add_all_qubit_quantum_error(error_bitflip, 'measure')
        
        #thermal component
        thermal_error = noise.thermal_relaxation_error(T1, T2, t)
        noise_model.add_all_qubit_quantum_error(thermal_error, qasm_1qubit_gates)
        
    else:
        print('SimulationError: Invalid option for noisy simulator')
        sys.exit()
        
    return noise_model

def _noise(blocks, backend):
    noise_block = [block for block in blocks if block.startswith('%noise')]
    
    if len(noise_block) == 0:
        noise_model = none(backend)
        noise_prints = [['Noise Model: ', 'None']]
    else:
        noise_block = noise_block[0]
        noise_opts = noise_block.split(' ')
        
        noise_selection = [opt for opt in noise_opts if opt.startswith('model')]
        
        if len(noise_selection) != 0:
            noise_selection = noise_selection[0].split('=')[1].strip('\n')
            
            if noise_selection not in noise_avail:
                print('SimulationError: noise model not available')
                sys.exit()
            
            if noise_selection == 'none':
                noise_model = none(backend)
                noise_prints = [['Noise Model: ', 'None']]
                
            elif noise_selection == 'depolarizing':
                p = [opt for opt in noise_opts if opt.startswith('rate')]
                if len(p) != 0:
                    p = float(p[0].split('=')[1].strip('\n'))
                else:
                    p = 0.01
                noise_model = depolarizing(backend, p)
                noise_prints = [['Noise Model: ', 'Depolarizing Channel'],
                                ['1-Qubit Gate Depolarizing Error Rate: ', '{:.3e}'.format(p/10)],
                                ['2-Qubit Gate Depolarizing Error Rate: ', '{:.3e}'.format(p)]]
                
            elif noise_selection == 'readout':
                p = [opt for opt in noise_opts if opt.startswith('rate')]
                if len(p) != 0:
                    p = float(p[0].split('=')[1].strip('\n'))
                else:
                    p = 0.01
                noise_model = readout(backend, p)
                noise_prints = [['Noise Model: ', 'Read-out Error Channel'],
                                ['Read-out Error Rate: ', '{:.3e}'.format(p)]]
                
            elif noise_selection == 'dephasing':
                p = [opt for opt in noise_opts if opt.startswith('rate')]
                if len(p) != 0:
                    p = float(p[0].split('=')[1].strip('\n'))
                else:
                    p = 0.01
                noise_model = dephasing(backend, p)
                noise_prints = [['Noise Model: ', 'Dephasing Channel'],
                                ['Dephasing Error Rate: ', '{:.3e}'.format(p)]]

            elif noise_selection == 'thermal':
                T1 = [opt for opt in noise_opts if opt.startswith('T1')]
                if len(T1) != 0:
                    T1 = float(T1[0].split('=')[1].strip('\n'))
                else:
                    T1 = 20000

                T2 = [opt for opt in noise_opts if opt.startswith('T2')]
                if len(T2) != 0:
                    T2 = float(T2[0].split('=')[1].strip('\n'))
                else:
                    T2 = 20000

                t = [opt for opt in noise_opts if opt.startswith('t')]
                if len(t) != 0:
                    t = float(t[0].split('=')[1].strip('\n'))
                else:
                    t = 20                    
                    
                noise_model = thermal(backend, T1, T2, t)
                noise_prints = [['Noise Model: ', 'Thermal Relaxation Channel'],
                                ['T1 constant: ', '{:.2f} ns'.format(T1)],
                                ['T2 constant: ', '{:.2f} ns'.format(T2)],
                                ['Gate Relaxation Time: ', '{:.2f} ns'.format(t)]]
                
            elif noise_selection == 'bonet':
                p = [opt for opt in noise_opts if opt.startswith('dephasing_rate')]
                if len(p) != 0:
                    p = float(p[0].split('=')[1].strip('\n'))
                else:
                    p = 0.01
                    
                q = [opt for opt in noise_opts if opt.startswith('readout_rate')]
                if len(q) != 0:
                    q = float(q[0].split('=')[1].strip('\n'))
                else:
                    q = 0.01
                    
                T1 = [opt for opt in noise_opts if opt.startswith('T1')]
                if len(T1) != 0:
                    T1 = float(T1[0].split('=')[1].strip('\n'))
                else:
                    T1 = 20000

                T2 = [opt for opt in noise_opts if opt.startswith('T2')]
                if len(T2) != 0:
                    T2 = float(T2[0].split('=')[1].strip('\n'))
                else:
                    T2 = 20000

                t = [opt for opt in noise_opts if opt.startswith('t')]
                if len(t) != 0:
                    t = float(t[0].split('=')[1].strip('\n'))
                else:
                    t = 20                    
                    
                noise_model = bonet(backend, p, q, T1, T2, t)
                noise_prints = [['Noise Model: ', 'Dephasing + Thermal + Read-out'],
                                ['Dephasing Error Rate: ', '{:.3e}'.format(p)],
                                ['Read-out Error Rate: ', '{:.3e}'.format(q)],
                                ['T1 constant: ', '{:.2f} ns'.format(T1)],
                                ['T2 constant: ', '{:.2f} ns'.format(T2)],
                                ['Gate Relaxation Time: ', '{:.2f} ns'.format(t)]]
            
            elif noise_selection == 'bonet12':
                p = [opt for opt in noise_opts if opt.startswith('dephasing_rate')]
                if len(p) != 0:
                    p = float(p[0].split('=')[1].strip('\n'))
                else:
                    p = 0.01
                    
                q = [opt for opt in noise_opts if opt.startswith('readout_rate')]
                if len(q) != 0:
                    q = float(q[0].split('=')[1].strip('\n'))
                else:
                    q = 0.01
                    
                T1 = [opt for opt in noise_opts if opt.startswith('T1')]
                if len(T1) != 0:
                    T1 = float(T1[0].split('=')[1].strip('\n'))
                else:
                    T1 = 20000

                T2 = [opt for opt in noise_opts if opt.startswith('T2')]
                if len(T2) != 0:
                    T2 = float(T2[0].split('=')[1].strip('\n'))
                else:
                    T2 = 20000

                t = [opt for opt in noise_opts if opt.startswith('t')]
                if len(t) != 0:
                    t = float(t[0].split('=')[1].strip('\n'))
                else:
                    t = 20                    
                    
                noise_model = bonet(backend, p, q, T1, T2, t)
                noise_prints = [['Noise Model: ', 'Dephasing + Read-out'],
                                ['Dephasing Error Rate: ', '{:.3e}'.format(p)],
                                ['Read-out Error Rate: ', '{:.3e}'.format(q)]]
            
            elif noise_selection == 'bonet23':
                p = [opt for opt in noise_opts if opt.startswith('dephasing_rate')]
                if len(p) != 0:
                    p = float(p[0].split('=')[1].strip('\n'))
                else:
                    p = 0.01
                    
                q = [opt for opt in noise_opts if opt.startswith('readout_rate')]
                if len(q) != 0:
                    q = float(q[0].split('=')[1].strip('\n'))
                else:
                    q = 0.01
                    
                T1 = [opt for opt in noise_opts if opt.startswith('T1')]
                if len(T1) != 0:
                    T1 = float(T1[0].split('=')[1].strip('\n'))
                else:
                    T1 = 20000

                T2 = [opt for opt in noise_opts if opt.startswith('T2')]
                if len(T2) != 0:
                    T2 = float(T2[0].split('=')[1].strip('\n'))
                else:
                    T2 = 20000

                t = [opt for opt in noise_opts if opt.startswith('t')]
                if len(t) != 0:
                    t = float(t[0].split('=')[1].strip('\n'))
                else:
                    t = 20                    
                    
                noise_model = bonet(backend, p, q, T1, T2, t)
                noise_prints = [['Noise Model: ', 'Thermal + Read-out'],
                                ['Read-out Error Rate: ', '{:.3e}'.format(q)],
                                ['T1 constant: ', '{:.2f} ns'.format(T1)],
                                ['T2 constant: ', '{:.2f} ns'.format(T2)],
                                ['Gate Relaxation Time: ', '{:.2f} ns'.format(t)]]
                       
            else:
                print('SimulationError: noise model not available')
                sys.exit()
        else:
            noise_model = none(backend)
            noise_prints = [['Noise Model: ', 'None']]
        
    return noise_model, noise_prints
    
    
    
