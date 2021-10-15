from typing import Callable
import numpy as np

class Trote3d_temperature_integration:

    # Defines the initial variables used in the temperature integration
    def __init__(self, consts, in_vars, condition: Callable[[], bool]=None):

        if (in_vars.ninici!=1): self.ninc = in_vars.ninici+1
        else: self.ninc = in_vars.ninici
        self.farref = False
        if (in_vars.t0 > in_vars.tfim): self.farref = True

        self.farref = False
        if (in_vars.t0 > in_vars.tfim): self.farref = True

        if (condition is None):
            self.condition = lambda:((self.ninc<=in_vars.nimax) and 
                (((consts.temp>in_vars.tfim) and self.farref) or 
                ((consts.temp<in_vars.tfim) and (not self.farref))))

        leicom = 1
        nredtot = ifim = 0

        self.idl = np.zeros((3, in_vars.nelem), dtype='float')

    def integrate(self, in_vars, mesh, consts, time_int):

        while self.condition():

            if ((consts.temp+consts.dtemp)<in_vars.tfim):
                consts.dtemp=in_vars.tfim-consts.temp
                in_vars.dt=consts.dtemp/in_vars.varr
                ifim = 1
            
            consts.calc_matrix_mat_props_with_temp()

            time_int.integrate(in_vars, mesh, self.idl)

            #TODO- Manually forcing condition
            self.ninc = 100
            consts.temp = -100
            self.farref = True