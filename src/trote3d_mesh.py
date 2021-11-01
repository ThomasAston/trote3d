import numpy as np

class Trote3d_mesh:

    def __init__(self, in_vars, mel=43):
        self.mel = mel
        self.inputs = in_vars
        self.nn = (in_vars.nl+1)*(in_vars.nc+1)*(in_vars.nh+1)  # Total number of nodes in the mesh
        self.ne = in_vars.nl*in_vars.nc*in_vars.nh              # total number of elements
        if(in_vars.nelem==6):                                   # Hex element case
            self.nn += self.ne+in_vars.nl*in_vars.nc            # total number of nodes in the mesh
            self.ne *= 4                                        # total number of elements
        self.nn3 = self.nn*3                                    # Total number of degrees of freedom
        self.nnodt = self.ne*(in_vars.nelem+1)                  # Dimension of the connectivity table 
    
        # Preallocating memory with empty (non-zero, random) numpy arrays
        # TODO - Might need to be zeroed
        self.xinit = np.empty((3,self.nn), dtype='float')
        self.x = np.empty((3,self.nn), dtype='float')
        self.mcon = np.zeros((self.nnodt), dtype='int')
        self.intabl = np.empty((self.ne), dtype='int')
        self.ngauss = np.empty((self.ne), dtype='int')
        self.nnode = np.empty((self.ne), dtype='int')
        self.mctabl = np.empty((self.ne), dtype='int')
        self.ntype = np.empty((self.ne), dtype='int')

        self.condl = np.zeros((3, self.nn), dtype='float')
        self.ncr = np.zeros((3, self.nn), dtype='int')

        self.jdiag = np.empty((self.nn3), dtype='int')
        self.id = np.zeros((3, self.nn), dtype='int')


    def generate_mesh(self):
       
        nel = self.inputs.nelem
        nnod1 = nel+1
        nc1 = self.inputs.nc+1
        nc2 = self.inputs.nc*2
        nc21 = nc2+1
        nc22 = nc21+1
        nl1 = self.inputs.nl+1
        nh1 = self.inputs.nh+1

        # Calculate the number of corner nodes
        ilst = 1
        ilend = nc1
        if(nel==6): iuend = nc21*self.inputs.nl+nc1
        else: iuend = nc1*nl1
        iust = iuend - nc1
        iueh = iuend*self.inputs.nh
        ilstb = ilst+iueh
        ilendb = ilend+iueh
        iustb = iust+iueh
        iuendb = iuend+iueh

        self.input_error_checking()

        # Initialize variables for ILY=IZ=1,IL=IC=0 
        ies=0
        ins=ilend
        xln=0e0
        rnh=self.inputs.nh
        d3h=self.inputs.shig/rnh

        # Loop over width/thickness layer (STH direction)
        for ily in range(self.inputs.nlay):
            nlil=self.inputs.nly[ily]
            rnlil=nlil
            d2l=self.inputs.thl[ily]/rnlil
            matly=self.inputs.matl[ily]          
            ityly=self.inputs.nityp[ily]

            # Loop over element (or cell) rows within each layer   
            for il in range(nlil):
                if(nel==6): ins=ins+nc1
                else: ins=ins+1
                x1n=self.inputs.slen
                xln=xln+d2l
                if(ily+1==self.inputs.nlay and il+1==self.inputs.nl): xln=self.inputs.sth

                # Generate nodes on the right surface
                xhn=0.e0
                inv=ins
                for ihg in range(1, nh1+1):
                    self.xinit[0,inv-1]=self.inputs.slen
                    if(self.inputs.malhdr==1):
                        self.xinit[1,inv-1]=xln
                        self.xinit[2,inv-1]=self.inputs.shig-xhn
                    else:
                        self.xinit[1,inv-1]=xhn
                        self.xinit[2,inv-1]=xln       
                    xhn=xhn+d3h
                    if(ihg==self.inputs.nh): xhn=self.inputs.shig
                    inv+=iuend

                # Loop over the X1-zones (SLEN direction) 
                for iz in range(1, self.inputs.nz+1):
                    nciz=self.inputs.ncz[iz-1]
                    rnciz=nciz
                    d1z=self.inputs.elz[iz-1]/rnciz

                    # Loop over the element (or cell) columns within each zone 
                    for ic in range(1, nciz+1):
                        ins+=1
                        in1s=ins-nc1
                        x1n-=d1z
                        if(iz==self.inputs.nz and ic==nciz): 
                            x1n=0.e0
                        ies+=1

                        # Loop over the third direction (SHIG direction);
                        # genetate nodes and nodal connectivity, and assign material
                        # id. no., and also generate arrays NTYPE(IE), MCTABL(IE)
                        # and NGAUSS(IE).
                        xhn=0.e0
                        inv=ins
                        in1=in1s
                        ie=ies 
                        for ihg in range(1,nh1+1):
                            self.xinit[0,inv-1]=x1n
                            if(self.inputs.malhdr==1):
                                self.xinit[1,inv-1]=xln
                                self.xinit[2,inv-1]=self.inputs.shig-xhn
                            else:
                                self.xinit[1,inv-1]=xhn
                                self.xinit[2,inv-1]=xln
                            if(nel==6):
                                self.xinit[0,in1-1]=x1n+0.5e0*d1z
                                if(self.inputs.malhdr==1):
                                    self.xinit[1,in1-1]=xln-0.5e0*d2l
                                    self.xinit[2,in1]=self.inputs.shig-xhn
                                else:
                                    self.xinit[1,in1-1]=xhn
                                    self.xinit[2,in1-1]=xln-0.5e0*d2l

                            if(ihg>self.inputs.nh): continue # might need to be a break statement
                            
                            if(nel==6):
                                iei=4*(ie-1)
                                mci=nnod1*iei
                                mc1=mci
                                mc2=mc1+nnod1
                                mc3=mc2+nnod1
                                mc4=mc3+nnod1
                                for _ in range(4):
                                    iei=iei+1
                                    self.mctabl[iei-1]=mci
                                    mci=mci+nnod1
                                    self.mcon[mci-1]=matly
                                    self.ntype[iei-1]=ityly
                                    self.ngauss[iei-1]=2
                                    if(ityly==2): self.ngauss[iei-1]=1
                                self.mcon[mc1]=in1+iuend
                                self.mcon[mc1+1]=inv-nc21+iuend
                                self.mcon[mc1+2]=inv-nc22+iuend
                                self.mcon[mc1+3]=in1       
                                self.mcon[mc1+4]=inv-nc21      
                                self.mcon[mc1+5]=inv-nc22       
                                self.mcon[mc2]=in1+iuend
                                self.mcon[mc2+1]=inv-nc22+iuend
                                self.mcon[mc2+2]=inv-1+iuend
                                self.mcon[mc2+3]=in1       
                                self.mcon[mc2+4]=inv-nc22      
                                self.mcon[mc2+5]=inv-1          
                                self.mcon[mc3]=in1+iuend
                                self.mcon[mc3+1]=inv-1+iuend
                                self.mcon[mc3+2]=inv+iuend
                                self.mcon[mc3+3]=in1       
                                self.mcon[mc3+4]=inv-1         
                                self.mcon[mc3+5]=inv            
                                self.mcon[mc4]=in1+iuend
                                self.mcon[mc4+1]=inv+iuend
                                self.mcon[mc4+2]=inv-nc21+iuend
                                self.mcon[mc4+3]=in1       
                                self.mcon[mc4+4]=inv           
                                self.mcon[mc4+5]=inv-nc21    
                                in1=in1+iuend
                            
                            else:
                                mc=nnod1*(ie-1)
                                self.mcon[mc+nnod1-1]=matly
                                self.ntype[ie-1]=ityly
                                self.mctabl[ie-1]=mc
                                self.ngauss[ie-1]=8
                                if(ityly==2 or ityly==5 or ityly==6 or ityly==7): self.ngauss[ie-1]=1
                                self.mcon[mc]=inv-nc1+iuend
                                self.mcon[mc+1]=inv-nc1-1+iuend
                                self.mcon[mc+2]=inv+iuend 
                                self.mcon[mc+3]=inv-1+iuend
                                self.mcon[mc+4]=inv-nc1
                                self.mcon[mc+5]=inv-nc1-1
                                self.mcon[mc+6]=inv       
                                self.mcon[mc+7]=inv-1

                            inv=inv+iuend
                            ie=ie+self.inputs.nc*self.inputs.nl
                            xhn=xhn+d3h
                            if(ihg==self.inputs.nh): xhn=self.inputs.shig    
        
        # Generate nodes on the front/lower surface
        inv=1 
        xhn=0.e0
        for ihg in range(1,nh1+1):
            self.xinit[0,inv-1]=self.inputs.slen
            if(self.inputs.malhdr==1):
                self.xinit[1,inv-1]=0.e0
                self.xinit[2,inv-1]=self.inputs.shig-xhn
            else:
                self.xinit[1,inv-1]=xhn
                self.xinit[2,inv-1]=0.e0      
            inv=inv+iuend
            xhn=xhn+d3h
            if(ihg==self.inputs.nh): xhn=self.inputs.shig

        ins=1
        x1n=self.inputs.slen
        for iz in range(self.inputs.nz):
            nciz=self.inputs.ncz[iz]
            rnciz=nciz
            d1z=self.inputs.elz[iz]/rnciz
            for ic in range(1,nciz+1):
                ins=ins+1
                x1n=x1n-d1z
                if(iz+1==self.inputs.nz and ic==nciz): x1n=0.e0
                inv=ins
                xhn=0.e0
                for ihg in range(1,nh1+1):
                    self.xinit[0,inv-1]=x1n
                    if(self.inputs.malhdr==1):
                        self.xinit[1,inv-1]=0.e0
                        self.xinit[2,inv-1]=self.inputs.shig-xhn
                    else:
                        self.xinit[1,inv-1]=xhn
                        self.xinit[2,inv-1]=0.e0       
                    inv=inv+iuend
                    xhn=xhn+d3h
                    if(ihg==self.inputs.nh): xhn=self.inputs.shig

        # Generate array INTABL(NE), NNODE(NE), and calculate NIPT
        self.intabl[0]=0
        for ie in range(1,self.ne):
            self.nnode[ie-1]=nel
            self.intabl[ie]=self.intabl[ie-1]+self.ngauss[ie-1]
        self.nnode[self.ne-1]=nel
        self.nipt=self.intabl[self.ne-1]+self.ngauss[self.ne-1]

        # Copy array XINI in X [is this really needed?]
        self.x = np.copy(self.xinit)

        # Returning the corner nodes so that they can be logged
        return [ilst, ilend, iust, iuend, ilstb, ilendb, iustb, iuendb]


    def input_error_checking(self):

        epsilon = 1e-10     # small value for double comparisons
        # Why is im needed?
        im = np.empty((20)) # empty numpy array of size 20 (random values)

        nlay = self.inputs.nlay
        nz = self.inputs.nz
        if(nlay*(21-nlay)<=0): raise ValueError("*** error; illegal number of layers")
        if(nz*(21-nz)<=0): raise ValueError("*** error; illegal number of zones")
        s = 0.e0
        jj = 0
        for ily in range(nlay):
            s += self.inputs.thl[ily] 
            jj += self.inputs.nly[ily]
            matly = self.inputs.matl[ily]
            ityly = self.inputs.nityp[ily]
            
            # IF(MATLY*(NMAT-MATLY+1).LE.0) THEN # Commented out in original FTD code
            if (matly*(2-matly+1)<=0): raise ValueError(f"*** ERROR; LAYER',{ily:>3},"+
                f"REFERS ILLEGAL MATERIAL ID. NO. {matly:>3}")
            else: im[matly]=1

            if(ityly*(21-ityly)<=0): raise ValueError(f"*** ERROR; LAYER',{ily:>3},"+
                f"REFERS ILLEGAL INTEGRATION TYPE NO. {ityly:>3}")

        diff=self.inputs.sth-s
        if (abs(diff)>epsilon): raise ValueError(f"*** ERROR; CHECK LAYER WIDTH/THICKNESSES")
        if (jj != self.inputs.nl): raise ValueError(f"*** ERROR; CHECK INPUT DATA NLY(ILY) AND NL")

        # Commented out original FTD code
        # DO 150 K=1,NMAT
        # do 150 k=1,2
        # IF(IM(K).EQ.0) THEN
        #     IER=IER+1
        #     WRITE(imsg,33) K
        #     FORMAT(/3X,' *** ERROR; MATERIAL WITH ID. NO.',I3,  
        #             '  IS NOT USED')
        #     ENDIF
        # CONTINUE

        s = 0.e0
        jj = 0 
        for iz in range(nz):
            s += self.inputs.elz[iz] 
            jj += self.inputs.ncz[iz]
        diff = self.inputs.slen - s 
        if (abs(diff)>epsilon): raise ValueError(f"*** ERROR; CHECK ZONE LENGTHS")
        if (jj != self.inputs.nc): raise ValueError(f"*** ERROR; CHECK INPUT DATA NCZ(IZ) AND NC")


    def apply_symmetry_planes(self, const):

        for i in range(self.nn):

            # Coordinated planes as symmetry planes 
            if (abs(self.x[0,i])<=const.epsilon and self.inputs.icfx==1): self.ncr[0,i] =2
            if (abs(self.x[1,i])<=const.epsilon and self.inputs.icfy==1): self.ncr[1,i] =2
            if (abs(self.x[2,i])<=const.epsilon and self.inputs.icfz==1): self.ncr[2,i] =2

            # Additional [arallel planes
            if (abs(self.x[0,i]-self.inputs.cplx)<=const.epsilon and self.inputs.iplx==1): self.ncr[0,i]=2
            if (abs(self.x[1,i]-self.inputs.cply)<=const.epsilon and self.inputs.iply==1): self.ncr[1,i] =2
            if (abs(self.x[2,i]-self.inputs.cplz)<=const.epsilon and self.inputs.iplz==1): self.ncr[2,i] =2


    def attach_material(self, const, materials):

        # Can't have this in the initialisation as "nipt" is calculated when the mesh is generated
        self.elm = np.zeros((self.mel, self.nipt), dtype='float')

        reinf = materials.materials["reinforcements"][self.inputs.mref]
        matrix = materials.materials["matrixes"][self.inputs.mmat]

        igau = 0
        for ie in range(self.ne):
            mc    = self.mctabl[ie]
            mat   = self.mcon[mc+self.inputs.nelem]
            npint = self.ngauss[ie]
            for _ in range(npint):
                if(mat==1):
                    self.elm[7,igau]  = reinf["r_y0"]
                    self.elm[16,igau] = reinf["r_y0"]
                    self.elm[20,igau] = const.r_lambda
                    self.elm[21,igau] = const.r_miu
                elif(mat==2):
                    self.elm[7,igau]  = matrix["xm_y0"]
                    self.elm[16,igau] = matrix["xm_y0"]
                    self.elm[20,igau] = const.xm_lambda
                    self.elm[21,igau] = const.xm_miu
                    self.elm[22,igau] = matrix["s0anand"]
                    self.elm[36,igau] = const.xm_lambda
                    self.elm[37,igau] = const.xm_miu
                    self.elm[38,igau] = matrix["s0anand"]
                else: raise ValueError("Material not found")
                igau += 1

    def calc_global_stiffness_matrix(self):

        ieq = 0
        for i in range(self.nn):
            for j in range(3):
                self.id[j,i] = ieq
                ieq+=1
        neq = ieq

        for ie in range(self.ne):
            mc  = self.mctabl[ie]
            nel = self.nnode[ie]
            for inl in range(nel):
                ii = self.mcon[mc+inl]
                for i in range(3):
                    ieq = self.id[i,ii-1] #TODO - have to add the -1 here or else the matrix goes out of bounds
                    for jnl in range(nel):
                        jn = self.mcon[mc+jnl]
                        for j in range(3):
                            jeq = self.id[j,jn -1] #TODO - have to add the -1 here or else the matrix goes out of bounds
                            m = max(ieq,jeq)
                            self.jdiag[m] = max(self.jdiag[m],abs(ieq-jeq))

        self.jdiag[0] = 0
        for jeq in range(1,neq):
            self.jdiag[jeq] += self.jdiag[jeq-1]+1


        #TODO-Same code repeated with minor modifications, FTD original seems to suggest that it is optimising in some way?

        ieq = 0
        for i in range(self.nn):
            for j in range(3):
                if (self.ncr[j,i]<=1):
                    self.id[j,i] = ieq
                    ieq+=1
                else: self.id[j,i] =0
        neq = ieq


        for ie in range(self.ne):
            mc  = self.mctabl[ie]
            nel = self.nnode[ie]
            for inl in range(nel):
                ii = self.mcon[mc+inl]
                for i in range(3):
                    ieq = self.id[i,ii-1] #TODO - have to add the -1 here or else the matrix goes out of bounds
                    if (ieq!=0):
                        for jnl in range(nel):
                            jn = self.mcon[mc+jnl] 
                            for j in range(3):
                                jeq = self.id[j,jn-1] #TODO - have to add the -1 here or else the matrix goes out of bounds
                                if (jeq!=0):
                                    m = max(ieq,jeq)
                                    self.jdiag[m] = max(self.jdiag[m],abs(ieq-jeq))

        self.jdiag[0] = 0
        for jeq in range(1,neq):
            self.jdiag[jeq] += self.jdiag[jeq-1]+1