#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 10:48:38 2021

@author: rgonzalez
"""

import qiskit.aqua.components.optimizers as aqoptim
import sys

optimizer_avail = ['cg']#, 'lbfgsb', 'cobyla', 'nelder-mead', 'pbfgs']

def _optim(blocks):
    optimizer_block = [block for block in blocks if block.startswith('%optimizer')]
    
    if len(optimizer_block) == 0:
        optimizer = aqoptim.CG(maxiter=100,          
                               disp=False,
                               gtol=10**(-6),
                               tol=None,
                               eps=1.4901161193847656e-08)
        optimizer_name = 'Conjugate Gradient'
    else:
        optimizer_block = optimizer_block[0]
        optimizer_opts = optimizer_block.split(' ')
        
        optimizer_method = [opt for opt in optimizer_opts if opt.startswith('method')]
        
        if len(optimizer_method) != 0:
            optimizer_method = optimizer_method[0].split('=')[1].strip('\n')
            if optimizer_method not in optimizer_avail:
                print('OptimizerError: Invalid optimizer selected')
                sys.exit()
            else:
                if optimizer_method == 'cg':
                    maxiter = [opt for opt in optimizer_opts if opt.startswith('maxiter')]
                    if len(maxiter) != 0:
                        maxiter = int(maxiter[0].split('=')[1].strip('\n'))
                    else:
                        maxiter = 100
                        
                    disp = [opt for opt in optimizer_opts if opt.startswith('print')]
                    if len(disp) != 0:
                        disp = disp[0].split('=')[1].strip('\n')
                        if disp == 'true':
                            disp = True
                        elif disp == 'false':
                            disp = False
                        else:
                            print('OptimizerError: Invalid option in ConjugateGradient print option')
                    else:
                        disp = False 
    
                    gtol = [opt for opt in optimizer_opts if opt.startswith('conv')]
                    if len(gtol) != 0:
                        gtol = int(gtol[0].split('=')[1].strip('\n'))
                        gtol = 10**(-gtol)
                    else:
                        gtol = 10**(-8)
                    
                    optimizer = aqoptim.CG(maxiter=maxiter,
                                           disp=disp,
                                           gtol=gtol,
                                           tol=None,
                                           eps=1.4901161193847656e-08)
                    
                    optimizer_name = 'Conjugate Gradient'
        
    return optimizer, optimizer_name