from typing import Callable
import numpy as np

class Trote3d_time_integration:

    # Defines the initial variables used in the temperature integration
    def __init__(self, in_vars, nred=1, nrmax=10, condition: Callable[[], bool]=None):

        self.lopt = False
        self.nred = nred
        self.nrmax = nrmax

        if (condition is None):
            self.condition = lambda:(self.nred<=in_vars.nrmax and self.lopt==False)

        leicom = 1
        nredtot = ifim = 0

        self.xmre = np.zeros((3, in_vars.nelem), dtype='float')


    def integrate(self, in_vars, mesh, idl):

        igauss = 0
        for ie in range(mesh.ne):
            npint = mesh.ngauss[ie]
            for _ in range(npint):
                mesh.elm[8,igauss] = mesh.elm[33,igauss]
                igauss+=1
            
        while self.condition():

            igauss = 0
            for ie in range(mesh.ne):
                mc    = mesh.mctabl[ie]
                mat   = mesh.mcon[mc+in_vars.nelem] # had to add -1 here
                npint = mesh.ngauss[ie]           
                for inl in range(in_vars.nelem):
                    ino = mesh.mcon[mc+inl]
                    for icoor in range(3):
                        idl[icoor,inl] = mesh.id[icoor,ino-1] # same here
            

            #TODO- Manually forcing condition
            self.nred = 100
            self.lopt = True
