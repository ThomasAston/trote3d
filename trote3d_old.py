import numpy as np

class trote3d:

    ELEFI = {
        "FIS4" : np.empty((4),dtype='uint8'),
        "DFILS4" : np.empty((3,4),dtype='uint8'),
        "PS4" : -1,
        "FIS6" : np.empty((6),dtype='uint8'),
        "DFILS6" : np.empty((3,6),dtype='uint8'),
        "PS6" : -1,
        "FIS8" : np.empty((8),dtype='uint8'),
        "DFILS8" : np.empty((3,8),dtype='uint8'),
        "PS8" : -1,
        "FIP6" : np.empty((6,2),dtype='uint8'),
        "DFILP6" : np.empty((3,6,2),dtype='uint8'),
        "PP6" : np.empty((2),dtype='uint8'),
        "FIP8" : np.empty((8,8),dtype='uint8'),
        "DFILP8" : np.empty((3,8,8),dtype='uint8'),
        "PP8" : np.empty((8),dtype='uint8'),
        "DG" : np.empty((3,3,8),dtype='uint8'),
        "DDG" : np.empty((8),dtype='uint8')
    }

	# Copied from FTD's original MATER.INC
    # Common area of ​​material parameters
    MATER = {
        "R_MODY": -1,   # Young's module of reinforcement
        "R_POISS": -1,  # Reinforcement Poisson Coefficient
        "R_Y0": -1,     # Initial elastic limit of reinforcement
        "R_ALFA": -1,   # Reinforcement thermal expansion coefficient
        "R_LAMBDA": -1, # Lambda Lame Coefficient of Reinforcement
        "R_MIU": -1,    # Miu Lame Coefficient of Reinforcement
        "R_KAPA": -1,   # Coefficient k=lambda2*miu/3 of the reinforcement
        "XM_MODY": -1,  # Young's modulus of the matrix
        "XM_POISS": -1, # Poisson's coefficient of the matrix
        "XM_Y0": -1,    # Initial elastic limit of the matrix
        "XM_ALFA": -1,  # Matrix thermal` expansion coefficient
        "XM_LAMBDA": -1,# Lame lambda coefficient of the matrix
        "XM_MIU": -1,   # Matrix Lame Miu Coefficient
        "XM_KAPA": -1,  # Coefficient k=lambda2*miu/3 of the matrix
        "HF": -1,       # Hill's anisotropy coefficients
        "HG": -1,       # Hill's anisotropy coefficients
        "HH": -1,       # Hill's anisotropy coefficients
        "HL": -1,       # Hill's anisotropy coefficients
        "HM": -1,       # Hill's anisotropy coefficients
        "HN": -1,       # Hill's anisotropy coefficients
        "AANAND": -1,   # Parameter A of Anand's law of behavior
        "QANAND": -1,   # Q parameter of Anand's law of behavior
        "CSIANAND": -1, # Csi parameter of Anand's law of behavior
        "SOANAND": -1,  # Initial value of the state parameter s
        "EMANAND": -1,  # Parameter m of Anand's law of behavior
        "ANSBAR": -1,   # Average value of the state parameter only
        "ANANN": -1,    # Parameter n of Anand's law of behavior
        "ANH0": -1,     # h0 value of Anand's law of behavior
        "ANANA": -1,    # Parameter a of Anand's law of behavior
        "RGASP": -1     # Perfect gas constant 
    }

	# Copied from FTD's original PONTE.INC
    # Common area of ​​dynamic management hands
    PONTE = {
        "LPA": -1,      # Table A usage limit
        "LPK": -1,      # K table usage limit
        "LPX0": -1,     # Initial problem coordinates
        "LPX": -1,      # Current coordinates of the problem
        "LINTAB": -1,
        "LNGAUS": -1,   # Number of Gauss Points per Element
        "LNNODE": -1,   # Number of us per element
        "LMCTAB": -1,   # Element pointers to the MCON table
        "LNTYPE": -1,   # Type of element integration
        "LMCON": -1,    # Mesh Connectivity Table
        "LXOR": -1,
        "LELM": -1,     # Table with the results in the
        "LDU": -1,      # Displacements in nodes (global coordinates)
        "LDUR": -1,
        "LFRN": -1,     # Nodal reactions
        "LXSM": -1,     # Second global member
        "LCONDL": -1,
        "LCGV": -1,
        "LXMR": -1,     # Global stiffness matrix
        "LNCR": -1,
        "LID": -1,      # Table of equations with non-prewritten gl
        "LJDIAG": -1,   # Position of diagonal terms in the global matrix
        "LESTAD": -1,
        "LIGSM": -1 
    }

	# # Copied from FTD's original UNIES.INC
    # # Common area of unit numbers and / or 
    # UNIES = {
    #     "ITINPUT": -1,  # Single input data file
    #     "IUNID": -1,    # Outer mesh, COSMOS/M 
    #     "IMSG": -1,     # Output results, file msg1.out
    #     "IMSG2": -1,    # Results output, msg2.out file
    #     "IMSH": -1,     # Postprocessor, mesh file *.flavia.msh
    #     "IRES": -1      # Postprocessed, results file
    # }	

	# Copied from FTD's original VARCA.INC
    # Character type variables common area 
    VARCA = {
        "FPRNOME": " ", # Name of problem to solve
        "FMEXT": " ",   # Outdoor mesh file
        "FTINPUT": " ", # Single input data file
        "FMSH": " ",    # Post-processor, ASCII mesh
        "FRES": " ",    # Postprocessor, Results in ASCII
        "REINOME": " ", # *.ffr file for reset
        "EXMSH": ".ffm",   # *.ffm binary file extension
        "EXRES": ".ffr",   # *.ffr binary file extension
        "EXOUT": ".out"    # Extension of *.out files
    }

    # Copied from FTD's original VARIN.INC
    # Common area of ​​integer variables
    VARIN = {
        "MA" : -1,      # Dimension of the super table of reals A
        "MK " : -1,     # Dimension of the super table of integers K
        "MAAV " : -1,   # Space remaining in A
        "MKAV " : -1,   # Space remaining in K
        "NINICI " : -1,  # Number of the first calculation step
        "FINISH " : -1, # Maximum number of calculation steps
        "NGRAV " : -1,  # *.ffr recording frequency
        "NSAI " : -1,   # Frequency of security exits
        "IMP " : -1,    # Results printing parameter
        "NIMAX " : -1,  # Maximum number of time increments
        "NRMAX " : -1,  # Num max increment reduction attempts
        "NITCG " : -1,  # In a max of iterations of system resolution
        "NMALH " : -1,  # Mesh file source definition
        "NCONDL " : -1, # Definition of origin of boundary conditions
        "NOPTIM " : -1, # Optimization option parameter
        "NPH " : -1,    # Pair. choose correction hydrostatic pressure
        "IRS " : -1,    # Selective reduced integration
        "NN " : -1,     # Total number of nodes in the structure
        "NE " : -1,     # Total number of structure elements
        "NEL " : -1,    # Number of us per element
        "NNODT " : -1,  # Connectivity table dimension
        "NN3 " : -1,    # Total number of degrees of freedom
        "MEL " : -1,    # Number of elements in ELM table
        "MISMAX " : -1, # For XMR Scaling
        "NIPT " : -1,   # Total number of Gaussian points
        "NINC " : -1,   # Current calculation increment number
        "NEQ " : -1,    # Number of equations to solve (without prescribed gl)
        "MALHDR " : -1, # mesh generation direction
        "NL" : -1,      # Dimensions in mesh elements
        "NC" : -1,      # Dimensions in mesh elements
        "NH" : -1,      # Dimensions in mesh elements
        "NELEM " : -1,  # Number of us per element
        "NREDTOT " : -1,# Total number of step reduction attempts
        "ICUT " : -1,   # Useful length of string FPRNOME
        "ICUTR " : -1,  # Useful length of string REINOME
        "IPGAU " : -1,  # Gaussian point monitoring results
        "IPECR " : -1,  # Print frequency for the screen
        "IPMSG1 " : -1, # Print frequency for MSG1.out
        "ICFX" : -1,    # Definition of symmetry coordinate planes
        "ICFY" : -1,    # Definition of symmetry coordinate planes
        "ICFZ " : -1,   # Definition of symmetry coordinate planes
        "IPLX" : -1,    # Definition of additional planes of symmetry 
        "IPLY": -1,     # Definition of additional planes of symmetry 
        "IPLZ" : -1     # Definition of additional planes of symmetry 
    }

	# Copied from FTD's original VARLO.INC
    # Common zone of logical variables 
    VARLO = {
        "LOPT": False, # Increment optimization indicator 
    }

    # Copied from FTD's original VARRE.INC
    # Common area of real variables 
    VARRE = {
        "T0":-1,    # Initial temperature value
        "TFIM":-1,  # Final process temperature
        "VARR":-1,  # cooling speed
        "T":-1,     # current value of time
        "DT":-1,    # Maximum time increment
        "PI":-1,    # PI value
        "PI2":-1,   # PI/2 value
        "PHI":-1,   # Integration portion
        "DELTA":-1, # Optimization parameter
        "DEPTOL":-1,# Optimization parameter
        "ZERO":-1,  # Small value to compare with zero
        "R13":-1,   # One third
        "R23":-1,   # Two thirds
        "SQR3":-1,  # square root of one third
        "TOLS":-1,  # Tolerance in parameter calculation only
        "CPLX":-1,  # Coordinates of additional planes of symmetry 
        "CPLY":-1,  #Coordinates of additional planes of symmetry 
        "CPLZ":-1   # Coordinates of additional planes of symmetry 
    }

    def __init__(self, MAMAX, MKMAX):
        self.MA = MAMAX
        self.MK = MKMAX
        self.A = np.zeros((MAMAX))
        self.K = np.zeros((MKMAX))

    # Definition of logical units and names of Input/Output (I/O) files
    def deflog(self, filename):
        self.VARCA['FTINPUT'] = filename
        file = open(filename, 'r')
        lines = file.readlines()
        self.VARCA['FPRNOME'] = str.split(lines[0])[0]
        self.VARCA['FMSH'] =  self.VARCA['FPRNOME'] + self.VARCA['EXMSH']
        self.VARCA['FRES'] =  self.VARCA['FPRNOME'] + self.VARCA['EXRES']
        self.VARCA['FMEXT'] =  self.VARCA['FPRNOME'] + self.VARCA['EXOUT']
        file.close()

    # Reading input files and filling in the respective common areas 
    def lefent(self):
        file = open(self.VARCA['FTINPUT'], 'r')
        lines = file.readlines() # Reading twice here is a bit silly
        # Making use of the fixed file format [Lines 2-6]
        self.VARIN['NINICI','NIMAX','NRMAX','NGRAV'] = str.split(lines[2])[0:4]
        self.VARIN['NMALH','NCONDL','NOPTIM','NPH','IRS'] = str.split(lines[3])[0:5]
        self.VARIN['PHI','DELTA','DEPTOL'] = str.split(lines[4])[0:2]
        self.VARIN['T0','TFIM'] = str.split(lines[5])[0:1]
        self.VARIN['DT'] = str.split(lines[6])[0]
        self.VARRE['VARR'] = str.split(lines[6])[0]

        if self.VARIN['NMALH']==1:
            LEMALH(A,K)

    class cmalha:

        def __init__(self, filename):
            file = open(filename, 'r')
            lines = file.readlines() # Reading a third time here is a bit silly
            # Making use of the fixed file format [Lines 8-11]
            self.malhdr, self.nelem = str.split(lines[8])[0:1]
            self.nl, self.nc, self,nh = str.split(lines[9])[0:2]
            self.sth, self.slen, self.shig = str.split(lines[10])[0:2]
            self.nlay, self.nz, self.nmat = str.split(lines[11])[0:2]
            for i in range(self.nlay):
                self.thl, self.nly, self.matl, self.nityp = str.split(lines[8])[0:1]



if __name__ == "__main__":

    prog = trote3d(MAMAX=1000000,MKMAX=1000000)
    prog.deflog('Tinput.tro')
    prog.lefent()