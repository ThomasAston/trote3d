import numpy as np

class Trote3d_elements:

    def __init__(self, consts):

        # Preallocating memory with zeroes numpy arrays
        self.pp6 = np.zeros((2), dtype='float')
        self.fis4 = np.zeros((4), dtype='float')
        self.fis6 = np.zeros((6), dtype='float')
        self.fis8 = np.zeros((8), dtype='float')
        self.ddg = np.zeros((8), dtype='float')
        self.pp8 = np.zeros((8), dtype='float')
        self.dfils4 = np.zeros((3,4), dtype='float')
        self.dfils6 = np.zeros((3,6), dtype='float')
        self.dfils8 = np.zeros((3,8), dtype='float')
        self.fip6 = np.zeros((6,2), dtype='float')
        self.fip8 = np.zeros((8,8), dtype='float')
        self.dfilp6 = np.zeros((3,6,2), dtype='float')
        self.dfilp8 = np.zeros((3,8,8), dtype='float')
        self.dg = np.zeros((3,3,8), dtype='float')

        # Temporary variables for calculation
        w = np.zeros((2), dtype='float')
        gp = np.zeros((2,2), dtype='float')
        dgp = np.zeros((2,2), dtype='float')

        # 4-node tetrahedral element and 1 integration point
        for k in range(4):
            self.fis4[k] = 0.25e0
        self.dfils4[0,0] = -1.0e0
        self.dfils4[1,0] = -1.0e0
        self.dfils4[2,0] = -1.0e0
        self.dfils4[0,1] = 1.0e0
        self.dfils4[1,2] = 1.0e0
        self.dfils4[2,3] = 1.0e0
        self.ps4         = 1.0e0/6.0e0


        # Prismatic element of 6 nodes and 1 point of integration
        w7 = 0.50e0*consts.r13
        for k in range(6):
            self.fis6[k] = w7
        self.dfils6[0,0] = -0.50e0
        self.dfils6[1,0] = -0.50e0
        self.dfils6[2,0] = -w7
        self.dfils6[0,1] = 0.50e0
        self.dfils6[2,1] = -w7
        self.dfils6[1,2] = 0.50e0
        self.dfils6[2,2] = -w7
        self.dfils6[0,3] = -0.50e0
        self.dfils6[1,3] = -0.50e0
        self.dfils6[2,3] = w7
        self.dfils6[0,4] = 0.50e0
        self.dfils6[2,4] = w7
        self.dfils6[1,5] = 0.50e0
        self.dfils6[2,5] = w7
        self.ps6         = 1.00e0


        # Prismatic element of 6 nodes and 2 integration points
        w[0]   = 0.5e0*(1.0e0-consts.sqr3)
        w[1]   = 0.5e0*(1.0e0+consts.sqr3)
        w5   = consts.r13*w[0]
        w6   = consts.r13*w[1]
        for kp in range(2):
            self.dfilp6[0,1,kp] = -w[kp]
            self.dfilp6[0,2,kp] = w[kp]
            self.dfilp6[1,1,kp] = -w[kp]
            self.dfilp6[1,3,kp] = w[kp]
            self.pp6[kp]=0.5e0
        for k in range(3):
            l                  = k+3
            self.fip6[k,0]     = w5
            self.fip6[k,1]     = w6
            self.fip6[l,0]     = w6
            self.fip6[l,1]     = w5
            self.dfilp6[2,k,0]= -w7
            self.dfilp6[2,k,1]= -w7
            self.dfilp6[2,l,0]= w7
            self.dfilp6[2,l,1]= w7
            self.dfilp6[0,l,0]= self.dfilp6[0,k,1]            
            self.dfilp6[1,l,0]= self.dfilp6[1,k,1]            
            self.dfilp6[0,l,1]= self.dfilp6[0,k,0]            
            self.dfilp6[1,l,1]= self.dfilp6[1,k,0]        


        # 8-node hexahedral element and 1 integration point
        for k in range(8):
            self.fis8[k] = 0.125e0
        w4 = 0.125e0
        l  = 0
        for k in range(2):
            for j in range(2):
                for i in range(2):
                    self.dfils8[0,l] = w4*(-1.0e0)**(i+1)
                    self.dfils8[1,l] = w4*(-1.0e0)**(j+1)
                    self.dfils8[2,l] = w4*(-1.0e0)**(k+1)
                    self.dg[0,1,l]   = w4*(-1.0e0)**(i+j+2)
                    self.dg[0,2,l]   = w4*(-1.0e0)**(i+k+2)
                    self.dg[1,2,l]   = w4*(-1.0e0)**(j+k+2)
                    self.ddg[l]      = w4*(-1.0e0)**(i+j+k+3)
                    l                = l+1
        for l in range(8):
            self.dg[1,0,l] = self.dg[0,1,l]
            self.dg[2,0,l] = self.dg[0,2,l]
            self.dg[2,1,l] = self.dg[1,2,l]
            self.dg[0,0,l] = 0.0e0
            self.dg[1,1,l] = 0.0e0
            self.dg[2,2,l] = 0.0e0
        self.ps8 = 8.0e0


        # 8-node hexahedral element and 8 integration points
        aip=-3.0e0*consts.sqr3
        for ip in range(2):
            aip       += consts.sqr3+consts.sqr3
            gp[0,ip]  = 0.5e0*(1.0e0-aip)
            gp[1,ip]  = 0.5e0*(1.0e0+aip)
            dgp[0,ip] = -0.5e0
            dgp[1,ip] = 0.5e0
        for lp in range(2):
            for jp in range(2):
                for ip in range(2):
                    kp      = 4*(lp)+2*(jp)+ip
                    self.pp8[kp] = 1.0e0
                    for l in range(2):
                        for j in range(2):
                            for i in range(2):
                                k                   = 4*(l)+2*(j)+i
                                self.fip8[k,kp]     = gp[i,ip]*gp[j,jp]*gp[l,lp]
                                self.dfilp8[0,k,kp] = dgp[i,ip]*gp[j,jp]*gp[l,lp]
                                self.dfilp8[1,k,kp] = gp[i,ip]*dgp[j,jp]*gp[l,lp]
                                self.dfilp8[2,k,kp] = gp[i,ip]*gp[j,jp]*dgp[l,lp]
