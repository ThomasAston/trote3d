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
        self.xl = np.zeros((3, in_vars.nelem), dtype='float')
        if (in_vars.irs==1): self.bc = np.zeros((6*3*8), dtype='float')


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

                #cooloc.f        
                for inl in range(in_vars.nelem):
                    ino = mesh.mcon[mc+inl]
                    for icoor in range(3):
                        self.xl[icoor,inl] = mesh.x[icoor,ino-1] # same here
                        idl[icoor,inl] = mesh.id[icoor,ino-1] # same here

                # Calculation of the matrix of the derivatives of the functions of 
                # shape of elements 
                if (in_vars.irs==1):
                    soma2 = np.empty((3), dtype='float')
                    xjac = np.empty((3, 3), dtype='float')
                    xjacinv = np.empty((3, 3), dtype='float')
                    for j in range(3):
                        for i in range(3): 
                            soma1=0.e0
                            for k in range(in_vars.nelem):
                                soma1 += mesh.dfils8[i,k]*self.xl[j,k]
                            xjac[i,j] = soma1
                    
                    xjacinv = np.linalg.inv(xjac)
                    for k in range(in_vars.nelem):
                        for i in range(3):
                            soma2[i] = 0.e0
                            for j in range(3):
                                soma2[i]+= xjac[i,j]*mesh.dfils8[j,k]
                    
                        for l in range(3):
                            self.bc[0,l,k] = soma2[l]
                            self.bc[1,l,k] = soma2[l]
                            self.bc[2,l,k] = soma2[l]
                    
                for ipint in range(npint):
                    igauss += 1
                    
                        
            

            #TODO- Manually forcing condition
            self.nred = 100
            self.lopt = True
