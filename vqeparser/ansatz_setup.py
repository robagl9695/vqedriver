#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 13:34:33 2021

@author: rgonzalez
"""

import qiskit.chemistry.components.variational_forms as varforms
import sys
from qiskit.chemistry.components.initial_states import HartreeFock

ansatz_avail = ['uccsd']

def _initial_state_set(num_spinorb,
                       num_part,
                       qubitop_map,
                       qubitop_z2red):
    
    initial_state = HartreeFock(num_orbitals=num_spinorb, 
                                num_particles=num_part, 
                                qubit_mapping=qubitop_map,
                                two_qubit_reduction=qubitop_z2red)
    
    return initial_state

def _ansatz(blocks, 
            num_spinorb, 
            num_part,
            qubitop_map,
            qubitop_z2red,
            num_qubits):
    
    ansatz_block = [block for block in blocks if block.startswith('%ansatz')]
    
    initial_state = _initial_state_set(num_spinorb, num_part, qubitop_map, qubitop_z2red)
    
    #if qubitop_map != 'parity':
    #    num_qubits += 2
    
    if len(ansatz_block) == 0:
        ansatz = varforms.UCCSD(num_orbitals=num_spinorb,
                                num_particles=num_part, 
                                initial_state=initial_state,
                                qubit_mapping=qubitop_map,
                                two_qubit_reduction=qubitop_z2red
                                )
        ansatz_name = 'UCCSD'
    else:
        ansatz_block = ansatz_block[0]
        ansatz_opts = ansatz_block.split(' ')
        
        ansatz_method = [opt for opt in ansatz_opts if opt.startswith('method')]
        
        if len(ansatz_method) != 0:
            ansatz_method = ansatz_method[0].split('=')[1].strip('\n')
            if ansatz_method not in ansatz_avail:
                print('AnsatzError: Invalid variational form selected')
                sys.exit(1)
            else:
                if ansatz_method == 'twolocal':
#                    ansatz = TwoLocal(num_qubits=num_qubits,
#                          rotation_blocks=['ry', 'rz'], 
#                          entanglement_blocks='cz', 
#                          initial_state=initial_state)
                    ansatz_name = 'Two Local Circuit'
                        
    return ansatz, ansatz_name
