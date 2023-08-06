# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 18:14:29 2016

@author: becker
"""

import numpy as np

#=================================================================#
class IterationCounter(object):
    """
    Simple class for information on iterative solver
    """
    def __init__(self, disp=20, name="", verbose=1):
        self.disp = disp
        self.name = name
        self.verbose = verbose
        self.niter = 0
    def __call__(self, rk=None):
        # if self.disp and self.niter%self.disp==0:
        #     print('iter({}) {:4d}\trk = {}'.format(self.name, self.niter, str(rk)))
        self.niter += 1
    def __del__(self):
        if self.verbose: print('niter ({}) {:4d}'.format(self.name, self.niter))
