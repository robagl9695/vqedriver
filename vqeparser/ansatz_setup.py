#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 13:34:33 2021

@author: rgonzalez
"""

import qiskit.chemistry.components.variational_forms as varforms
import sys
from qiskit.chemistry.components.initial_states import HartreeFock

ansatz_avail = ['uccsd', 'chc']

def _initial_state_set(num_spinorb,
                       num_part,
                       qubitop_map,
                       qubitop_z2red):
    
    initial_state = HartreeFock(num_orbitals=num_spinorb, 
                                num_particles=num_part, 
                                qubit_mapping=qubitop_map,
                                two_qubit_reduction=False#qubitop_z2red
                                )
    
    return initial_state

def get_excitations_singles(num_part, num_spinorb, exctype):
    
    ### THIS FUNCTION IS TAKEN FROM THE QISKIT SOURCE CODE ####
    #ref: https://qiskit.org/documentation/_modules/qiskit/chemistry/components/variational_forms/uccsd.html#UCCSD.compute_excitation_lists
    
    num_alpha = num_part[0]
    num_beta = num_part[1]
    
    num_particles = num_alpha + num_beta

    if num_particles < 2:
        raise ValueError('Invalid number of particles {}'.format(num_particles))
    if num_spinorb < 4 or num_spinorb % 2 != 0:
        raise ValueError('Invalid number of orbitals {}'.format(num_spinorb))
    if num_spinorb <= num_particles:
        raise ValueError('No unoccupied orbitals')
        
    # convert the active space for alpha and beta respectively
    beta_index = num_spinorb // 2

    # making lists of indexes of MOs involved in excitations

    active_occ_list_alpha = list(range(0, num_alpha))
    active_occ_list_beta = [i + beta_index for i in range(0, num_beta)]

    active_unocc_list_alpha = list(range(num_alpha, num_spinorb // 2))
    active_unocc_list_beta = [i + beta_index for i in range(num_beta, num_spinorb // 2)]

    single_excitations = []

    # lists of single excitations

    for occ_alpha in active_occ_list_alpha:
        for unocc_alpha in active_unocc_list_alpha:
            single_excitations.append([occ_alpha, unocc_alpha])
    for occ_beta in active_occ_list_beta:
        for unocc_beta in active_unocc_list_beta:
            single_excitations.append([occ_beta, unocc_beta])
            
    double_excitations = []

    # lists of double excitations
    
    for occ_alpha in active_occ_list_alpha:
        for unocc_alpha in active_unocc_list_alpha:
            for occ_beta in active_occ_list_beta:
                for unocc_beta in active_unocc_list_beta:
                    double_excitations.append(
                        [occ_alpha, unocc_alpha, occ_beta, unocc_beta])
                    
    if exctype == 's':
        return single_excitations
    elif exctype == 'd':        
        return double_excitations
    elif exctype == 'sd':
        return single_excitations + double_excitations
    else:
        print('AnsatzError: Invalid excitation type')
        sys.exit()

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
                                excitation_type='sd',
                                two_qubit_reduction=False#qubitop_z2red
                                )
        ansatz_name = 'UCCSD'
    else:
        ansatz_block = ansatz_block[0]
        ansatz_opts = ansatz_block.split(' ')
        
        ansatz_method = [opt for opt in ansatz_opts if opt.startswith('method')]
        
        ansatz_exctype = [opt for opt in ansatz_opts if opt.startswith('exctype')]
        
        if len(ansatz_exctype) == 0:
            ansatz_exctype = 'sd'
        else:
            ansatz_exctype = ansatz_exctype[0].split('=')[1].strip('\n')
            if ansatz_exctype not in ['sd', 's', 'd']:
                print('AnsatzError: Invalid excitation type')
                sys.exit()
        
        if len(ansatz_method) != 0:
            ansatz_method = ansatz_method[0].split('=')[1].strip('\n')
            if ansatz_method not in ansatz_avail:
                print('AnsatzError: Invalid variational form selected')
                sys.exit()
            else:
                if ansatz_method == 'uccsd':
                    ansatz = varforms.UCCSD(num_orbitals=num_spinorb,
                                            num_particles=num_part,
                                            initial_state=initial_state,
                                            qubit_mapping=qubitop_map,
                                            excitation_type=ansatz_exctype,
                                            two_qubit_reduction=False#qubitop_z2red
                                            )
                    ansatz_name = 'UCCSD'
                elif ansatz_method == 'chc':
                    
                    excitations = get_excitations_singles(num_part=num_part, 
                                                          num_spinorb=num_spinorb,
                                                          exctype=ansatz_exctype)
                    ansatz = varforms.CHC(num_qubits=num_qubits,
                                            initial_state=initial_state,
                                            excitations=excitations
                                            )
                    ansatz_name = 'CHC'
        else:
            ansatz = varforms.UCCSD(num_orbitals=num_spinorb,
                                num_particles=num_part, 
                                initial_state=initial_state,
                                qubit_mapping=qubitop_map,
                                excitation_type='sd',
                                two_qubit_reduction=False#qubitop_z2red
                                )
            ansatz_name = 'UCCSD'
                        
    return ansatz, ansatz_name, ansatz_exctype
