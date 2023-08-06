# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 10:34:54 2015

@author: jap93
"""

class Symmetryoperation:
    
    def __init__(self, x, y, z, o1 = None, o2 = None, o3 = None):
        
        self.op = x + "," + y + "," + z
        
        if o1 is not None:
            self.op += "," + o1 + "," + o2 + "," + o3
        
    def get_symmetry_operation(self):
        return self.op
        
    def print_operation(self):
        
        print (self.op)