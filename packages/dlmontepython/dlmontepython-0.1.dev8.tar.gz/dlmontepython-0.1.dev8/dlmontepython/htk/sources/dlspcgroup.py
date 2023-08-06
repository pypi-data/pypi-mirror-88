# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 19:21:35 2014

@author: John
"""
from dlmontepython.htk.sources.dlsymmetryoperation import Symmetryoperation as sym

class Spcgroup:
    
    def __init__(self):
        
        self.symops = []
        self.name = ' '
        self.number = 0
        self.setting = 0
        
    #def print (_space_group_operations(self):
        
        
    # returns the symmetry operators for a space group
    # the number and setting must be specified
    def get_spacegroup(self, number, setting, name):
        
        if setting < 1 and number < 1:
            
            print ("space group not defined")
            return self.symops
            
        else:
            
            self.number = number
            self.setting = setting
    
        if name == "P1" or number == 1:        
            self.name == "P1"
            self.number = 1
            self.setting = 1
                
            s = sym("x","y","z")
            self.symops.append(s) 
                 
            return self.symops
            
        elif name == "P-1" or number == 2:       
            self.name == "P-1"
            self.number = 2
            self.setting = 1
            
            s = sym("x","y","z")
            self.symops.append(s)
            s = sym("-x","-y","-z")
            self.symops.append(s)
               
            return self.symops
        
        elif name == "P121" or number == 3:
            self.name == "P121"
            self.number = 3
            
            if setting == 2: 
                self.setting = 2
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z")
                self.symops.append(s)
   
            elif setting == 1:
                self.setting = 1
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "y", "-z")
                self.symops.append(s)
                
            else:
                
                print ( "setting not found for this symmetry class")
                
            return self.symops

        elif name == "P1211" or number == 4:
            self.name == "P121"
            self.number = 4
            
            if setting == 2:
                self.setting = 2
                                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z", "0", "0", "1/2")
                self.symops.append(s)
           
            if setting == 1:
                self.setting = 1
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "0", "1/2", "0")
                self.symops.append(s) 
                
            else:
                
                print ( "setting not found for this symmetry class")
                
            return self.symops
            
        elif name == "C121" or name == "A112" or number == 5:
            self.number = 5 

            if name == "A112" or setting == 2: 
                self.name = "A112"
                self.setting = 2
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z")
                self.symops.append(s)
               
            elif name == "C121" or setting == 1: 
                self.name = "C121"
                self.setting = 1
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "0", "0", "0")
                self.symops.append(s)

            else:
                
                print ( "setting not found for this symmetry class")
                
            return self.symops             

        elif name == "P1M1" or name == "P11M" or number == 6:
            self.number = 6
            
            if name == "P11M" or setting == 2:      
                self.name = "P11M"
                self.setting = 2
                
                s = sym("x", "y", "z", "0", "0", "0")
                self.symops.append(s)
                s = sym("x", "y", "-z", "0", "0", "0")
                self.symops.append(s)
                
            elif name == "P1M1" or setting == 1:
                self.name = "P1M1"
                self.setting = 2
                
                s = sym("x", "y", "z", "0", "0", "0")
                self.symops.append(s)
                s = sym("x", "-y", "z", "0", "0", "0")
                self.symops.append(s)  
                
            else:
                
                print ( "setting not found for this symmetry class")
                
            return self.symops
            
        elif name == "P1N1" or name == "P1A1" or name == "P11A" or name == "P11N" or name == "P11B" or name == "P1C1" or number == 7:
            self.number = 7        

            if name == "P1N1" or setting == 2:
                self.name = "P1N1"
                self.setting = 2
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "1/2", "0", "1/2")
                self.symops.append(s)  

            elif name == "P1A1" or setting == 3:
                self.name = "P1A1"
                self.setting = 3
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "1/2", "0", "0")
                self.symops.append(s)

            elif name == "P11A" or setting == 4:
                self.name = "P1A1"
                self.setting = 4
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "1/2", "0", "0")
                self.symops.append(s)               

            elif name == "P11N" or setting == 5:
                self.name = "P11N"
                self.setting = 5
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "1/2", "1/2", "0")
                self.symops.append(s)

            elif name == "P11B" or setting == 6:
                self.name = "P11B"
                self.setting = 6
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "0", "1/2", "0")
                self.symops.append(s)

            elif name == "P1C1" or setting == 1:
                self.name = "P11B"
                self.setting = 1
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "0", "0", "1/2")
                self.symops.append(s)
                
            else:
                
                print ( "setting not found for this symmetry class")
                
            return self.symops
            
        elif name == "C1M1" or name == "A11M" or number == 8:
            self.number = 8
            
            if name == "A11M" or setting == 2:
                self.name = "A11M"
                self.setting = 2
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "0", "0", "0")
                self.symops.append(s)
             
            elif name == "C1M1" or setting == 1:
                self.name = "C1M1"
                self.setting = 1
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "0", "0", "0")
                self.symops.append(s)        
                
            else:
                
                print ( "setting not found for this symmetry class")
                
            return self.symops                

        elif name == "C1C1" or name == "A1N1" or name == "I1A1" or name == "A11A" or name == "B11N" or name == "I11B" or number == 9:
            self.number = 9        

            if name == "C1C1" or setting == 1:
                self.name = "A1N1"
                self.setting = 1
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "0", "0", "1/2")
                self.symops.append(s)

            elif name == "A1N1" or setting == 2:
                self.name = "A1N1"
                self.setting = 2
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "1/2", "0", "1/2")
                self.symops.append(s)

            elif name == "I1A1" or setting == 3:
                self.name = "I1A1"
                self.setting = 3
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "1/2", "0", "0")
                self.symops.append(s)

            elif name == "A11A" or setting == 4:
                self.name = "A11A"
                self.setting = 4
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "1/2", "0", "0")
                self.symops.append(s)

            elif name == "B11N" or setting == 5:
                self.name = "B11N"
                self.setting = 5
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "1/2", "1/2", "0")
                self.symops.append(s)

            elif name == "I11B" or setting == 6:
                self.name = "I11B"
                self.setting = 6
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "0", "1/2", "0")
                self.symops.append(s)
               
            else:
                
                print ( "setting not found for this symmetry class")
                
            return self.symops
            
        elif name == "P12/M1" or name == "P112/M" or number == 10:
            self.number = 10  
            
            if name == "P12/M1" or setting == 1:
                self.name = "P12/M1"
                self.setting = 1
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("-x", "y", "-z")
                self.symops.append(s)
                s = sym("x", "-y", "z")
                self.symops.append(s)                 

            elif name == "P112/M" or setting == 2:
                self.name = "P112/M"
                self.setting = 2
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "y", "-z")
                self.symops.append(s)
                 
            else:
                
                print ( "setting not found for this symmetry class")
                
            return self.symops
            
        elif name == "P121/M1" or name == "P1121/M" or number == 11:
            self.number = 11        
        
            if name == "P121/M1" or setting == 1:
                self.name = "P121/M1"
                self.setting = 1
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "0", "1/2", "0")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "0", "1/2", "0")
                self.symops.append(s)

            elif name == "P1121/M" or setting == 2:
                self.name = "P1121/M"
                self.setting = 2
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z", "0", "0", "1/2")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "0", "0", "1/2")
                self.symops.append(s)
                 
            else:
                
                print ( "setting not found for this symmetry class")
                
            return self.symops

        elif name == "C12/M1" or name == "A112/M" or number == 12:
            self.number = 12
            
            if name == "C12/M1" or setting == 1:
                self.name = "C12/M1"
                self.setting = 1
                
                s = sym("x", "y", "z", "0","0","0")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "0","0","0")
                self.symops.append(s)
                s = sym("-x", "-y", "-z", "0","0","0")
                self.symops.append(s)
                s = sym("x", "-y", "z", "0","0","0")
                self.symops.append(s)               

            elif name == "A112/M" or setting == 2:
                self.name = "A112/M"
                self.setting = 2
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "y", "-z")
                self.symops.append(s)                

            return self.symops


        elif name == "P12/c1" or name == "P12/N1" or name == "P12/A1" or name == "P112/A" or name == "P112/N" or name == "P112/B" or number == 13:
            self.number = 13 
            
            if name == "P12/C1" or setting == 1:
                self.name = "P12/C1"
                self.setting = 1
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "0", "0", "1/2")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "0", "0", "1/2")
                self.symops.append(s)              

            elif name == "P12/N1" or setting == 2:
                self.name = "P12/N1"
                self.setting = 2
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "1/2", "0", "1/2")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "1/2", "0", "1/2")
                self.symops.append(s)

            elif name == "P12/A1" or setting == 3:
                self.name = "P12/A1"
                self.setting = 3
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "1/2", "0", "0")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "1/2", "0", "0")
                self.symops.append(s)

            elif name == "P112/A" or setting == 4:
                self.name = "P112/A"
                self.setting = 4
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z", "1/2", "0", "0")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "1/2", "0", "0")
                self.symops.append(s)

            elif name == "P112/N" or setting == 5:
                self.name = "P112/N"
                self.setting = 5
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z", "1/2", "1/2", "0")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "1/2", "1/2", "0")
                self.symops.append(s)

            elif name == "P112/B" or setting == 6:
                self.name = "P112/B"
                self.setting = 6
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z", "0", "1/2", "0")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "0", "1/2", "0")
                self.symops.append(s)
                 
            else:
                
                print ( "setting not found for this symmetry class")
                
            return self.symops
            
        elif name == "P121/C1" or name == "P121/N1" or name == "P121/A1" or name == "P1121/A" or name == "P1121/N" or name == "P1121/B" or number == 14:
            self.number = 13
            
            if name == "P121/C1" or setting == 1:
                self.name = "P121/C1"
                self.setting = 1
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "0", "1/2", "1/2")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "0", "1/2", "1/2")
                self.symops.append(s)

            elif name == "P121/N1" or setting == 2:
                self.name = "P121/N1"
                self.setting = 2
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "1/2", "1/2", "1/2")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "1/2", "1/2", "1/2")
                self.symops.append(s)

            elif name == "P121/A1" or setting == 3:
                self.name = "P121/A1"
                self.setting = 3
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "1/2", "1/2", "1/2")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "1/2", "1/2", "1/2")
                self.symops.append(s)

            elif name == "P1121/A" or setting == 4:
                self.name = "P1121/A1"
                self.setting = 4
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z", "1/2", "0", "1/2")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "1/2", "0", "1/2")
                self.symops.append(s)

            elif name == "P1121/N" or setting == 5:
                self.name = "P1121/N"
                self.setting = 5
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z", "1/2", "1/2", "1/2")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "1/2", "1/2", "1/2")
                self.symops.append(s)

            elif name == "P1121/B" or setting == 6:
                self.name = "P1121/B"
                self.setting = 6
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z", "0", "1/2", "1/2")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "0", "1/2", "1/2")
                self.symops.append(s)
                 
            else:
                
                print ( "setting not found for this symmetry class")
                
            return self.symops

        elif name == "C12/C1" or name == "A12/N1" or name == "I12/A1" or name == "A112/A" or name == "B112/N" or name == "I112/B" or number == 15:
        
            if name == "C12/C1" or setting == 1:
                self.name = "C12/C1"
                self.setting = 1
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "0", "0", "1/2")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "0", "0", "1/2")
                self.symops.append(s)

            elif name == "A12/N1" or setting == 2:
                self.name = "A12/N1"
                self.setting = 2
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "1/2", "0", "1/2")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "1/2", "0", "1/2")
                self.symops.append(s)

            elif name == "I12/A1" or setting == 3:
                self.name = "I12/A1"
                self.setting = 3
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "1/2", "0", "0")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "-y", "z", "1/2", "0", "0")
                self.symops.append(s)

            elif name == "A112/A" or setting == 4:
                self.name = "A112/A"
                self.setting = 4
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z", "1/2", "0", "0")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "1/2", "0", "0")
                self.symops.append(s)

            elif name == "B112/N" or setting == 5:
                self.name = "B112/N"
                self.setting = 5
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z", "1/2", "1/2", "0")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "1/2", "1/2", "0")
                self.symops.append(s)

            elif name == "I112/B" or setting == 6:
                self.name = "I112/B"
                self.setting = 6
                
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z", "0", "1/2", "0")
                self.symops.append(s)
                s = sym("-x", "-y", "-z")
                self.symops.append(s)
                s = sym("x", "y", "-z", "0", "1/2", "0")
                self.symops.append(s)

            else:
                
                print ( "setting not found for this symmetry class")
                
            return self.symops

        elif number == 16 or name == "P222":
            self.name = "P222"
            self.setting = 1
            self.number = 16
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "y", "-z")
            self.symops.append(s)
            s = sym("-x", "-y", "z")
            self.symops.append(s)
            s = sym("x", "-y", "-z")
            self.symops.append(s)
               
            return self.symops
            
        elif number == 17 or name == "P2221":
            self.name = "P2221"
            self.setting = 1
            self.number = 17
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("-x", "y", "-z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("x", "-y", "-z")
            self.symops.append(s)
                
            return self.symops

        elif number == 18 or name == "P21212":
            self.name = "P21212"
            self.setting = 1
            self.number = 18
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z")
            self.symops.append(s)
            s = sym("-x", "y", "-z", "1/2", "1/2", "0")
            self.symops.append(s)
            s = sym("x", "-y", "-z", "1/2", "1/2", "0")
            self.symops.append(s)
               
            return self.symops

        elif number == 19 or name == "P212121":
            self.name = "P212121"
            self.setting = 1
            self.number = 19
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "y", "-z", "0", "1/2", "1/2")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "1/2", "0", "1/2")
            self.symops.append(s)
            s = sym("x", "-y", "-z", "1/2", "1/2", "0")
            self.symops.append(s)
              
            return self.symops

        elif number == 20 or name == "C2221":
            self.name = "C2221"
            self.setting = 1
            self.number = 20
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("-x", "y", "-z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("x", "-y", "-z", "0", "0", "0")
            self.symops.append(s)
              
            return self.symops

        elif number == 21 or name == "C222":
            self.name = "C222"
            self.setting = 1
            self.number = 21
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "y", "-z", "0", "0", "0")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "-z", "0", "0", "0")
            self.symops.append(s)
              
            return self.symops

        elif number == 22 or name == "F222":
            self.name = "F222"
            self.setting = 1
            self.number = 22
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "y", "-z", "0", "0", "0")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "-z", "0", "0", "0")
            self.symops.append(s)
                
            return self.symops

        elif number == 23 or name == "I222":
            self.name = "I222"
            self.setting = 1
            self.number = 23
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "y", "-z", "0", "0", "0")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "-z", "0", "0", "0")
            self.symops.append(s)
              
            return self.symops

        elif number == 24 or name == "I212121":
            self.name = "I212121"
            self.setting = 1
            self.number = 24
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "y", "-z", "1/2", "0", "0")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "1/2", "0")
            self.symops.append(s)
            s = sym("x", "-y", "-z", "0", "0", "1/2")
            self.symops.append(s)
               
            return self.symops

        elif number == 25 or name == "PMM2":
            self.name = "PMM2"
            self.setting = 1
            self.number = 25
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "0", "0", "0")
            self.symops.append(s)
               
            return self.symops
                
        elif number == 26 or name == "PMC21":
            self.name = "PMC21"
            self.setting = 1
            self.number = 26
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("-x", "y", "z", "0", "0", "1/2")
            self.symops.append(s)
               
            return self.symops

        elif number == 27 or name == "PCC2":
            self.name = "PCC2"
            self.setting = 1
            self.number = 27
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("-x", "y", "z", "0", "0", "1/2")
            self.symops.append(s)
               
            return self.symops

        elif number == 28 or name == "PMA2":
            self.name = "PMA2"
            self.setting = 1
            self.number = 28
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "1/2", "0", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "1/2", "0", "0")
            self.symops.append(s)
              
            return self.symops

        elif number == 29 or name == "PCA21":
            self.name = "PCA21"
            self.setting = 1
            self.number = 29
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("x", "-y", "z", "1/2", "0", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "1/2", "0", "1/2")
            self.symops.append(s)
               
            return self.symops
     
        elif number == 30 or name == "PNC2":
            self.name = "PNC2"
            self.setting = 1
            self.number = 30
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("x", "-y", "z", "0", "1/2", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "0", "1/2", "1/2")
            self.symops.append(s)
               
            return self.symops

        elif number == 31 or name == "PMN21":
            self.name = "PMN21"
            self.setting = 1
            self.number = 31
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("x", "-y", "z", "1/2", "0", "1/2")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "1/2", "0", "1/2")
            self.symops.append(s)
            s = sym("-x", "y", "z", "0", "0", "0")
            self.symops.append(s)
             
            return self.symops

        elif number == 32 or name == "PBA2":
            self.name = "PBA2"
            self.setting = 1
            self.number = 32
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z")
            self.symops.append(s)
            s = sym("x", "-y", "z", "1/2", "1/2", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "1/2", "1/2", "0")
            self.symops.append(s)
               
            return self.symops

        elif number == 33 or name == "PNA21":
            self.name = "PNA21"
            self.setting = 1
            self.number = 33
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("x", "-y", "z", "1/2", "1/2", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "1/2", "1/2", "1/2")
            self.symops.append(s)
                
            return self.symops

        elif number == 34 or name == "PNN2":
            self.name = "PNN2"
            self.setting = 1
            self.number = 34
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "1/2", "1/2", "1/2")
            self.symops.append(s)
            s = sym("-x", "y", "z", "1/2", "1/2", "1/2")
            self.symops.append(s)
                
            return self.symops

        elif number == 35 or name == "CMM2":
            self.name = "CMM2"
            self.setting = 1
            self.number = 35
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "0", "0", "0")
            self.symops.append(s)
                
            return self.symops

        elif number == 36 or name == "CMC21":
            self.name = "CMC21"
            self.setting = 1
            self.number = 36
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("x", "-y", "z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("-x", "y", "z", "0", "0", "0")
            self.symops.append(s)
               
            return self.symops

        elif number == 37 or name == "CCC2":
            self.name = "CMC21"
            self.setting = 1
            self.number = 37
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("-x", "y", "z", "0", "0", "1/2")
            self.symops.append(s)
               
            return self.symops

        elif number == 38 or name == "AMM2":
            self.name = "AMM2"
            self.setting = 1
            self.number = 38
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "0", "0", "0")
            self.symops.append(s)
               
            return self.symops

        elif number == 39 or name == "ABM2":
            self.name = "ABM2"
            self.setting = 1
            self.number = 39
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "0", "1/2", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "0", "1/2", "0")
            self.symops.append(s)
               
            return self.symops

        elif number == 40 or name == "AMA2":
            self.name = "AMA2"
            self.setting = 1
            self.number = 40
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "1/2", "0", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "1/2", "0", "0")
            self.symops.append(s)
               
            return self.symops

        elif number == 41 or name == "ABA2":
            self.name = "ABA2"
            self.setting = 1
            self.number = 41
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "1/2", "1/2", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "1/2", "1/2", "0")
            self.symops.append(s)
                
            return self.symops

        elif number == 42 or name == "FMM2":
            self.name = "FMM2"
            self.setting = 1
            self.number = 42
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "1/2", "1/2", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "1/2", "1/2", "0")
            self.symops.append(s)
              
            return self.symops

        elif number == 43 or name == "FDD2":
            self.name = "FDD2"
            self.setting = 1
            self.number = 43
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "1/4", "1/4", "1/4")
            self.symops.append(s)
            s = sym("-x", "y", "z", "1/4", "1/4", "1/4")
            self.symops.append(s)
        
            return self.symops

        elif number == 44 or name == "IMM2":
            self.name = "IMM2"
            self.setting = 1
            self.number = 44
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "0", "0", "0")
            self.symops.append(s)
          
            return self.symops

        elif number == 45 or name == "Iba2":
            self.name = "IMM2"
            self.setting = 1
            self.number = 45
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("-x", "y", "z", "0", "0", "1/2")
            self.symops.append(s)

            return self.symops

        elif number == 46 or name == "IMA2":
            self.name = "IMA2"
            self.setting = 1
            self.number = 46
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "1/2", "0", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "1/2", "0", "1/2")
            self.symops.append(s)
                
            return self.symops

        elif number == 47 or name == "Pmmm":
            self.name = "PMMM"
            self.setting = 1
            self.number = 47
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("-x", "-y", "-z", "0", "0", "0")
            self.symops.append(s)
            s = sym("-x", "y", "-z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "y", "-z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "-z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("-x", "y", "z", "0", "0", "0")
            self.symops.append(s)

        elif name == "PNNN" or number == 48:

            self.name = "PMMM"
            self.number = 48 
            
            if setting == 1:
                
                self.setting = 1
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "z", "0", "0", "0")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "0", "0", "0")
                self.symops.append(s)
                s = sym("-x", "-y", "-z", "1/2", "1/2", "1/2")
                self.symops.append(s)
                s = sym("x", "-y", "-z", "0", "0", "0")
                self.symops.append(s)
                s = sym("x", "y", "-z", "1/2", "1/2", "1/2")
                self.symops.append(s)
                s = sym("x", "-y", "z", "1/2", "1/2", "1/2")
                self.symops.append(s)
                s = sym("-x", "y", "z", "1/2", "1/2", "1/2")
                self.symops.append(s)
          
            elif setting == 2:
                
                self.setting = 2
                s = sym("x", "y", "z")
                self.symops.append(s)
                s = sym("-x", "-y", "-z", "0", "0", "0")
                self.symops.append(s)
                s = sym("-x", "-y", "z", "1/2", "1/2", "1/2")
                self.symops.append(s)
                s = sym("-x", "y", "-z", "1/2", "0", "1/2")
                self.symops.append(s)
                s = sym("x", "y", "-z", "1/2", "1/2", "0")
                self.symops.append(s)
                s = sym("x", "-y", "z", "1/2", "0", "1/2")
                self.symops.append(s)
                s = sym("x", "-y", "-z", "0", "1/2", "1/2")
                self.symops.append(s)
                s = sym("-x", "y", "z", "0", "1/2", "1/2")
                self.symops.append(s)

            else:
                
                print ( "setting not found for this symmetry class")
                
            return self.symops
            
        elif number == 49 or name == "PCCM":
            self.name = "PCCM"
            self.setting = 1
            self.number = 49
            
            s = sym("x", "y", "z")
            self.symops.append(s)
            s = sym("-x", "-y", "-z", "0", "0", "0")
            self.symops.append(s)
            s = sym("-x", "-y", "z", "0", "0", "0")
            self.symops.append(s)
            s = sym("-x", "y", "-z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("x", "y", "-z", "0", "0", "0")
            self.symops.append(s)
            s = sym("x", "-y", "z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("x", "-y", "-z", "0", "0", "1/2")
            self.symops.append(s)
            s = sym("-x", "y", "z", "1/2", "1/2", "1/2")
            self.symops.append(s)

        elif number == 50 or name == "PBAN":
            self.name = "PBAN"
            self.number = 50   
            
            if setting == 1:
                self.setting = 1
                s = sym("x","y","z","0","0","0") 
                self.symops.append(s)                 
                s = sym("-x","y","-z","0","0","0")
                self.symops.append(s)                
                s = sym("-x","-y","z","0","0","0") 
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","1/2","0")
                self.symops.append(s)

            elif setting == 2:
                self.setting = 2
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)                  
                s = sym("-x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","-y","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","1/2","0")
                self.symops.append(s)

            else:
                
                print ( "setting not found for this symmetry class")
                
            return self.symops
            
        elif number == 51 or name == "PMMA":
            
            self.name = "PMMA"
            self.setting = 1
            self.number = 51
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)                  
            s = sym("-x","-y","z","1/2","0","0")
            self.symops.append(s)              
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)                
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)               
            s = sym("x","-y","-z","1/2","0","0")
            self.symops.append(s)              
            s = sym("x","y","-z","1/2","0","0")
            self.symops.append(s)               
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)                 
            s = sym("-x","y","z","1/2","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 52 or name == "PNNA":
        
            self.name = "PNNA"
            self.setting = 1
            self.number = 52
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)                  
            s = sym("-x","-y","z","1/2","0","0")
            self.symops.append(s)              
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)               
            s = sym("-x","y","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","1/2","0","0")
            self.symops.append(s)               
            s = sym("x","-y","-z","0","1/2","1/2")
            self.symops.append(s)            
            s = sym("x","-y","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","y","z","0","1/2","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 53 or name == "PMNA":
        
            self.name = "PMNA"
            self.setting = 1
            self.number = 53
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)                  
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)               
            s = sym("-x","-y","z","1/2","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","0","1/2")
            self.symops.append(s)            
            s = sym("x","y","-z","1/2","0","1/2")
            self.symops.append(s)             
            s = sym("x","-y","z","1/2","0","1/2")
            self.symops.append(s)             
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)                
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 54 or name == "PCCA":

            self.name = "PCCA"
            self.setting = 1
            self.number = 54

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)                  
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)               
            s = sym("-x","-y","z","1/2","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","1/2","0","0")
            self.symops.append(s)               
            s = sym("x","-y","z","0","0","1/2")
            self.symops.append(s)               
            s = sym("x","-y","-z","1/2","0","1/2")
            self.symops.append(s)            
            s = sym("-x","y","z","1/2","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 55 or name == "PBAM":

            self.name = "PBAM"
            self.setting = 1
            self.number = 55

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)                  
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)               
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)                
            s = sym("-x","y","-z","1/2","1/2","0")
            self.symops.append(s)            
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)                 
            s = sym("x","-y","z","1/2","1/2","0")
            self.symops.append(s)             
            s = sym("x","-y","-z","1/2","1/2","0")
            self.symops.append(s)            
            s = sym("-x","y","z","1/2","1/2","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 56 or name == "PCCN":

            self.name = "PCCN"
            self.setting = 1
            self.number = 56
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)                  
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)               
            s = sym("-x","-y","z","1/2","1/2","0")
            self.symops.append(s)            
            s = sym("-x","y","-z","0","1/2","1/2")
            self.symops.append(s)            
            s = sym("x","y","-z","1/2","1/2","0")
            self.symops.append(s)             
            s = sym("x","-y","z","0","1/2","1/2")
            self.symops.append(s)             
            s = sym("x","-y","-z","1/2","0","1/2")
            self.symops.append(s)            
            s = sym("-x","y","z","1/2","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 57 or name == "PBCM":

            self.name = "PBCM"
            self.setting = 1
            self.number = 57
 
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)                   
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)                
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)               
            s = sym("-x","y","-z","0","1/2","1/2")
            self.symops.append(s)             
            s = sym("x","y","-z","0","0","1/2")
            self.symops.append(s)                
            s = sym("x","-y","z","0","1/2","1/2")
            self.symops.append(s)              
            s = sym("x","-y","-z","0","1/2","0")
            self.symops.append(s)               
            s = sym("-x","y","z","0","1/2","0")
            self.symops.append(s) 
            
            return self.symops

        elif number == 58 or name == "PNNM":

            self.name = "PNNM"
            self.setting = 1
            self.number = 58
 
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)                  
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)               
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)                
            s = sym("-x","y","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)                 
            s = sym("x","-y","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 59 or name == "PMMN":
            
            self.name = "PMMN"
            self.number = 59
        
            if setting == 1:
                self.setting = 1

                s = sym("x","y","z","0","0","0")
                self.symops.append(s)                  
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","-y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","0","0")
                self.symops.append(s)

            elif setting == 2:
                self.setting = 2

                s = sym("x","y","z","0","0","0")
                self.symops.append(s)                 
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","-y","z","0","1/2","0")
                self.symops.append(s)
                s = sym("x","-y","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","0","0")
                self.symops.append(s)
                
            else:
                
                print ( 'wrong setting provided')
                
            return self.symops

        elif number == 60 or name == "PBCN":

            self.name = "PBCN"
            self.setting = 1
            self.number = 60
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 61 or name == "PBCA":

            self.name = "PBCA"
            self.setting = 1
            self.number = 61
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)                  
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","1/2","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","-z","0","1/2","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","1/2","0","1/2")
            self.symops.append(s)
            s = sym("x","-y","z","0","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 62:
            self.number = 62
            
            if setting == 1 or name == "PNMA":
                self.name = "PNMA"
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)                  
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","z","0","1/2","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","1/2","1/2")
                self.symops.append(s)

            elif setting == 2 or name == "PMCN":
                self.name = "PMCN"
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                
            else:
                print ( 'setting not given')
                
            return self.symops

        elif number == 63 or name == "CMCM":

            self.name = "CMCM"
            self.setting = 1
            self.number = 63
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            
            return self.symops

        elif number == 64 or name == "CMCA":

            self.name = "CMCA"
            self.setting = 1
            self.number = 64
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","-y","z","0","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-y","z","0","1/2","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","0","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops
            
        elif number == 65 or name == "CMMM":

            self.name = "CMMM"
            self.setting = 1
            self.number = 65
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops
            
        elif number == 66 or name == "CCCM":

            self.name = "CCCM"
            self.setting = 1
            self.number = 66
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops
            
        elif number == 67 or name == "CMMA":

            self.name = "CMMA"
            self.setting = 1
            self.number = 67
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","1/2","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","1/2","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","1/2","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","1/2","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops
            
        elif number == 68 or name == "CCCA":

            self.name = "CCCA"
            self.number = 68   
            
            if setting == 1:
                
                self.setting = 1
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)                 
                s = sym("-x","y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","y","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","y","z","0","1/2","1/2")
                self.symops.append(s)

            elif setting == 2 or name == "Ccca":
                
                self.setting = 2
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)                  
                s = sym("-x","-y","z","1/2","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("x","-y","-z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","z","0","0","1/2")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","0","1/2")
                self.symops.append(s)
                
            else:
                
                print ( 'could not find symmetry setting')
                
            return self.symops

        elif number == 69 or name == "FMMM":
            
            self.name = "FMMM"
            self.setting = 1
            self.number = 69
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 70:
            self.name = "FDDD"        
            self.number = 70

            if setting == 1:

                self.setting = 1

                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("x","y","-z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-x","y","z","1/4","1/4","1/4")
                self.symops.append(s)

            elif setting == 2:
                
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/4","0","1/4")
                self.symops.append(s)
                s = sym("x","y","-z","1/4","1/4","0")
                self.symops.append(s)
                s = sym("x","-y","z","1/4","0","1/4")
                self.symops.append(s)
                s = sym("x","-y","-z","0","1/4","1/4")
                self.symops.append(s)
                s = sym("-x","y","z","0","1/4","1/4")
                self.symops.append(s)
                
            else:
                
                print ( 'wrong setting given')
                
            return self.symops

        elif number == 71 or name == "IMMM":
            
            self.name = "IMMM"
            self.setting = 1
            self.number = 71
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 72 or name == "IBAM":
            self.name = "IBAM"
            self.setting = 1
            self.number = 72

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 73 or name == "IBCA":
            self.name = "IBCA"
            self.setting = 1
            self.number = 73

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","1/2","0")
            self.symops.append(s)
            s = sym("x","-y","z","1/2","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","0","1/2","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0",0.)
            self.symops.append(s)

        elif number == 74 or name == "IMMA":
            self.name = "IMMA"
            self.setting = 1
            self.number = 74

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","1/2","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","1/2","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","1/2","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","1/2","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 75 or name == "P4":
            self.name = "P4"
            self.setting = 1
            self.number = 75

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 76 or name == "P41":
            self.name = "P41"
            self.setting = 1
            self.number = 76

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","1/4")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","3/4")
            self.symops.append(s)
            
            return self.symops

        elif number == 77 or name == "P42":
            self.name = "P42"
            self.setting = 1
            self.number = 77
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops
           
        elif number == 78 or name == "P43":
            self.name = "P43"
            self.setting = 1
            self.number = 78

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","3/4")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","1/4")
            self.symops.append(s)
            
            return self.symops

        elif number == 79 or name == "I4":
            self.name = "I4"
            self.setting = 1
            self.number = 79

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 80 or name == "I41":
            self.name = "I41"
            self.setting = 1
            self.number = 80

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","1/2","1/4")
            self.symops.append(s)
            s = sym("y","-x","z","0","1/2","1/4")
            self.symops.append(s)
            
            return self.symops

        elif number == 81 or name == "P-4":
            self.name = "P-4"
            self.setting = 1
            self.number = 81

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 82 or name == "I-4":
            self.name = "I-4"
            self.setting = 1
            self.number = 82

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 83 or name == "P4/M":
            self.name = "P4/M"
            self.setting = 1
            self.number = 83

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 84 or name == "P42/M":
            self.name = "P42/M"
            self.setting = 1
            self.number = 84

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 85:
            self.name = " "
            self.number = 85
            
            if setting == 1:
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","0","0")
                self.symops.append(s)
     
            elif setting == 2:
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","0","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("y","-x","z","0","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","1/2","0")
                self.symops.append(s)

            else:
               
               print ( 'setting not found')
               
            return self.symops
   
        elif number == 86:
            self.name = " "
            self.number = 86
            
            if setting == 1:     
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","0","0")
                self.symops.append(s)

            elif setting == 2:
                self.setting = 2

                s = sym("x","y","z","0","0","0")                  
                s = sym("-x","-y","-z","0","0","0")               
                s = sym("-x","-y","z","1/2","1/2","0")           
                s = sym("-y","x","z","0","1/2","1/2")             
                s = sym("x","y","-z","1/2","1/2","0")            
                s = sym("y","-x","-z","0","1/2","1/2")            
                s = sym("y","-x","z","1/2","0","1/2")             
                s = sym("-y","x","-z","1/2","0","1/2")

            else:
               
               print ( 'setting not found')
               
            return self.symops
            
        elif number == 87 or name == "I4/M":
            self.name = "I4/M"
            self.setting = 1
            self.number = 87
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 88:
            self.name = " "
            self.number = 86        
        
            if setting == 1:
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("-y","x","z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("x","y","-z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("y","-x","z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","0","0")
                self.symops.append(s)

            elif setting == 2:
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","z","3/4","1/4","1/4")
                self.symops.append(s)
                s = sym("x","y","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","-z","3/4","1/4","1/4")
                self.symops.append(s)
                s = sym("y","-x","z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","x","-z","1/4","1/4","1/4")
                self.symops.append(s)
                
            else:
               
               print ( 'setting not found')
               
            return self.symops 
            
        elif number == 89 or name == "P422":
            self.name = "P422"
            self.setting = 1
            self.number = 89
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 90 or name == "P4212":
            self.name = "P4212"
            self.setting = 1
            self.number = 90
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","x","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","-x","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 91 or name == "P4122":
            self.name = "P4122"
            self.setting = 1
            self.number = 91
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","1/4")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","3/4")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","3/4")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/4")
            self.symops.append(s)

            return self.symops
            
        elif number == 92 or name == "P41212":
            self.name = "P41212"
            self.setting = 1
            self.number = 92
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","1/2","1/4")
            self.symops.append(s)
            s = sym("-y","x","z","1/2","1/2","1/4")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","3/4")
            self.symops.append(s)
            s = sym("y","-x","z","1/2","1/2","3/4")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops
            
        elif number == 93 or name == "P4222":
            self.name = "P4222"
            self.setting = 1
            self.number = 93
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/2")
            self.symops.append(s)

            return self.symops
            
        elif number == 94 or name == "P42212":
            self.name = "P42212"
            self.setting = 1
            self.number = 94
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 95 or name == "P4322":
            self.name = "P4322"
            self.setting = 1
            self.number = 95
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","3/4")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","1/4")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","1/4")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","3/4")
            self.symops.append(s)

            return self.symops
            
        elif number == 96 or name == "P43212":
            self.name = "P43212"
            self.setting = 1
            self.number = 96
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x","z","1/2","1/2","3/4")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","1/2","3/4")
            self.symops.append(s)
            s = sym("y","-x","z","1/2","1/2","1/4")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","1/4")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 97 or name == "I422":
            self.name = "I422"
            self.setting = 1
            self.number = 97
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 98 or name == "I4122":
            self.name = "I4122"
            self.setting = 1
            self.number = 98
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","1/2","1/4")
            self.symops.append(s)
            s = sym("-y","x","z","0","1/2","1/4")
            self.symops.append(s)
            s = sym("x","-y","-z","0","1/2","1/4")
            self.symops.append(s)
            s = sym("y","-x","z","0","1/2","1/4")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 99 or name == "P4MM":
            self.name = "P4MM"
            self.setting = 1
            self.number = 99
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 100 or name == "P4BM":
            self.name = "P4BM"
            self.setting = 1
            self.number = 100
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","x","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","-x","z","1/2","1/2","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 101 or name == "P42CM":
            self.name = "P42CM"
            self.setting = 1
            self.number = 101
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 102 or name == "P42NM":
            self.name = "P42NM"
            self.setting = 1
            self.number = 102
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-y","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 103 or name == "P4CC":
            self.name = "P4CC"
            self.setting = 1
            self.number = 103
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 104 or name == "P4NC":
            self.name = "P4NC"
            self.setting = 1
            self.number = 104
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","1/2","1/2","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 105 or name == "P42MC":
            self.name = "P42MC"
            self.setting = 1
            self.number = 105
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 106 or name == "P42BC":
            self.name = "P42BC"
            self.setting = 1
            self.number = 106
 
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","-y","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","1/2","1/2","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 107 or name == "I4MM":
            self.name = "I4MM"
            self.setting = 1
            self.number = 107
 
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 108 or name == "I4CM":
            self.name = "I4CM"
            self.setting = 1
            self.number = 108
 
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 109 or name == "I41MD":
            self.name = "I41MD"
            self.setting = 1
            self.number = 109
 
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","1/2","1/4")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","1/2","1/4")
            self.symops.append(s)
            s = sym("y","-x","z","0","1/2","1/4")
            self.symops.append(s)
            s = sym("y","x","z","0","1/2","1/4")
            self.symops.append(s)
            
            return self.symops

        elif number == 110 or name == "I41CD":
            self.name = "I41CD"
            self.setting = 1
            self.number = 110
 
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","1/2","1/4")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","1/2","0","1/4")
            self.symops.append(s)
            s = sym("y","-x","z","0","1/2","1/4")
            self.symops.append(s)
            s = sym("y","x","z","1/2","0","1/4")
            self.symops.append(s)
            
            return self.symops

        elif number == 111 or name == "P-42M":
            self.name = "P-42M"
            self.setting = 1
            self.number = 111
 
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 112 or name == "P-42c":
            self.name = "P-42C"
            self.setting = 1
            self.number = 112
 
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 113 or name == "P-421M":
            self.name = "P-421M"
            self.setting = 1
            self.number = 113
 
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","x","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","-x","z","1/2","1/2","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 114 or name == "P-421C":
            self.name = "P-421C"
            self.setting = 1
            self.number = 114
 
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","1/2","1/2","1/2")
            self.symops.append(s)
            
            return self.symops
         
        elif number == 115 or name == "P-4M2":
            self.name = "P-4M2"
            self.setting = 1
            self.number = 115
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 116 or name == "P-4C2":
            self.name = "P-4C2"
            self.setting = 1
            self.number = 116
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 117 or name == "P-4B2":
            self.name = "P-4B2"
            self.setting = 1
            self.number = 117            

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","x","-z","1/2","1/2","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 118 or name == "P-4N2":
            self.name = "P-4N2"
            self.setting = 1
            self.number = 118            

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","-x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 119 or name == "I-4M2":
            self.name = "I-4M2"
            self.setting = 1
            self.number = 119
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 120 or name == "I-4C2":
            self.name = "I-4C2"
            self.setting = 1
            self.number = 120

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/2")
            self.symops.append(s)

            return self.symops
            
        elif number == 121 or name == "I-42M":
            self.name = "I-42M"
            self.setting = 1
            self.number = 121

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 122 or name == "I-42D":
            self.name = "I-42D"
            self.setting = 1
            self.number = 122

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","1/2","1/4")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","1/2","1/4")
            self.symops.append(s)
            s = sym("y","x","z","0","1/2","1/4")
            self.symops.append(s)
            s = sym("-y","-x","z","0","1/2","1/4")
            self.symops.append(s)
            
            return self.symops

        elif number == 123 or name == "P4/MMM":
            self.name = "P4/MMM"
            self.setting = 1
            self.number = 123

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 124 or name == "P4/MCC":
            self.name = "P4/MCC"
            self.setting = 1
            self.number = 124

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","x","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","x","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","-x","z","1/2","1/2","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 125:
            self.name = " "
            self.number = 125
        
            if setting == 1:    
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","x","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","-x","z","1/2","1/2","0")
                self.symops.append(s)

            elif number == 2:
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","0","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","-y","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","z","0","1/2","0")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","0","0")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("-y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","z","1/2","1/2","0")
                self.symops.append(s)
                
            else:
                
                print ( 'setting not found')
                
            return self.symops
            
        elif number == 126:
            self.name = " "
            self.number = 126
        
            if setting == 1:
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","x","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","z","1/2","1/2","1/2")
                self.symops.append(s)
                
            elif setting == 2:
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","-x","z","0","1/2","0")
                self.symops.append(s)
                s = sym("x","-y","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("-y","x","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","z","0","0","1/2")
                self.symops.append(s)
                
            else:
                
                print ( 'setting not found')
                
            return self.symops
   
#P4/mbm    
        elif number == 127 or name == "P4/MBM":
            self.name = "P4/MBM"
            self.setting = 1
            self.number = 127

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)                
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("x","-y","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","x","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","x","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","-x","z","1/2","1/2","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 128 or name == "P4/MNC":
            self.name = "P4/MNC"
            self.setting = 1
            self.number = 128

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-y","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","1/2","1/2","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 129 or name == "P4/NMM":
            self.name = "P4/NMM"
            self.number = 129
        
            if setting == 1: #"P4/nmm":
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","-y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","-x","z","1/2","1/2","0")
                self.symops.append(s)

            elif setting == 2: #P4/nmm    
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","0","1/2","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("x","-y","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","z","0","1/2","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","0","0")
                self.symops.append(s)
                s = sym("-y","-x","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("y","x","z","0","0","0")
                self.symops.append(s)
 
            else:
                
                print ( 'setting not found')
                
            return self.symops
#P4/ncc    
        elif number == 130 or name == "P4/NCC":
            self.name = "P4/NCC"
            self.number = 130
           
            if setting == 1:
                
                self.setting =1

                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","-y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","z","0","0","1/2")
                self.symops.append(s)
                s = sym("-y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","0","1/2")
                self.symops.append(s)
                s = sym("y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","z","1/2","1/2","1/2")
                self.symops.append(s)
#P4/ncc    
            elif setting == 2:
                self.setting = 2

                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","-y","z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","z","0","1/2","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","-z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("y","x","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","x","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("y","x","z","0","0","1/2")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("-y","-x","z","1/2","1/2","1/2")
                self.symops.append(s)
                
            else:
                
                print ( 'setting not found')
                
            return self.symops   
            
        elif number == 131 or name == "P42/MMC":
            self.name = "P4/MMC"
            self.setting = 1
            self.number = 131

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)            
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 132 or name == "P42/MCM":
            self.name = "P4/MCM"
            self.setting = 1
            self.number = 132
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 133 or name == "P42/NBC":
            self.name = "P4/NBC"
            self.number = 133
                
            if setting == 1:
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","y","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","x","z","0","0","1/2")
                self.symops.append(s)
                s = sym("-y","-x","z","0","0","1/2")
                self.symops.append(s)
     
            elif setting == 2: #P42/nbc   
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","0","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("y","-x","z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","y","z","0","1/2","0")
                self.symops.append(s)
                s = sym("-y","-x","z","0","0","1/2")
                self.symops.append(s)
                s = sym("-y","x","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                
            else:
                
                print ( 'setting not found')
                
            return self.symops

        elif number == 134 or name == "P42/NNM":
            self.name = "P4/NNM"
            self.number = 134
                
            if setting == 1:
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","x","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","z","0","0","0")
                self.symops.append(s)
   
            elif setting == 2: #P42/nnm   
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","-x","z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("y","x","z","1/2","1/2","0")
                self.symops.append(s)

            else:
                
                print ( 'setting not found')
                
            return self.symops
 
        elif number == 135 or name == "P42/MBC":
            self.name = "P42/MBC"
            self.setting = 1
            self.number = 135
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","-x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","x","z","1/2","1/2","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 136 or name == "P42/mnm":
            self.name = "P42/MNM"
            self.setting = 1
            self.number = 136
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-y","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 137 or name == "P42/NMC":
            self.name = "P42/NMC"
            self.number = 137
     
            if setting == 1:
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","z","1/2","1/2","1/2")
                self.symops.append(s)
                
            elif setting == 2: #P42/nmc   
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","z","0","1/2","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","0","0")
                self.symops.append(s)
                s = sym("-y","-x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","x","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("y","x","z","0","0","1/2")
                self.symops.append(s)
                
            else:
                
                print ( 'setting not found')
                
            return self.symops
            
        elif number == 138 or name == "P42/NCM":
            self.name = "P42/NMC"
            self.number = 138
     
            if setting == 1:
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","z","0","0","1/2")
                self.symops.append(s)
                s = sym("-y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","0","1/2")
                self.symops.append(s)
                s = sym("y","x","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","-x","z","1/2","1/2","0")
                self.symops.append(s)
   
            elif setting == 2: #P42/ncm   
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","-z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("y","x","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("-y","-x","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("y","x","z","0","0","0")
                self.symops.append(s)
                
            else:
                
                print ( 'setting not found')
                
            return self.symops
           
        elif number == 139 or name == "I4/MMM":
            self.name = "I4/MMM"
            self.setting = 1
            self.number = 139

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 140 or name == "I4/MCM":
            self.name = "I4/MCM"
            self.setting = 1
            self.number = 140
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 141 or name == "I41/AMD":
            self.name = "I41/AMD"
            self.number = 141
               
            if setting == 1: #I41/amd   
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("-x","y","-z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("y","-x","z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("x","-y","-z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("x","y","-z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("-y","-x","z","0","1/2","1/4")
                self.symops.append(s)
    
            elif setting == 2: #I41/amd   
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/4","3/4","1/4")
                self.symops.append(s)
                s = sym("x","-y","z","0","1/2","0")
                self.symops.append(s)
                s = sym("x","y","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","-z","1/4","3/4","1/4")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","1/4","3/4","1/4")
                self.symops.append(s)
                s = sym("y","-x","z","1/4","1/4","3/4")
                self.symops.append(s)
                s = sym("-y","-x","-z","1/4","1/4","3/4")
                self.symops.append(s)
                s = sym("-x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","z","1/4","3/4","1/4")
                self.symops.append(s)
                s = sym("-y","x","-z","1/4","1/4","3/4")
                self.symops.append(s)
                s = sym("y","x","z","1/4","1/4","3/4")
                self.symops.append(s)
                
            else:
                
                print ( ' setting not found ')
                
            return self.symops

        elif number == 142:
            self.name = "I41/ACD"
            self.number = 142
                       
            if setting == 1: #I41/acd   
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","0","1/4")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("y","-x","z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("x","-y","-z","1/2","0","1/4")
                self.symops.append(s)
                s = sym("x","y","-z","0","1/2","1/4")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","z","0","0","1/2")
                self.symops.append(s)
                s = sym("-y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","0","1/2")
                self.symops.append(s)
                s = sym("y","x","z","1/2","0","1/4")
                self.symops.append(s)
                s = sym("-y","-x","z","1/2","0","1/4")
                self.symops.append(s)
   
            elif setting == 2: #I41/acd   
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/4","3/4","1/4")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","0","0")
                self.symops.append(s)
                s = sym("x","y","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("y","-x","-z","1/4","3/4","1/4")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("y","x","-z","3/4","1/4","1/4")
                self.symops.append(s)
                s = sym("y","-x","z","1/4","1/4","3/4")
                self.symops.append(s)
                s = sym("-y","-x","-z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-x","y","z","0","0","1/2")
                self.symops.append(s)
                s = sym("-y","-x","z","3/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","x","-z","1/4","1/4","3/4")
                self.symops.append(s)
                s = sym("y","x","z","1/4","1/4","1/4")
                self.symops.append(s)
                
            else:
                
                print ( ' setting not found ')
                
            return self.symops
 
        elif number == 143 or name == "P3":
            self.name = "P3"
            self.setting = 1
            self.number = 143
    
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 144 or name == "P31":
            self.name = "P31"
            self.setting = 1
            self.number = 144
    
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","1/3")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","2/3")
            self.symops.append(s)
            
            return self.symops

        elif number == 145 or name == "P32":
            self.name = "P32"
            self.setting = 1
            self.number = 145
    
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","2/3")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","1/3")
            self.symops.append(s)

            return self.symops
            
        elif number == 146 or name == "R3(H)":
            self.name = "R3(H)"
            self.setting = 1
            self.number = 146
    
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 146 or name == "R3(R)":
            self.name = "R3(R)"
            self.setting = 1
            self.number = 146
    
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 147 or name == "P-3":
            self.name = "P-3"
            self.setting = 1
            self.number = 147
    
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 148:
            self.number = 148        
        
            if setting == 1 or name == "R-3(H)":
                self.name = "R-3(H)"
                self.setting = 1

                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x+y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("y","-x+y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x-y","x","-z","0","0","0")
                self.symops.append(s)
     
            elif setting == 2 or name == "R-3(R)":
                self.name = "R-3(R)"
                self.setting = 2

                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("-y","-z","-x","0","0","0")
                self.symops.append(s)

            else:
                
                print ( 'the wrong class name or setting has been provided')
                
            return self.symops
            
        elif number == 149 or name == "P312":
            self.name = "P312"
            self.setting = 1
            self.number = 149
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 150 or name == "P321":
            self.name = "P321"
            self.setting = 1
            self.number = 150
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 151 or name == "P3112":
            self.name = "P3112"
            self.setting = 1
            self.number = 151
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","1/3")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","2/3")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","2/3")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","1/3")
            self.symops.append(s)
            
            return self.symops
            
        elif number == 152 or name == "P3121":
            self.name = "P3121"
            self.setting = 1
            self.number = 152
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","1/3")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","2/3")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","1/3")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","2/3")
            self.symops.append(s)

            return self.symops
            
        elif number == 153 or name == "P312":
            self.name = "P312"
            self.setting = 1
            self.number = 153
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","2/3")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/3")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","1/3")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","2/3")
            self.symops.append(s)

            return self.symops
            
        elif number == 154 or name == "P3221":
            self.name = "P3221"
            self.setting = 1
            self.number = 154
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","2/3")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","1/3")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","2/3")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","1/3")
            self.symops.append(s)
            
            return self.symops
            
        elif number == 155:
            self.number = 155  
            
            if setting == 1 or name == "R32(H)":
                self.name = "R32(H)"
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x-y","z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x+y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-x+y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x-y","-y","-z","0","0","0")
                self.symops.append(s)
   
            elif setting == 2 or name == "R32(R)":
                self.name = "R32(R)"
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","-y","-x","0","0","0")
                self.symops.append(s)
                s = sym("-x","-z","-y","0","0","0")
                self.symops.append(s)
                
            else:
                
                print ( 'class name or setting not found')
                
            return self.symops
 
        elif number == 156 or name == "P3M1":
            self.name = "P3M1"
            self.setting = 1
            self.number = 156
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops
          
        elif number == 157 or name == "P31M":
            self.name = "P31M"
            self.setting = 1
            self.number = 157
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","-y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 158 or name == "P3C1":
            self.name = "P3C1"
            self.setting = 1
            self.number = 158
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 159 or name == "P31C":
            self.name = "P31C"
            self.setting = 1
            self.number = 159
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","-y","z","0","0","1/2")
            
            return self.symops

        elif number == 160:
            self.number = 160
            
            if setting == 1 or name == "R3M(H)":
                self.name = "R3M(H)"
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("-x+y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("x","x-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x+y","y","z","0","0","0")
                self.symops.append(s)

            elif setting == 2 or name == "R3M(R)":
                self.name = "R3M(R)"
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("y","x","z","0","0","0")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("z","y","x","0","0","0")
                self.symops.append(s)
                s = sym("x","z","y","0","0","0")
                self.symops.append(s)
                
            else:
                
                print ( ' setting or name not found')
                
            return self.symops

        elif number == 161:
            self.number = 161
            
            if setting == 1 or name == "R3C(H)":
                self.name = "R3C(H)"
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","z","0","0","1/2")
                self.symops.append(s)
                s = sym("-x+y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("x","x-y","z","0","0","1/2")
                self.symops.append(s)
                s = sym("-x+y","y","z","0","0","1/2")
                self.symops.append(s)

            elif setting == 2 or name == "R3C(R)":
                self.name = "R3C(R)"
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("z","y","x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","z","y","1/2","1/2","1/2")
                self.symops.append(s)
                
            else:
                
                print ( ' setting or name not found')
                
            return self.symops
            
        elif number == 162 or name == "P-31M":
            self.name = "P-31M"
            self.setting = 1
            self.number = 162
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","-y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 163 or name == "P-31C":
            self.name = "P-31C"
            self.setting = 1
            self.number = 163
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","-y","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 164 or name == "P-3M1":
            self.name = "P-3M1"
            self.setting = 1
            self.number = 164
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 165 or name == "P-3C1":
            self.name = "P-3C1"
            self.setting = 1
            self.number = 165
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","1/2")
            self.symops.append(s)

            return self.symops
            
        elif number == 166:
            self.number = 166 
            
            if setting == 1 or name == "R-3M(H)":
                self.name = "R-3M(H)"
                self.setting = 1

                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x-y","z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x+y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-x+y","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","-x+y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x-y","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("x-y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","x-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x+y","y","z","0","0","0")
                self.symops.append(s)
     
            elif setting == 2 or name == "R-3M(R)":
                self.name = "R-3M(R)"
                self.setting = 2

                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","-y","-x","0","0","0")
                self.symops.append(s)
                s = sym("-z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("-x","-z","-y","0","0","0")
                self.symops.append(s)
                s = sym("y","x","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","-z","-x","0","0","0")
                self.symops.append(s)
                s = sym("z","y","x","0","0","0")
                self.symops.append(s)
                s = sym("x","z","y","0","0","0")
                self.symops.append(s)
                
            else:
                
                print ( 'setting or class name not found')
                
            return self.symops

        elif number == 167:
            self.number = 167        
        
            if setting == 1 or name == "R-3C(H)":
                self.name = "R-3C(H)"
                self.setting = 1

                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","x-y","z","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x+y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-x+y","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("y","-x+y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x-y","-y","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("-y","-x","z","0","0","1/2")
                self.symops.append(s)
                s = sym("x-y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","x-y","z","0","0","1/2")
                self.symops.append(s)
                s = sym("-x+y","y","z","0","0","1/2")
                self.symops.append(s)

            elif setting == 2 or name == "R-3C(R)":
                self.name = "R-3C(R)"
                self.setting = 2

                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","-y","-x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("-x","-z","-y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-z","-x","0","0","0")
                self.symops.append(s)
                s = sym("z","y","x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","z","y","1/2","1/2","1/2")
                self.symops.append(s)
                
            else:
                
                print ( 'setting or class name not found')
                
            return self.symops

        elif number == 168 or name == "P6":
            self.name = "P6"
            self.setting = 1
            self.number = 168
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 169 or name == "P61":
            self.name = "P61"
            self.setting = 1
            self.number = 169

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","1/3")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","2/3")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","5/6")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","1/6")
            self.symops.append(s)

            return self.symops
            
        elif number == 170 or name == "P65":
            self.name = "P65"
            self.setting = 1
            self.number = 170

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","2/3")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","1/3")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","1/6")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","5/6")
            self.symops.append(s)

            return self.symops
            
        elif number == 171 or name == "P62":
            self.name = "P62"
            self.setting = 1
            self.number = 171

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","2/3")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","1/3")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","2/3")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","1/3")
            self.symops.append(s)
            
            return self.symops

        elif number == 172 or name == "P64":
            self.name = "P64"
            self.setting = 1
            self.number = 172

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","1/3")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","2/3")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","1/3")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","2/3")
            self.symops.append(s)
            
            return self.symops

        elif number == 173 or name == "P63":
            self.name = "P63"
            self.setting = 1
            self.number = 173

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 174 or name == "P-6":
            self.name = "P-6"
            self.setting = 1
            self.number = 174

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 175 or name == "P6/M":
            self.name = "P6/M"
            self.setting = 1
            self.number = 175

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 176 or name == "P63/M":
            self.name = "P63/M"
            self.setting = 1
            self.number = 176

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","-x","-z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 177 or name == "P622":
            self.name = "P622"
            self.setting = 1
            self.number = 177

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 178 or name == "P6122":
            self.name = "P6122"
            self.setting = 1
            self.number = 178

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","1/3")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","1/3")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","2/3")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","5/6")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","2/3")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","5/6")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","1/6")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","1/6")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 179 or name == "P6522":
            self.name = "P6522"
            self.setting = 1
            self.number = 179

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","2/3")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","2/3")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","1/3")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","1/6")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","1/3")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/6")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","5/6")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","5/6")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 180 or name == "P6222":
            self.name = "P6222"
            self.setting = 1
            self.number = 180

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","2/3")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","2/3")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","1/3")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","2/3")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","1/3")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","2/3")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","1/3")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","1/3")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 181 or name == "P6422":
            self.name = "P6422"
            self.setting = 1
            self.number = 181

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","1/3")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","1/3")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","2/3")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","1/3")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","2/3")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/3")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","2/3")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","2/3")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 182 or name == "P6322":
            self.name = "P6322"
            self.setting = 1
            self.number = 182

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 183 or name == "P6MM":
            self.name = "P6MM"
            self.setting = 1
            self.number = 183

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","-y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 184 or name == "P6CC":
            self.name = "P6CC"
            self.setting = 1
            self.number = 184

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","-y","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 185 or name == "P63CM":
            self.name = "P63CM"
            self.setting = 1
            self.number = 185

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-x+y","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","-y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 186 or name == "P63MC":
            self.name = "P63MC"
            self.setting = 1
            self.number = 186

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-x+y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","-y","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 187 or name == "P-6M2":
            self.name = "P-6M2"
            self.setting = 1
            self.number = 187

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 188 or name == "P-6C2":
            self.name = "P-6C2"
            self.setting = 1
            self.number = 188

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 189 or name == "P-62M":
            self.name = "P-62M"
            self.setting = 1
            self.number = 189

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","-y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 190 or name == "P-62C":
            self.name = "P-62C"
            self.setting = 1
            self.number = 190

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-x+y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","-y","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 191 or name == "P6/MMM":
            self.name = "P6/MMM"
            self.setting = 1
            self.number = 191

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","-y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 192 or name == "P6/MCC":
            self.name = "P6/MCC"
            self.setting = 1
            self.number = 192

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-x+y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","-y","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 193 or name == "P63/MCM":
            self.name = "P63/MCM"
            self.setting = 1
            self.number = 193

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-x+y","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","-y","z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 194 or name == "P63/MMC":
            self.name = "P63/MMC"
            self.setting = 1
            self.number = 194

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-x+y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x-y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","x-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","x-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("x","x-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("y","x","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x+y","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x+y","-x","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-x","-x+y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("x-y","-y","z","0","0","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 195 or name == "P23":
            self.name = "P23"
            self.setting = 1
            self.number = 195

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 196 or name == "F23":
            self.name = "F23"
            self.setting = 1
            self.number = 196

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 197 or name == "I23":
            self.name = "I23"
            self.setting = 1
            self.number = 197

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 198 or name == "P213":
            self.name = "P213"
            self.setting = 1
            self.number = 198

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","1/2","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","-z","0","1/2","1/2")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-z","-x","y","1/2","0","1/2")
            self.symops.append(s)
            s = sym("-z","x","-y","0","1/2","1/2")
            self.symops.append(s)
            s = sym("z","-x","-y","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","1/2","0","1/2")
            self.symops.append(s)
            s = sym("-y","z","-x","0","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-z","-x","1/2","1/2","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 199 or name == "I213":
            self.name = "I213"
            self.setting = 1
            self.number = 199

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","1/2","0")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-z","-x","y","0","1/2","0")
            self.symops.append(s)
            s = sym("-z","x","-y","1/2","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","1/2")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","1/2","0")
            self.symops.append(s)
            s = sym("-y","z","-x","1/2","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","1/2")
            self.symops.append(s)
            
            return self.symops
         
        elif number == 200 or name == "PM-3":
            self.name = "PM-3"
            self.setting = 1
            self.number = 200

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","x","0","0","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 201: 
            self.name = "PN-3"
            self.number = 201
            
            if setting == 1: # "Pn-3:
                self.setting = 1

                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","0","0")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-z","-x","y","0","0","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","x","-y","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","-x","-y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-z","x","0","0","0")
                self.symops.append(s)
                s = sym("z","x","-y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","z","-x","0","0","0")
                self.symops.append(s)
                s = sym("z","-x","y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-z","-x","0","0","0")
                self.symops.append(s)
                s = sym("-z","x","y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-z","-x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","z","-x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-z","x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","z","x","1/2","1/2","1/2")
                self.symops.append(s)
    
            elif setting == 2: #Pn-3      
                self.setting = 2

                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","-x","y","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-z","x","-y","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("z","-x","-y","0","1/2","1/2")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-z","x","1/2","1/2","0")
                self.symops.append(s)
                s = sym("z","x","-y","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","z","-x","1/2","0","1/2")
                self.symops.append(s)
                s = sym("z","-x","y","1/2","0","1/2")
                self.symops.append(s)
                s = sym("y","-z","-x","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","x","y","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-z","-x","0","0","0")
                self.symops.append(s)
                s = sym("y","z","-x","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","-z","x","1/2","0","1/2")
                self.symops.append(s)
                s = sym("-y","z","x","0","1/2","1/2")
                self.symops.append(s)
                
            else:
                
                print ( 'setting not found')
                
            return self.symops
 
        elif number == 202 or name == "FM-3":
            self.name = "FM-3"
            self.setting = 1
            self.number = 202

            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","x","0","0","0")
            self.symops.append(s)
            
            return self.symops
            
        if number == 203:
            self.name = "FD-3"
            self.number = 203
         
            if setting == 1: #Fd-3      
                self.setting = 1
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","0","0")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-z","-x","y","0","0","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","x","-y","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","-x","-y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-x","y","z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","-z","x","0","0","0")
                self.symops.append(s)
                s = sym("z","x","-y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","z","-x","0","0","0")
                self.symops.append(s)
                s = sym("z","-x","y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("y","-z","-x","0","0","0")
                self.symops.append(s)
                s = sym("-z","x","y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","-z","-x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("y","z","-x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("y","-z","x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","z","x","1/4","1/4","1/4")
                self.symops.append(s)
   
            elif setting == 2: #Fd-3      
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/4","0","1/4")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","-z","0","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","-x","y","1/4","1/4","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-z","x","-y","1/4","0","1/4")
                self.symops.append(s)
                s = sym("x","-y","z","1/4","0","1/4")
                self.symops.append(s)
                s = sym("z","-x","-y","0","1/4","1/4")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","-z","x","1/4","1/4","0")
                self.symops.append(s)
                s = sym("z","x","-y","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-y","z","-x","1/4","0","1/4")
                self.symops.append(s)
                s = sym("z","-x","y","1/4","0","1/4")
                self.symops.append(s)
                s = sym("y","-z","-x","0","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","x","y","0","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","-z","-x","0","0","0")
                self.symops.append(s)
                s = sym("y","z","-x","1/4","1/4","0")
                self.symops.append(s)
                s = sym("y","-z","x","1/4","0","1/4")
                self.symops.append(s)
                s = sym("-y","z","x","0","1/4","1/4")
                self.symops.append(s)
                
            else:
                
                print ( 'setting not found')
                
            return self.symops
  
        elif number == 204 or name == "IM-3":
            self.name = "IM-3"
            self.setting = 1
            self.number = 204
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)                
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","x","0","0","0")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 205 or name == "PA-3":
            self.name = "PA-3"
            self.setting = 1
            self.number = 205
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","1/2","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","-z","0","1/2","1/2")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-z","-x","y","1/2","0","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","1/2","0","1/2")
            self.symops.append(s)
            s = sym("-z","x","-y","0","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-y","z","0","1/2","1/2")
            self.symops.append(s)
            s = sym("z","-x","-y","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","-z","x","1/2","0","1/2")
            self.symops.append(s)
            s = sym("z","x","-y","1/2","0","1/2")
            self.symops.append(s)
            s = sym("-y","z","-x","0","1/2","1/2")
            self.symops.append(s)
            s = sym("z","-x","y","0","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-z","-x","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-z","x","y","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("y","z","-x","1/2","0","1/2")
            self.symops.append(s)
            s = sym("y","-z","x","0","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","z","x","1/2","1/2","0")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 206 or name == "IA-3":
            self.name = "IA-3"
            self.setting = 1
            self.number = 206
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","1/2","0")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-z","-x","y","0","1/2","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","1/2","0")
            self.symops.append(s)
            s = sym("-z","x","-y","1/2","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","1/2","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","1/2")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-z","x","0","1/2","0")
            self.symops.append(s)
            s = sym("z","x","-y","0","1/2","0")
            self.symops.append(s)
            s = sym("-y","z","-x","1/2","0","0")
            self.symops.append(s)
            s = sym("z","-x","y","1/2","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","1/2")
            self.symops.append(s)
            s = sym("-z","x","y","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("y","z","-x","0","1/2","0")
            self.symops.append(s)
            s = sym("y","-z","x","1/2","0","0")
            self.symops.append(s)
            s = sym("-y","z","x","0","0","1/2")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 207 or name == "P432":
            self.name = "P432"
            self.setting = 1
            self.number = 207
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","x","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","z","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","x","0","0","0")
            self.symops.append(s)
            s = sym("-x","-z","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","-x","0","0","0")
            self.symops.append(s)
            s = sym("-x","z","y","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","-x","0","0","0")
            self.symops.append(s)
            s = sym("x","-z","y","0","0","0")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 208 or name == "P4232":
            self.name = "P4232"
            self.setting = 1
            self.number = 208
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","z","-y","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","-z","-y","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","-x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","z","y","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","-x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-z","y","1/2","1/2","1/2")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 209 or name == "F432":
            self.name = "F432"
            self.setting = 1
            self.number = 209
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","x","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","z","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","x","0","0","0")
            self.symops.append(s)
            s = sym("-x","-z","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","-x","0","0","0")
            self.symops.append(s)
            s = sym("-x","z","y","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","-x","0","0","0")
            self.symops.append(s)
            s = sym("x","-z","y","0","0","0")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 210 or name == "F4132":
            self.name = "F4132"
            self.setting = 1
            self.number = 210
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","x","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("y","-x","z","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("x","z","-y","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","x","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-x","-z","-y","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","-x","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-x","z","y","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","-x","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("x","-z","y","1/4","1/4","1/4")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 211 or name == "I432":
            self.name = "I432"
            self.setting = 1
            self.number = 211
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","x","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","z","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","x","0","0","0")
            self.symops.append(s)
            s = sym("-x","-z","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","-x","0","0","0")
            self.symops.append(s)
            s = sym("-x","z","y","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","-x","0","0","0")
            self.symops.append(s)
            s = sym("x","-z","y","0","0","0")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 212 or name == "P4332":
            self.name = "P4332"
            self.setting = 1
            self.number = 212
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","1/2","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","-z","0","1/2","1/2")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","1/4","3/4","3/4")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-z","-x","y","1/2","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","-z","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-z","x","-y","0","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","x","z","3/4","1/4","3/4")
            self.symops.append(s)
            s = sym("z","-x","-y","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","x","3/4","1/4","3/4")
            self.symops.append(s)
            s = sym("y","-x","z","3/4","3/4","1/4")
            self.symops.append(s)
            s = sym("x","z","-y","1/4","3/4","3/4")
            self.symops.append(s)
            s = sym("-y","-z","x","1/2","0","1/2")
            self.symops.append(s)
            s = sym("z","-y","x","3/4","3/4","1/4")
            self.symops.append(s)
            s = sym("-x","-z","-y","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-y","z","-x","0","1/2","1/2")
            self.symops.append(s)
            s = sym("z","y","-x","1/4","3/4","3/4")
            self.symops.append(s)
            s = sym("-x","z","y","3/4","1/4","3/4")
            self.symops.append(s)
            s = sym("y","-z","-x","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-z","-y","-x","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("x","-z","y","3/4","3/4","1/4")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 213 or name == "P4132":
            self.name = "P4132"
            self.setting = 1
            self.number = 213
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","1/2","0","1/2")
            self.symops.append(s)
            s = sym("-x","y","-z","0","1/2","1/2")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("x","-y","-z","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-z","-x","y","1/2","0","1/2")
            self.symops.append(s)
            s = sym("-y","-x","-z","3/4","3/4","3/4")
            self.symops.append(s)
            s = sym("-z","x","-y","0","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","x","z","1/4","3/4","1/4")
            self.symops.append(s)
            s = sym("z","-x","-y","1/2","1/2","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","x","1/4","3/4","1/4")
            self.symops.append(s)
            s = sym("y","-x","z","1/4","1/4","3/4")
            self.symops.append(s)
            s = sym("x","z","-y","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-y","-z","x","1/2","0","1/2")
            self.symops.append(s)
            s = sym("z","-y","x","1/4","1/4","3/4")
            self.symops.append(s)
            s = sym("-x","-z","-y","3/4","3/4","3/4")
            self.symops.append(s)
            s = sym("-y","z","-x","0","1/2","1/2")
            self.symops.append(s)
            s = sym("z","y","-x","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-x","z","y","1/4","3/4","1/4")
            self.symops.append(s)
            s = sym("y","-z","-x","1/2","1/2","0")
            self.symops.append(s)
            s = sym("-z","-y","-x","3/4","3/4","3/4")
            self.symops.append(s)
            s = sym("x","-z","y","1/4","1/4","3/4")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 214 or name == "I4132":
            self.name = "I4132"
            self.setting = 1
            self.number = 214
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","1/2","0")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-z","-x","y","0","1/2","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-z","x","-y","1/2","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","1/4","3/4","1/4")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","1/2")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","x","1/4","3/4","1/4")
            self.symops.append(s)
            s = sym("y","-x","z","1/4","1/4","3/4")
            self.symops.append(s)
            s = sym("x","z","-y","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-y","-z","x","0","1/2","0")
            self.symops.append(s)
            s = sym("z","-y","x","1/4","1/4","3/4")
            self.symops.append(s)
            s = sym("-x","-z","-y","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-y","z","-x","1/2","0","0")
            self.symops.append(s)
            s = sym("z","y","-x","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-x","z","y","1/4","3/4","1/4")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","1/2")
            self.symops.append(s)
            s = sym("-z","-y","-x","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("x","-z","y","1/4","1/4","3/4")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 215 or name == "P-43M":
            self.name = "P-43M"
            self.setting = 1
            self.number = 215
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","x","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","z","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","x","0","0","0")
            self.symops.append(s)
            s = sym("-x","-z","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","-x","0","0","0")
            self.symops.append(s)
            s = sym("-x","z","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","-x","0","0","0")
            self.symops.append(s)
            s = sym("x","-z","-y","0","0","0")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 216 or name == "F-43M":
            self.name = "F-43M"
            self.setting = 1
            self.number = 216
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","x","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","z","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","x","0","0","0")
            self.symops.append(s)
            s = sym("-x","-z","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","-x","0","0","0")
            self.symops.append(s)
            s = sym("-x","z","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","-x","0","0","0")
            self.symops.append(s)
            s = sym("x","-z","-y","0","0","0")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 217 or name == "I-43M":
            self.name = "I-43M"
            self.setting = 1
            self.number = 217
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","x","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","z","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","x","0","0","0")
            self.symops.append(s)
            s = sym("-x","-z","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","-x","0","0","0")
            self.symops.append(s)
            s = sym("-x","z","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","-x","0","0","0")
            self.symops.append(s)
            s = sym("x","-z","-y","0","0","0")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 218 or name == "P-43N":
            self.name = "P-43N"
            self.setting = 1
            self.number = 218
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","z","y","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","-z","y","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","-x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","z","-y","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","-x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-z","-y","1/2","1/2","1/2")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 219 or name == "F-43C":
            self.name = "F-43C"
            self.setting = 1
            self.number = 219
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","1/2","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","1/2","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","1/2","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","x","0","1/2","0")
            self.symops.append(s)
            s = sym("y","-x","-z","1/2","0","0")
            self.symops.append(s)
            s = sym("x","z","y","1/2","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","x","0","1/2","0")
            self.symops.append(s)
            s = sym("-x","-z","y","1/2","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","-x","0","1/2","0")
            self.symops.append(s)
            s = sym("-x","z","-y","1/2","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","-x","0","1/2","0")
            self.symops.append(s)
            s = sym("x","-z","-y","1/2","0","0")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 220 or name == "I-43D":
            self.name = "I-43D"
            self.setting = 1
            self.number = 220
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","1/2","0")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-z","-x","y","0","1/2","0")
            self.symops.append(s)
            s = sym("-y","-x","z","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-z","x","-y","1/2","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","1/4","1/4","3/4")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","1/2")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","x","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("y","-x","-z","1/4","3/4","1/4")
            self.symops.append(s)
            s = sym("x","z","y","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-y","-z","x","0","1/2","0")
            self.symops.append(s)
            s = sym("-z","-y","x","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-x","-z","y","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-y","z","-x","1/2","0","0")
            self.symops.append(s)
            s = sym("-z","y","-x","1/4","1/4","3/4")
            self.symops.append(s)
            s = sym("-x","z","-y","1/4","1/4","3/4")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","1/2")
            self.symops.append(s)
            s = sym("z","-y","-x","1/4","3/4","1/4")
            self.symops.append(s)
            s = sym("x","-z","-y","1/4","3/4","1/4")
            self.symops.append(s)
            
            return self.symops
 
        elif number == 221 or name == "PM-3M":
            self.name = "PM-3M"
            self.setting = 1
            self.number = 221
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","z","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","x","0","0","0")
            self.symops.append(s)
            s = sym("z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-x","-z","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-x","z","y","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("x","-z","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","-x","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-z","y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","-x","0","0","0")
            self.symops.append(s)
            s = sym("x","z","y","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","x","0","0","0")
            self.symops.append(s)
            s = sym("x","-z","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","x","0","0","0")
            self.symops.append(s)
            s = sym("-x","z","-y","0","0","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 222 or name == "PN-3N":
            self.name = "PN-3N"
            self.number = 222
          
            if setting == 1: #"Pn-3n":
                self.setting = 1
      
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","0","0")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-z","-x","y","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","x","-y","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","y","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","-x","-y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("x","z","-y","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-z","x","0","0","0")
                self.symops.append(s)
                s = sym("z","-y","x","0","0","0")
                self.symops.append(s)
                s = sym("z","x","-y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","-z","-y","0","0","0")
                self.symops.append(s)
                s = sym("y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","z","-x","0","0","0")
                self.symops.append(s)
                s = sym("z","y","-x","0","0","0")
                self.symops.append(s)
                s = sym("z","-x","y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","z","y","0","0","0")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-z","-x","0","0","0")
                self.symops.append(s)
                s = sym("-z","-y","-x","0","0","0")
                self.symops.append(s)
                s = sym("-z","x","y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-z","y","0","0","0")
                self.symops.append(s)
                s = sym("-y","-z","-x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("z","-y","-x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","x","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","-z","y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","z","-x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","y","-x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","z","y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-z","x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","-y","x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-z","-y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","z","x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("z","y","x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","z","-y","1/2","1/2","1/2")
                self.symops.append(s)

            elif setting == 2: #Pn-3n     
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","-x","y","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-z","x","-y","1/2","0","1/2")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","0","0")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("z","-x","-y","0","1/2","1/2")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","y","x","1/2","0","0")
                self.symops.append(s)
                s = sym("-z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("y","-x","z","0","1/2","0")
                self.symops.append(s)
                s = sym("x","z","-y","0","0","1/2")
                self.symops.append(s)
                s = sym("-y","-x","z","0","0","1/2")
                self.symops.append(s)
                s = sym("-x","y","z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-z","x","1/2","1/2","0")
                self.symops.append(s)
                s = sym("z","-y","x","0","1/2","0")
                self.symops.append(s)
                s = sym("z","x","-y","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","-z","-y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","z","-x","1/2","0","1/2")
                self.symops.append(s)
                s = sym("z","y","-x","0","0","1/2")
                self.symops.append(s)
                s = sym("z","-x","y","1/2","0","1/2")
                self.symops.append(s)
                s = sym("-x","z","y","1/2","0","0")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("y","-z","-x","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","-y","-x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","x","y","0","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-z","y","0","1/2","0")
                self.symops.append(s)
                s = sym("-y","-z","-x","0","0","0")
                self.symops.append(s)
                s = sym("z","-y","-x","1/2","0","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","1/2","0")
                self.symops.append(s)
                s = sym("-x","-z","y","0","0","1/2")
                self.symops.append(s)
                s = sym("y","z","-x","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-z","y","-x","0","1/2","0")
                self.symops.append(s)
                s = sym("x","z","y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-z","x","1/2","0","1/2")
                self.symops.append(s)
                s = sym("-z","-y","x","0","0","1/2")
                self.symops.append(s)
                s = sym("x","-z","-y","1/2","0","0")
                self.symops.append(s)
                s = sym("-y","z","x","0","1/2","1/2")
                self.symops.append(s)
                s = sym("z","y","x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","z","-y","0","1/2","0")
                self.symops.append(s)
                
            else:
                
                print ( 'setting not found')
                
            return self.symops
 
        elif number == 223 or name == "PM-3N":
            self.name = "PM-3N"
            self.setting = 1
            self.number = 223
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","z","-y","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","-x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-x","-z","-y","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","x","z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","-x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-x","z","y","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","-x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("x","-z","y","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","-x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","x","-z","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","-z","y","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","-x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","z","y","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("x","-z","-y","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","x","1/2","1/2","1/2")
            self.symops.append(s)
            s = sym("-x","z","-y","1/2","1/2","1/2")
            self.symops.append(s)
            
            return self.symops

        elif number == 224 or name == "PN-3M":
            self.name = "PN-3M" 
            self.number = 224
            
            if setting == 1: #Pn-3m     
                self.setting = 1
            
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","0","0")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-z","-x","y","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","x","-y","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","y","x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","-x","-y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","z","-y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-z","x","0","0","0")
                self.symops.append(s)
                s = sym("z","-y","x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("z","x","-y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","-z","-y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","x","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","z","-x","0","0","0")
                self.symops.append(s)
                s = sym("z","y","-x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("z","-x","y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-x","z","y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","-z","-x","0","0","0")
                self.symops.append(s)
                s = sym("-z","-y","-x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","x","y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-z","y","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-z","-x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("z","-y","-x","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-z","y","0","0","0")
                self.symops.append(s)
                s = sym("y","z","-x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","y","-x","0","0","0")
                self.symops.append(s)
                s = sym("x","z","y","0","0","0")
                self.symops.append(s)
                s = sym("y","-z","x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","-y","x","0","0","0")
                self.symops.append(s)
                s = sym("x","-z","-y","0","0","0")
                self.symops.append(s)
                s = sym("-y","z","x","1/2","1/2","1/2")
                self.symops.append(s)
                s = sym("z","y","x","0","0","0")
                self.symops.append(s)
                s = sym("-x","z","-y","0","0","0")
                self.symops.append(s)
   
            elif setting == 2: #Pn-3m     
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","-x","y","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-z","x","-y","1/2","0","1/2")
                self.symops.append(s)
                s = sym("-y","x","z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-y","z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("z","-x","-y","0","1/2","1/2")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","y","x","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("y","-x","z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","z","-y","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-y","-x","z","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","-z","x","1/2","1/2","0")
                self.symops.append(s)
                s = sym("z","-y","x","1/2","0","1/2")
                self.symops.append(s)
                s = sym("z","x","-y","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-x","-z","-y","0","0","0")
                self.symops.append(s)
                s = sym("y","x","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","z","-x","1/2","0","1/2")
                self.symops.append(s)
                s = sym("z","y","-x","1/2","1/2","0")
                self.symops.append(s)
                s = sym("z","-x","y","1/2","0","1/2")
                self.symops.append(s)
                s = sym("-x","z","y","0","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-x","-z","0","1/2","1/2")
                self.symops.append(s)
                s = sym("y","-z","-x","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-z","-y","-x","0","0","0")
                self.symops.append(s)
                s = sym("-z","x","y","0","1/2","1/2")
                self.symops.append(s)
                s = sym("x","-z","y","1/2","0","1/2")
                self.symops.append(s)
                s = sym("-y","-z","-x","0","0","0")
                self.symops.append(s)
                s = sym("z","-y","-x","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","x","-z","1/2","0","1/2")
                self.symops.append(s)
                s = sym("-x","-z","y","1/2","1/2","0")
                self.symops.append(s)
                s = sym("y","z","-x","1/2","1/2","0")
                self.symops.append(s)
                s = sym("-z","y","-x","1/2","0","1/2")
                self.symops.append(s)
                s = sym("x","z","y","0","0","0")
                self.symops.append(s)
                s = sym("y","-z","x","1/2","0","1/2")
                self.symops.append(s)
                s = sym("-z","-y","x","1/2","1/2","0")
                self.symops.append(s)
                s = sym("x","-z","-y","0","1/2","1/2")
                self.symops.append(s)
                s = sym("-y","z","x","0","1/2","1/2")
                self.symops.append(s)
                s = sym("z","y","x","0","0","0")
                self.symops.append(s)
                s = sym("-x","z","-y","1/2","0","1/2")
                self.symops.append(s)

            else:
                 
                 print ( ' setting not found ')
                 
            return self.symops
            
        elif number == 225 or name == "FM-3M":
            self.name = "FM-3M"
            self.setting = 1
            self.number = 225
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","z","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","x","0","0","0")
            self.symops.append(s)
            s = sym("z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-x","-z","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-x","z","y","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("x","-z","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","-x","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-z","y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","-x","0","0","0")
            self.symops.append(s)
            s = sym("x","z","y","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","x","0","0","0")
            self.symops.append(s)
            s = sym("x","-z","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","x","0","0","0")
            self.symops.append(s)
            s = sym("-x","z","-y","0","0","0")
            self.symops.append(s)

            return self.symops
            
        elif number == 226 or name == "FM-3C":
            self.name = "FM-3C"
            self.setting = 1
            self.number = 226
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","1/2","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","1/2","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","1/2","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","x","0","1/2","0")
            self.symops.append(s)
            s = sym("-z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","1/2","0","0")
            self.symops.append(s)
            s = sym("x","z","-y","1/2","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","1/2","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","x","0","1/2","0")
            self.symops.append(s)
            s = sym("z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-x","-z","-y","1/2","0","0")
            self.symops.append(s)
            s = sym("y","x","z","1/2","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","-x","0","1/2","0")
            self.symops.append(s)
            s = sym("z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-x","z","y","1/2","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","1/2","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","-x","0","1/2","0")
            self.symops.append(s)
            s = sym("-z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("x","-z","y","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","-x","0","1/2","0")
            self.symops.append(s)
            s = sym("-y","x","-z","1/2","0","0")
            self.symops.append(s)
            s = sym("-x","-z","y","1/2","0","0")
            self.symops.append(s)
            s = sym("y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","-x","0","1/2","0")
            self.symops.append(s)
            s = sym("x","z","y","1/2","0","0")
            self.symops.append(s)
            s = sym("y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","x","0","1/2","0")
            self.symops.append(s)
            s = sym("x","-z","-y","1/2","0","0")
            self.symops.append(s)
            s = sym("-y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","x","0","1/2","0")
            self.symops.append(s)
            s = sym("-x","z","-y","0","0","1/2")
            self.symops.append(s)

            return self.symops
            
        elif number == 227 or name == "FD-3M":
            self.name = "FD-3M"        
            self.number = 227
            
            if setting == 1: #"Fd-3m":

                self.setting = 1
            
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","0","0")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-x","-y","-z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-z","-x","y","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("x","y","-z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","x","-y","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("x","-y","z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","y","x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","-x","-y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("y","-x","z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("x","z","-y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","-x","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","-z","x","0","0","0")
                self.symops.append(s)
                s = sym("z","-y","x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("z","x","-y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-x","-z","-y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("y","x","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","z","-x","0","0","0")
                self.symops.append(s)
                s = sym("z","y","-x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("z","-x","y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-x","z","y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("y","-z","-x","0","0","0")
                self.symops.append(s)
                s = sym("-z","-y","-x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","x","y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("x","-z","y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","-z","-x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("z","-y","-x","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","-z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-z","y","0","0","0")
                self.symops.append(s)
                s = sym("y","z","-x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","y","-x","0","0","0")
                self.symops.append(s)
                s = sym("x","z","y","0","0","0")
                self.symops.append(s)
                s = sym("y","-z","x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","-y","x","0","0","0")
                self.symops.append(s)
                s = sym("x","-z","-y","0","0","0")
                self.symops.append(s)
                s = sym("-y","z","x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("z","y","x","0","0","0")
                self.symops.append(s)
                s = sym("-x","z","-y","0","0","0")
                self.symops.append(s)

            elif setting == 2: #Fd-3m     
                self.setting = 2
            
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/4","0","1/4")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","-z","0","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","-x","y","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","y","-z","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-z","x","-y","1/4","0","1/4")
                self.symops.append(s)
                s = sym("-y","x","z","0","1/4","1/4")
                self.symops.append(s)
                s = sym("x","-y","z","1/4","0","1/4")
                self.symops.append(s)
                s = sym("z","-x","-y","0","1/4","1/4")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","y","x","0","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("y","-x","z","1/4","0","1/4")
                self.symops.append(s)
                s = sym("x","z","-y","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-y","-x","z","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-x","y","z","0","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","-z","x","1/4","1/4","0")
                self.symops.append(s)
                s = sym("z","-y","x","1/4","0","1/4")
                self.symops.append(s)
                s = sym("z","x","-y","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-x","-z","-y","0","0","0")
                self.symops.append(s)
                s = sym("y","x","z","0","0","0")
                self.symops.append(s)
                s = sym("-y","z","-x","1/4","0","1/4")
                self.symops.append(s)
                s = sym("z","y","-x","1/4","1/4","0")
                self.symops.append(s)
                s = sym("z","-x","y","1/4","0","1/4")
                self.symops.append(s)
                s = sym("-x","z","y","0","1/4","1/4")
                self.symops.append(s)
                s = sym("y","-x","-z","0","1/4","1/4")
                self.symops.append(s)
                s = sym("y","-z","-x","0","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","-y","-x","0","0","0")
                self.symops.append(s)
                s = sym("-z","x","y","0","1/4","1/4")
                self.symops.append(s)
                s = sym("x","-z","y","1/4","0","1/4")
                self.symops.append(s)
                s = sym("-y","-z","-x","0","0","0")
                self.symops.append(s)
                s = sym("z","-y","-x","0","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","x","-z","1/4","0","1/4")
                self.symops.append(s)
                s = sym("-x","-z","y","1/4","1/4","0")
                self.symops.append(s)
                s = sym("y","z","-x","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-z","y","-x","1/4","0","1/4")
                self.symops.append(s)
                s = sym("x","z","y","0","0","0")
                self.symops.append(s)
                s = sym("y","-z","x","1/4","0","1/4")
                self.symops.append(s)
                s = sym("-z","-y","x","1/4","1/4","0")
                self.symops.append(s)
                s = sym("x","-z","-y","0","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","z","x","0","1/4","1/4")
                self.symops.append(s)
                s = sym("z","y","x","0","0","0")
                self.symops.append(s)
                s = sym("-x","z","-y","1/4","0","1/4")
                self.symops.append(s)

            else:
             
                print ( ' setting not found')
             
            return self.symops
            
        elif number == 228 or name == "FD-3C":
            self.name = "FD-3C"        
            self.number = 228
            
            if setting == 1: #"Fd-3c":

                self.setting = 1
            
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","y","-z","0","0","0")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-x","-y","-z","3/4","1/4","1/4")
                self.symops.append(s)
                s = sym("x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("-z","-x","y","0","0","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("x","y","-z","1/4","3/4","1/4")
                self.symops.append(s)
                s = sym("-z","x","-y","0","0","0")
                self.symops.append(s)
                s = sym("-y","x","z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("x","-y","z","1/4","1/4","3/4")
                self.symops.append(s)
                s = sym("z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","y","x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","-x","-y","1/4","3/4","1/4")
                self.symops.append(s)
                s = sym("y","-x","z","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("x","z","-y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","-x","z","1/2","0","0")
                self.symops.append(s)
                s = sym("-x","y","z","3/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","-z","x","0","0","0")
                self.symops.append(s)
                s = sym("z","-y","x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("z","x","-y","3/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-x","-z","-y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("y","x","z","1/2","0","0")
                self.symops.append(s)
                s = sym("-y","z","-x","0","0","0")
                self.symops.append(s)
                s = sym("z","y","-x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("z","-x","y","3/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-x","z","y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("y","-z","-x","0","0","0")
                self.symops.append(s)
                s = sym("-z","-y","-x","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","x","y","1/4","1/4","3/4")
                self.symops.append(s)
                s = sym("x","-z","y","1/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","-z","-x","1/4","1/4","3/4")
                self.symops.append(s)
                s = sym("z","-y","-x","0","1/2","0")
                self.symops.append(s)
                s = sym("-y","x","-z","1/2","0","0")
                self.symops.append(s)
                s = sym("-x","-z","y","0","1/2","0")
                self.symops.append(s)
                s = sym("y","z","-x","3/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","y","-x","0","1/2","0")
                self.symops.append(s)
                s = sym("x","z","y","1/2","0","0")
                self.symops.append(s)
                s = sym("y","-z","x","3/4","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","-y","x","0","1/2","0")
                self.symops.append(s)
                s = sym("x","-z","-y","1/2","0","0")
                self.symops.append(s)
                s = sym("-y","z","x","1/4","3/4","1/4")
                self.symops.append(s)
                s = sym("z","y","x","0","1/2","0")
                self.symops.append(s)
                s = sym("-x","z","-y","0","0","1/2")
                self.symops.append(s)
            
            elif setting == 2:  #Fd-3c     
                self.setting = 2
                
                s = sym("x","y","z","0","0","0")
                self.symops.append(s)
                s = sym("-x","-y","z","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-x","y","-z","1/4","0","1/4")
                self.symops.append(s)
                s = sym("z","x","y","0","0","0")
                self.symops.append(s)
                s = sym("y","x","-z","1/4","1/4","1/2")
                self.symops.append(s)
                s = sym("-x","-y","-z","0","0","0")
                self.symops.append(s)
                s = sym("x","-y","-z","0","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","-x","y","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-y","-x","-z","0","0","1/2")
                self.symops.append(s)
                s = sym("x","y","-z","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-z","x","-y","1/4","0","1/4")
                self.symops.append(s)
                s = sym("-y","x","z","1/2","1/4","1/4")
                self.symops.append(s)
                s = sym("x","-y","z","1/4","0","1/4")
                self.symops.append(s)
                s = sym("z","-x","-y","0","1/4","1/4")
                self.symops.append(s)
                s = sym("y","z","x","0","0","0")
                self.symops.append(s)
                s = sym("-z","y","x","1/2","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","-x","-y","0","0","0")
                self.symops.append(s)
                s = sym("y","-x","z","1/4","1/2","1/4")
                self.symops.append(s)
                s = sym("x","z","-y","1/4","1/4","1/2")
                self.symops.append(s)
                s = sym("-y","-x","z","1/4","1/4","1/2")
                self.symops.append(s)
                s = sym("-x","y","z","0","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","-z","x","1/4","1/4","0")
                self.symops.append(s)
                s = sym("z","-y","x","1/4","1/2","1/4")
                self.symops.append(s)
                s = sym("z","x","-y","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-x","-z","-y","0","0","1/2")
                self.symops.append(s)
                s = sym("y","x","z","0","0","1/2")
                self.symops.append(s)
                s = sym("-y","z","-x","1/4","0","1/4")
                self.symops.append(s)
                s = sym("z","y","-x","1/4","1/4","1/2")
                self.symops.append(s)
                s = sym("z","-x","y","1/4","0","1/4")
                self.symops.append(s)
                s = sym("-x","z","y","1/2","1/4","1/4")
                self.symops.append(s)
                s = sym("y","-x","-z","1/2","1/4","1/4")
                self.symops.append(s)
                s = sym("y","-z","-x","0","1/4","1/4")
                self.symops.append(s)
                s = sym("-z","-y","-x","1/2","0","0")
                self.symops.append(s)
                s = sym("-z","x","y","0","1/4","1/4")
                self.symops.append(s)
                s = sym("x","-z","y","1/4","1/2","1/4")
                self.symops.append(s)
                s = sym("-y","-z","-x","0","0","0")
                self.symops.append(s)
                s = sym("z","-y","-x","1/2","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","x","-z","1/4","1/2","1/4")
                self.symops.append(s)
                s = sym("-x","-z","y","1/4","1/4","1/2")
                self.symops.append(s)
                s = sym("y","z","-x","1/4","1/4","0")
                self.symops.append(s)
                s = sym("-z","y","-x","1/4","1/2","1/4")
                self.symops.append(s)
                s = sym("x","z","y","0","0","1/2")
                self.symops.append(s)
                s = sym("y","-z","x","1/4","0","1/4")
                self.symops.append(s)
                s = sym("-z","-y","x","1/4","1/4","1/2")
                self.symops.append(s)
                s = sym("x","-z","-y","1/2","1/4","1/4")
                self.symops.append(s)
                s = sym("-y","z","x","0","1/4","1/4")
                self.symops.append(s)
                s = sym("z","y","x","1/2","0","0")
                self.symops.append(s)
                s = sym("-x","z","-y","1/4","1/2","1/4")
                self.symops.append(s)

            else:
             
                print ( ' setting not found')
             
            return self.symops
            
        elif number == 229 or name == "IM-3M":
            self.name = "IM-3M"
            self.setting = 1
            self.number = 229
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","y","-z","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","z","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("x","z","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-x","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","x","0","0","0")
            self.symops.append(s)
            s = sym("z","x","-y","0","0","0")
            self.symops.append(s)
            s = sym("-x","-z","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","z","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-x","y","0","0","0")
            self.symops.append(s)
            s = sym("-x","z","y","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","-z","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("x","-z","y","0","0","0")
            self.symops.append(s)
            s = sym("-y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","-x","0","0","0")
            self.symops.append(s)
            s = sym("-y","x","-z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-z","y","0","0","0")
            self.symops.append(s)
            s = sym("y","z","-x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","-x","0","0","0")
            self.symops.append(s)
            s = sym("x","z","y","0","0","0")
            self.symops.append(s)
            s = sym("y","-z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","-y","x","0","0","0")
            self.symops.append(s)
            s = sym("x","-z","-y","0","0","0")
            self.symops.append(s)
            s = sym("-y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("z","y","x","0","0","0")
            self.symops.append(s)
            s = sym("-x","z","-y","0","0","0")
            self.symops.append(s)
            
            return self.symops

        elif number == 230 or name == "IA-3D":
            self.name = "IA-3D"
            self.setting = 1
            self.number = 230
            
            s = sym("x","y","z","0","0","0")
            self.symops.append(s)
            s = sym("-x","-y","z","0","1/2","0")
            self.symops.append(s)
            s = sym("-x","y","-z","1/2","0","0")
            self.symops.append(s)
            s = sym("z","x","y","0","0","0")
            self.symops.append(s)
            s = sym("y","x","-z","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-x","-y","-z","0","0","0")
            self.symops.append(s)
            s = sym("x","-y","-z","0","0","1/2")
            self.symops.append(s)
            s = sym("-z","-x","y","0","1/2","0")
            self.symops.append(s)
            s = sym("-y","-x","-z","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("x","y","-z","0","1/2","0")
            self.symops.append(s)
            s = sym("-z","x","-y","1/2","0","0")
            self.symops.append(s)
            s = sym("-y","x","z","1/4","3/4","1/4")
            self.symops.append(s)
            s = sym("x","-y","z","1/2","0","0")
            self.symops.append(s)
            s = sym("z","-x","-y","0","0","1/2")
            self.symops.append(s)
            s = sym("y","z","x","0","0","0")
            self.symops.append(s)
            s = sym("-z","y","x","1/4","3/4","1/4")
            self.symops.append(s)
            s = sym("-z","-x","-y","0","0","0")
            self.symops.append(s)
            s = sym("y","-x","z","1/4","1/4","3/4")
            self.symops.append(s)
            s = sym("x","z","-y","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-y","-x","z","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-x","y","z","0","0","1/2")
            self.symops.append(s)
            s = sym("-y","-z","x","0","1/2","0")
            self.symops.append(s)
            s = sym("z","-y","x","1/4","1/4","3/4")
            self.symops.append(s)
            s = sym("z","x","-y","0","1/2","0")
            self.symops.append(s)
            s = sym("-x","-z","-y","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("y","x","z","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-y","z","-x","1/2","0","0")
            self.symops.append(s)
            s = sym("z","y","-x","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("z","-x","y","1/2","0","0")
            self.symops.append(s)
            s = sym("-x","z","y","1/4","3/4","1/4")
            self.symops.append(s)
            s = sym("y","-x","-z","1/4","3/4","1/4")
            self.symops.append(s)
            s = sym("y","-z","-x","0","0","1/2")
            self.symops.append(s)
            s = sym("-z","-y","-x","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-z","x","y","0","0","1/2")
            self.symops.append(s)
            s = sym("x","-z","y","1/4","1/4","3/4")
            self.symops.append(s)
            s = sym("-y","-z","-x","0","0","0")
            self.symops.append(s)
            s = sym("z","-y","-x","1/4","3/4","1/4")
            self.symops.append(s)
            s = sym("-y","x","-z","1/4","1/4","3/4")
            self.symops.append(s)
            s = sym("-x","-z","y","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("y","z","-x","0","1/2","0")
            self.symops.append(s)
            s = sym("-z","y","-x","1/4","1/4","3/4")
            self.symops.append(s)
            s = sym("x","z","y","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("y","-z","x","1/2","0","0")
            self.symops.append(s)
            s = sym("-z","-y","x","3/4","1/4","1/4")
            self.symops.append(s)
            s = sym("x","-z","-y","1/4","3/4","1/4")
            self.symops.append(s)
            s = sym("-y","z","x","0","0","1/2")
            self.symops.append(s)
            s = sym("z","y","x","1/4","1/4","1/4")
            self.symops.append(s)
            s = sym("-x","z","-y","1/4","1/4","3/4")
            self.symops.append(s)

            return self.symops
            
        else:
            
            print ( 'class name or number not found')