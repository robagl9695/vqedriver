#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 10:48:38 2021

@author: rgonzalez
"""

import qiskit.aqua.components.optimizers as aqoptim
import sys
import numpy as np

optimizer_avail = ['cg',
                   'slsqp',
                   'l-bfgs-b',
                   'cobyla',
                   'nelder-mead',
                   'p-bfgs',
                   'powell',
                   'spsa',
                   'tnc',
                   'nft',
                   'gsls',
                   'adam',
                   'amsgrad',
                   'aqgd']


def set_cg(optimizer_opts):
    
    maxiter = [opt for opt in optimizer_opts if opt.startswith('maxiter')]
    
    if len(maxiter) != 0:
        maxiter = int(maxiter[0].split('=')[1].strip('\n'))
    else:
        maxiter = 25000
        
    disp = [opt for opt in optimizer_opts if opt.startswith('print')]
    if len(disp) != 0:
        disp = disp[0].split('=')[1].strip('\n')
        if disp == 'true':
            disp = True
        elif disp == 'false':
            disp = False
        else:
            print('OptimizerError: Invalid option in ConjugateGradient print option')
            sys.exit()
    else:
        disp = True 

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
    
    optimizer_prints = [['Maximum Iterations: ', maxiter],
               ['Convergence Tolerance: ', '{:.3e}'.format(gtol)]]

    return optimizer, optimizer_name, optimizer_prints

def set_slsqp(optimizer_opts):
    
    maxiter = [opt for opt in optimizer_opts if opt.startswith('maxiter')]
    
    if len(maxiter) != 0:
        maxiter = int(maxiter[0].split('=')[1].strip('\n'))
    else:
        maxiter = 25000
        
    disp = [opt for opt in optimizer_opts if opt.startswith('print')]
    if len(disp) != 0:
        disp = disp[0].split('=')[1].strip('\n')
        if disp == 'true':
            disp = True
        elif disp == 'false':
            disp = False
        else:
            print('OptimizerError: Invalid option in SLSQP print option')
            sys.exit()
    else:
        disp = True 

    ftol = [opt for opt in optimizer_opts if opt.startswith('conv')]
    if len(ftol) != 0:
        ftol = int(ftol[0].split('=')[1].strip('\n'))
        ftol = 10**(-ftol)
    else:
        ftol = 10**(-8)
    
    optimizer = aqoptim.SLSQP(maxiter=maxiter,
                           disp=disp,
                           ftol=ftol,
                           tol=None,
                           eps=1.4901161193847656e-08)
    
    optimizer_name = 'SLSQP'
    
    optimizer_prints = [['Maximum Iterations: ', maxiter],
               ['Convergence Tolerance: ', '{:.3e}'.format(ftol)]]

    return optimizer, optimizer_name, optimizer_prints

def set_lbfgsb(optimizer_opts):
    
    maxiter = [opt for opt in optimizer_opts if opt.startswith('maxiter')]
    
    if len(maxiter) != 0:
        maxiter = int(maxiter[0].split('=')[1].strip('\n'))
    else:
        maxiter = 25000
        
    maxfun = [opt for opt in optimizer_opts if opt.startswith('maxfun')]
        
    if len(maxfun) != 0:
        maxfun = int(maxfun[0].split('=')[1].strip('\n'))
    else:
        maxfun = 25000
        
   
    optimizer = aqoptim.L_BFGS_B(maxiter=maxiter,
                                 maxfun=maxfun,
                                 factr=10,
                                 iprint=1,
                                 epsilon=1.0e-09)
    
    ftol = 10*np.finfo(float).eps
    
    optimizer_name = 'L-BFGS-B'
    
    optimizer_prints = [['Maximum Iterations: ', maxiter],
                        ['Maximum Function Evaluations: ', maxfun],
               ['Convergence Tolerance: ', '{:.3e}'.format(ftol)]]

    return optimizer, optimizer_name, optimizer_prints

def set_cobyla(optimizer_opts):
    
    maxiter = [opt for opt in optimizer_opts if opt.startswith('maxiter')]
    
    if len(maxiter) != 0:
        maxiter = int(maxiter[0].split('=')[1].strip('\n'))
    else:
        maxiter = 25000
        
    disp = [opt for opt in optimizer_opts if opt.startswith('print')]
    if len(disp) != 0:
        disp = disp[0].split('=')[1].strip('\n')
        if disp == 'true':
            disp = True
        elif disp == 'false':
            disp = False
        else:
            print('OptimizerError: Invalid option in COBYLA print option')
            sys.exit()
    else:
        disp = True 

    gtol = [opt for opt in optimizer_opts if opt.startswith('conv')]
    if len(gtol) != 0:
        gtol = int(gtol[0].split('=')[1].strip('\n'))
        gtol = 10**(-gtol)
    else:
        gtol = 10**(-8)
    
    optimizer = aqoptim.COBYLA(maxiter=maxiter,
                           disp=disp,
                           rhobeg=gtol)
    
    optimizer_name = 'COBYLA'
    
    optimizer_prints = [['Maximum Iterations: ', maxiter]]

    return optimizer, optimizer_name, optimizer_prints

def set_nm(optimizer_opts):
    
    maxiter = [opt for opt in optimizer_opts if opt.startswith('maxiter')]
    
    if len(maxiter) != 0:
        maxiter = int(maxiter[0].split('=')[1].strip('\n'))
    else:
        maxiter = 25000
        
    maxfun = [opt for opt in optimizer_opts if opt.startswith('maxfun')]
        
    if len(maxfun) != 0:
        maxfun = int(maxfun[0].split('=')[1].strip('\n'))
    else:
        maxfun = 25000
        
    gtol = [opt for opt in optimizer_opts if opt.startswith('conv')]
    if len(gtol) != 0:
        gtol = int(gtol[0].split('=')[1].strip('\n'))
        gtol = 10**(-gtol)
    else:
        gtol = 10**(-8)
        
    disp = [opt for opt in optimizer_opts if opt.startswith('print')]
    if len(disp) != 0:
        disp = disp[0].split('=')[1].strip('\n')
        if disp == 'true':
            disp = True
        elif disp == 'false':
            disp = False
        else:
            print('OptimizerError: Invalid option in NelderMead print option')
            sys.exit()
    else:
        disp = True 
        
    adaptive = [opt for opt in optimizer_opts if opt.startswith('adapt')]
    if len(adaptive) != 0:
        adaptive = adaptive[0].split('=')[1].strip('\n')
        if adaptive == 'true':
            adaptive = True
        elif adaptive == 'false':
            adaptive = False
        else:
            print('OptimizerError: Invalid option in Nelder-Mead print option')
            sys.exit()
    else:
        adaptive = False 
        
    optimizer = aqoptim.NELDER_MEAD(maxiter=maxiter,
                                 maxfev=maxfun,
                                 disp=disp,
                                 xatol=gtol,
                                 adaptive=adaptive)
    
    optimizer_name = 'Nelder-Mead'
    
    if adaptive:
        adaptive == 'True'
    else:
        adaptive == 'False'
    
    optimizer_prints = [['Maximum Iterations: ', maxiter],
                        ['Maximum Function Evaluations: ', maxfun],
               ['Convergence Tolerance: ', '{:.3e}'.format(gtol)],
               ['Adaptive Method: ', adaptive]]

    return optimizer, optimizer_name, optimizer_prints

def set_pbfgs(optimizer_opts):
    
    from psutil import cpu_count

    numprocs = cpu_count()
        
    maxfun = [opt for opt in optimizer_opts if opt.startswith('maxfun')]
        
    if len(maxfun) != 0:
        maxfun = int(maxfun[0].split('=')[1].strip('\n'))
    else:
        maxfun = 25000
        
    optimizer = aqoptim.P_BFGS(maxfun=maxfun,
                                 factr=10,
                                 iprint=1,
                                 max_processes=numprocs)
    
    ftol = 10*np.finfo(float).eps
    
    optimizer_name = 'P-BFGS'
    
    optimizer_prints = [['Maximum Function Evaluations: ', maxfun],
               ['Convergence Tolerance: ', '{:.3e}'.format(ftol)]]

    return optimizer, optimizer_name, optimizer_prints

def set_powell(optimizer_opts):
    
    maxiter = [opt for opt in optimizer_opts if opt.startswith('maxiter')]
    
    if len(maxiter) != 0:
        maxiter = int(maxiter[0].split('=')[1].strip('\n'))
    else:
        maxiter = 25000
        
    maxfun = [opt for opt in optimizer_opts if opt.startswith('maxfun')]
        
    if len(maxfun) != 0:
        maxfun = int(maxfun[0].split('=')[1].strip('\n'))
    else:
        maxfun = 25000
        
    gtol = [opt for opt in optimizer_opts if opt.startswith('conv')]
    if len(gtol) != 0:
        gtol = int(gtol[0].split('=')[1].strip('\n'))
        gtol = 10**(-gtol)
    else:
        gtol = 10**(-8)
        
    disp = [opt for opt in optimizer_opts if opt.startswith('print')]
    if len(disp) != 0:
        disp = disp[0].split('=')[1].strip('\n')
        if disp == 'true':
            disp = True
        elif disp == 'false':
            disp = False
        else:
            print('OptimizerError: Invalid option in Powell print option')
            sys.exit()
    else:
        disp = True 
        
    optimizer = aqoptim.POWELL(maxiter=maxiter,
                                 maxfev=maxfun,
                                 disp=disp,
                                 xtol=gtol)
    
    optimizer_name = 'Powell'
    
    optimizer_prints = [['Maximum Iterations: ', maxiter],
                        ['Maximum Function Evaluations: ', maxfun],
               ['Convergence Tolerance: ', '{:.3e}'.format(gtol)]]

    return optimizer, optimizer_name, optimizer_prints

def set_spsa(optimizer_opts):
    
    maxiter = [opt for opt in optimizer_opts if opt.startswith('maxiter')]
    
    if len(maxiter) != 0:
        maxiter = int(maxiter[0].split('=')[1].strip('\n'))
    else:
        maxiter = 25000
          
    optimizer = aqoptim.SPSA(maxiter=maxiter,
                             save_steps=1, 
                             last_avg=1, 
                             c0=0.6283185307179586, 
                             c1=0.1, 
                             c2=0.602, 
                             c3=0.101, 
                             c4=0, 
                             skip_calibration=False)
    
    optimizer_name = 'SPSA'
    
    optimizer_prints = [['Maximum Iterations: ', maxiter]]

    return optimizer, optimizer_name, optimizer_prints

def set_tnc(optimizer_opts):
    
    maxiter = [opt for opt in optimizer_opts if opt.startswith('maxiter')]
    
    if len(maxiter) != 0:
        maxiter = int(maxiter[0].split('=')[1].strip('\n'))
    else:
        maxiter = 25000
        
    disp = [opt for opt in optimizer_opts if opt.startswith('print')]
    if len(disp) != 0:
        disp = disp[0].split('=')[1].strip('\n')
        if disp == 'true':
            disp = True
        elif disp == 'false':
            disp = False
        else:
            print('OptimizerError: Invalid option in Truncated Newton print option')
            sys.exit()
    else:
        disp = True 

    gtol = [opt for opt in optimizer_opts if opt.startswith('conv')]
    if len(gtol) != 0:
        gtol = int(gtol[0].split('=')[1].strip('\n'))
        gtol = 10**(-gtol)
    else:
        gtol = 10**(-8)
    
    optimizer = aqoptim.TNC(maxiter=maxiter,
                           disp=disp,
                           gtol=gtol,
                           accuracy=0,
                           ftol=-1,
                           xtol=-1,
                           eps=1.4901161193847656e-08)
    
    optimizer_name = 'Truncated Newton'
    
    optimizer_prints = [['Maximum Iterations: ', maxiter],
               ['Convergence Tolerance: ', '{:.3e}'.format(gtol)]]

    return optimizer, optimizer_name, optimizer_prints

def set_nft(optimizer_opts):
    
    maxiter = [opt for opt in optimizer_opts if opt.startswith('maxiter')]
    
    if len(maxiter) != 0:
        maxiter = int(maxiter[0].split('=')[1].strip('\n'))
    else:
        maxiter = 25000
        
    maxfun = [opt for opt in optimizer_opts if opt.startswith('maxfun')]
        
    if len(maxfun) != 0:
        maxfun = int(maxfun[0].split('=')[1].strip('\n'))
    else:
        maxfun = 25000
              
    disp = [opt for opt in optimizer_opts if opt.startswith('print')]
    if len(disp) != 0:
        disp = disp[0].split('=')[1].strip('\n')
        if disp == 'true':
            disp = True
        elif disp == 'false':
            disp = False
        else:
            print('OptimizerError: Invalid option in NFT print option')
            sys.exit()
    else:
        disp = True 
        
    optimizer = aqoptim.NFT(maxiter=maxiter,
                                 maxfev=maxfun,
                                 disp=disp,
                                 reset_interval=32)
    
    optimizer_name = 'Nakanishi-Fujii-Todo'
    
    optimizer_prints = [['Maximum Iterations: ', maxiter],
                        ['Maximum Function Evaluations: ', maxfun]]

    return optimizer, optimizer_name, optimizer_prints

def set_gsls(optimizer_opts):
    
    maxiter = [opt for opt in optimizer_opts if opt.startswith('maxiter')]
    
    if len(maxiter) != 0:
        maxiter = int(maxiter[0].split('=')[1].strip('\n'))
    else:
        maxiter = 25000
        
    maxfun = [opt for opt in optimizer_opts if opt.startswith('maxfun')]
        
    if len(maxfun) != 0:
        maxfun = int(maxfun[0].split('=')[1].strip('\n'))
    else:
        maxfun = 25000
              
    disp = [opt for opt in optimizer_opts if opt.startswith('print')]
    if len(disp) != 0:
        disp = disp[0].split('=')[1].strip('\n')
        if disp == 'true':
            disp = True
        elif disp == 'false':
            disp = False
        else:
            print('OptimizerError: Invalid option in NFT print option')
            sys.exit()
    else:
        disp = True 
        
    optimizer = aqoptim.GSLS(maxiter=maxiter,
                                 max_eval=maxfun,
                                 disp=disp,
                                 sampling_radius=1e-06, 
                                 sample_size_factor=1, 
                                 initial_step_size=0.01, 
                                 min_step_size=1e-10,
                                 step_size_multiplier=0.4,
                                 armijo_parameter=0.1,
                                 min_gradient_norm=1e-08,
                                 max_failed_rejection_sampling=50)
    
    optimizer_name = 'Gaussian-Smoothed Line Search'
    
    optimizer_prints = [['Maximum Iterations: ', maxiter],
                        ['Maximum Function Evaluations: ', maxfun]]

    return optimizer, optimizer_name, optimizer_prints

def set_adam(optimizer_opts):
    
    maxiter = [opt for opt in optimizer_opts if opt.startswith('maxiter')]
    
    if len(maxiter) != 0:
        maxiter = int(maxiter[0].split('=')[1].strip('\n'))
    else:
        maxiter = 25000
        
    gtol = [opt for opt in optimizer_opts if opt.startswith('conv')]
    if len(gtol) != 0:
        gtol = int(gtol[0].split('=')[1].strip('\n'))
        gtol = 10**(-gtol)
    else:
        gtol = 10**(-8)
    
    optimizer = aqoptim.ADAM(maxiter=maxiter,
                           tol=gtol,
                           lr=0.001, 
                           beta_1=0.9, 
                           beta_2=0.99, 
                           noise_factor=1e-08, 
                           eps=1e-10, 
                           amsgrad=False, 
                           snapshot_dir=None)
    
    optimizer_name = 'ADAM'
    
    optimizer_prints = [['Maximum Iterations: ', maxiter],
               ['Convergence Tolerance: ', '{:.3e}'.format(gtol)]]

    return optimizer, optimizer_name, optimizer_prints

def set_amsgrad(optimizer_opts):
    
    maxiter = [opt for opt in optimizer_opts if opt.startswith('maxiter')]
    
    if len(maxiter) != 0:
        maxiter = int(maxiter[0].split('=')[1].strip('\n'))
    else:
        maxiter = 25000
        
    gtol = [opt for opt in optimizer_opts if opt.startswith('conv')]
    if len(gtol) != 0:
        gtol = int(gtol[0].split('=')[1].strip('\n'))
        gtol = 10**(-gtol)
    else:
        gtol = 10**(-8)
    
    optimizer = aqoptim.ADAM(maxiter=maxiter,
                           tol=gtol,
                           lr=0.001, 
                           beta_1=0.9, 
                           beta_2=0.99, 
                           noise_factor=1e-08, 
                           eps=1e-10, 
                           amsgrad=True, 
                           snapshot_dir=None)
    
    optimizer_name = 'AMSGRAD'
    
    optimizer_prints = [['Maximum Iterations: ', maxiter],
               ['Convergence Tolerance: ', '{:.3e}'.format(gtol)]]

    return optimizer, optimizer_name, optimizer_prints

def set_aqgd(optimizer_opts):
    
    maxiter = [opt for opt in optimizer_opts if opt.startswith('maxiter')]
    
    if len(maxiter) != 0:
        maxiter = int(maxiter[0].split('=')[1].strip('\n'))
    else:
        maxiter = 25000
        
    disp = [opt for opt in optimizer_opts if opt.startswith('print')]
    if len(disp) != 0:
        disp = disp[0].split('=')[1].strip('\n')
        if disp == 'true':
            disp = True
        elif disp == 'false':
            disp = False
        else:
            print('OptimizerError: Invalid option in AQGD print option')
            sys.exit()
    else:
        disp = True 

    gtol = [opt for opt in optimizer_opts if opt.startswith('conv')]
    if len(gtol) != 0:
        gtol = int(gtol[0].split('=')[1].strip('\n'))
        gtol = 10**(-gtol)
    else:
        gtol = 10**(-8)
    
    optimizer = aqoptim.AQGD(maxiter=maxiter,
                           disp=disp,
                           tol=gtol,
                           eta=1.0,
                           momentum=0.25,
                           param_tol=gtol,
                           averaging=10)
    
    optimizer_name = 'Analytic Quantum Gradient Descent'
    
    optimizer_prints = [['Maximum Iterations: ', maxiter],
               ['Convergence Tolerance: ', '{:.3e}'.format(gtol)]]

    return optimizer, optimizer_name, optimizer_prints

def _optim(blocks):
    optimizer_block = [block for block in blocks if block.startswith('%optimizer')]
    
    if len(optimizer_block) == 0:
        optimizer = aqoptim.CG(maxiter=100,          
                               disp=False,
                               gtol=10**(-8),
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
                    optimizer, optimizer_name, optimizer_prints = set_cg(optimizer_opts)
                elif optimizer_method == 'slsqp':
                    optimizer, optimizer_name, optimizer_prints = set_slsqp(optimizer_opts)
                elif optimizer_method == 'l-bfgs-b':
                    optimizer, optimizer_name, optimizer_prints = set_lbfgsb(optimizer_opts)
                elif optimizer_method == 'cobyla':
                    optimizer, optimizer_name, optimizer_prints = set_cobyla(optimizer_opts)
                elif optimizer_method == 'nelder-mead':
                    optimizer, optimizer_name, optimizer_prints = set_nm(optimizer_opts)
                elif optimizer_method == 'p-bfgs':
                    optimizer, optimizer_name, optimizer_prints = set_pbfgs(optimizer_opts)
                elif optimizer_method == 'powell':
                    optimizer, optimizer_name, optimizer_prints = set_powell(optimizer_opts)
                elif optimizer_method == 'spsa':
                    optimizer, optimizer_name, optimizer_prints = set_spsa(optimizer_opts)
                elif optimizer_method == 'tnc':
                    optimizer, optimizer_name, optimizer_prints = set_tnc(optimizer_opts)
                elif optimizer_method == 'nft':
                    optimizer, optimizer_name, optimizer_prints = set_nft(optimizer_opts)
                elif optimizer_method == 'gsls':
                    optimizer, optimizer_name, optimizer_prints = set_gsls(optimizer_opts)
                elif optimizer_method == 'adam':
                    optimizer, optimizer_name, optimizer_prints = set_adam(optimizer_opts)
                elif optimizer_method == 'amsgrad':
                    optimizer, optimizer_name, optimizer_prints = set_amsgrad(optimizer_opts)
                elif optimizer_method == 'aqgd':
                    optimizer, optimizer_name, optimizer_prints = set_aqgd(optimizer_opts)                    
        
    return optimizer, optimizer_name, optimizer_prints