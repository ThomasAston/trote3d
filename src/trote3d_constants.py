from dataclasses import dataclass
from typing import ClassVar
from math import sqrt, asin

@dataclass()
class Trote3d_constants:
    
    epsilon: ClassVar[float] = 1.0e-9
    r13: ClassVar[float] = 1.0e0/3.e0
    r23: ClassVar[float] = 2.e0/3.e0
    sqr3: ClassVar[float] = sqrt(r13)
    pi2: ClassVar[float] = asin(1.e0)
    pi : ClassVar[float] = pi2 + pi2
    mel: ClassVar[int] = 43
    rgasp: ClassVar[float] = 8.3143e0  

    def calc_material_constants(self, materials, i, j):

        # reinforcement material constants 
        reinf = materials.materials["reinforcements"][i]
        self.r_lambda=reinf["r_poiss"]*reinf["r_mody"]/((1.0e0+
            reinf["r_poiss"])*(1.0e0-2.0e0*reinf["r_poiss"]))
        self.r_miu = reinf["r_mody"]/(2.0e0*(1.0e0+reinf["r_poiss"]))
        self.r_kapa = self.r_lambda+self.r23*self.r_miu

        # matrix onstants 
        mat = materials.materials["matrixes"][j]
        self.xm_lambda = mat["xm_poiss"]*mat["xm_mody"]/((1.0e0+
            mat["xm_poiss"])*(1.0e0-2.0e0*mat["xm_poiss"]))
        self.xm_miu = mat["xm_mody"]/(2.0e0*(1.0e0+mat["xm_poiss"]))
        self.xm_kapa = self.xm_lambda+self.r23*self.xm_miu

    def set_temp_and_time_variables(self, in_vars):
            self.temp = in_vars.t0
            self.dtemp = in_vars.varr*in_vars.dt
            self.t = 0.e0
            self.dtn = 0.e0

    #TODO - This makes no sense, the properties are hard coded
    def calc_matrix_mat_props_with_temp(self):
        self.xm_miu = 27041.0e0-17.057e0*(self.temp-273.0e0)
        self.xm_mody = 72474.0e0-43.480e0*(self.temp-273.0e0)
        self.xm_poiss = (18392.0e0-9.366e0*(self.temp-273.0e0))/(54082.0e0-34.114e0*(self.temp-273.0e0))
        self.xm_lambda = self.xm_poiss*self.xm_mody/((1.0e0+self.xm_poiss)*(1.0e0-2.0e0*self.xm_poiss))
        self.xm_kapa = self.r_lambda+self.r23*self.r_miu