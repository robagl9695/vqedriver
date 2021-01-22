#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 13:56:43 2021

@author: rgonzalez
"""

import os

prefix = os.getcwd()

def _parser(filename):
    
    #readfile and separate the extension
    if filename[-4] == '.' :
        extension = filename[-4:]
        filename = filename[:-4]
    else:
        extension = ''
    
    #create temporal input without the comments and blank spaces
    inputfile = open(prefix + '/' + filename + extension, 'r')
    cleanedfile = open(prefix + '/' + filename + '_cleaned' + '.tmp', 'w')
    
    if inputfile.mode == 'r':
        for line in inputfile.readlines():
            if not line.startswith('#') and line != '\n':
                cleanedfile.write(line)
                
    inputfile.close()
    cleanedfile.close()
    
    #read the cleaned file
    
    cleanedfile = open(prefix + '/' + filename + '_cleaned' + '.tmp', 'r')
    
    if cleanedfile.mode == 'r':
        contents = cleanedfile.read()
        
    cleanedfile.close()
    
    #read each block
    
    key = '%'
    key_indexes = []
    
    index = 0
    
    while index < len(contents):
        index = contents.find(key, index)
        if index == -1:
            break
        else:
            key_indexes.append(index)
            
        index += len(key)
    
    blocks = []
    
    for i in range(0, len(key_indexes),1):
        start = key_indexes[i]
        if i == len(key_indexes)-1:
            end = len(contents)
        else:
            end = key_indexes[i+1]-1
        block = contents[start:end]
        
        blocks.append(block)
    
    #remove the tmp file
    
    cleanedfilePath = prefix + '/' + filename + '_cleaned' + '.tmp'
    
    try:
        os.remove(cleanedfilePath)
    except:
        print('OSError: Error while deleting file ' + cleanedfilePath)
        
    return blocks, filename