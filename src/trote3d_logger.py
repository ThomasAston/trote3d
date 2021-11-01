import logging

class Trote3d_logger:

    def __init__(self,filename):
        logging.basicConfig(filename="../logs/"+filename+".log", level=logging.DEBUG, filemode='w', format='%(message)s')
    
    def log_inputs_and_mesh(self, in_vars, mesh):
        logging.info('Mesh definition: \n-------------------------------------')
        logging.info(f'MALHDR   = {in_vars.malhdr:>5} - Direction of mesh generation \n'+
                     f'NL       = {in_vars.nl:>5} - Number of rows of elements \n'+
                     f'NC       = {in_vars.nc:>5} - Number of element columns \n'+
                     f'NH       = {in_vars.nh:>5} - Number of element layers \n'+
                     f'NN       = {mesh.nn:>5} - Total number of nodes \n'+
                     f'NE       = {mesh.ne:>5} - Total number of elements \n'+
                     f'NELEM    = {in_vars.nelem:>5} - Number of nodes per element \n'+
                     f'NNODT    = {mesh.nnodt:>5} - MCON table dimension \n')
 
        if (in_vars.ninici==1):
            logging.info('Calculation parameters: \n-------------------------------------')
            logging.info(f'NINICI = {in_vars.ninici:>11} - Passo inicial dos incrementos\n' +
                            f'NIMAX  = {in_vars.nimax:>11} - Num max incrementos de tempo\n' +
                            f'NRMAX  = {in_vars.nrmax:>11} - Num max tentativas de reducao incr\n' +
                            f'NGRAV  = {in_vars.ngrav:>11} - Periodicidade de gravacao de *.ffr\n' +
                            f'NMALH  = {in_vars.nmalh:>11} - Origem da Malha (0 = gerada pelo codigo, 1 = exterior)\n' +
                            f'NCONDL = {in_vars.ncondl:>11} - Origem das condicoes limites: (0 = geradas pelo codigo 1 = exteriores)\n' +
                            f'NOPTIM = {in_vars.noptim:>11} - Optimizacao (1-Sim, 0-Nao)\n' +
                            f'NPH    = {in_vars.nph:>11} - Corr. P. hidro. (1-Sim, 0-Nao)\n' +
                            f'IRS    = {in_vars.irs:>11} - Integracao reduzida selectiva\n' +
                            f'PHI    = {in_vars.phi:11.3e} - Valor Phi para a integracao\n' +
                            f'DELTA  = {in_vars.delta:11.3e} - Parametro de optimizacao\n' +
                            f'T0     = {in_vars.t0:11.3e} - Temperatura incial do processo\n' +
                            f'TFIM   = {in_vars.tfim:11.3e} - Temperatura final do processo\n' +
                            f'DT     = {in_vars.dt:11.3e} - Incremento de tempo inicial\n' +
                            f'VARR   = {in_vars.varr:11.3e} - Velocidade de arrefecimento \n')

            logging.info('Definicao das saidas para o exterior: \n-------------------------------------')
            logging.info(f'IPGAU  = {in_vars.ipgau:>11} - Ponto de Gauss de recolha de valores\n' +
                            f'IPECR  = {in_vars.ipecr:>11} - Periodicidade de escrita para ecran\n' +
                            f'IPMSG1 = {in_vars.ipmsg1:>11} - Periodicidade de escrita para MSG1 \n')

            logging.info('Boundary conditions : \n-------------------------------------')
            logging.info(f'ICFY = {in_vars.icfy:>11} - Plano coordenado Y=0 de simetria\n' +
                            f'ICFZ = {in_vars.icfz:>11} - Plano coordenado Z=0 de simetria\n' +
                            f'IPLX = {in_vars.iplx:>11} - Plano adicional fixo paralelo a X=0\n' +
                            f'IPLY = {in_vars.iply:>11} - Plano adicional fixo paralelo a Y=0\n' +
                            f'IPLZ = {in_vars.iplz:>11} - Plano adicional fixo paralelo a Z=0\n' +
                            f'CPLX = {in_vars.cplx:11.3e} - Coordenada em Ox do plano adicional\n' +
                            f'CPLY = {in_vars.cply:11.3e} - Coordenada em Oy do plano adicional\n' +
                            f'CPLZ = {in_vars.cplz:11.3e} - Coordenada em Oz do plano adicional \n')
                        

    def log_mesh_data(self, in_vars, mesh, corner_nodes):
        logging.info('Basic mesh information: \n-------------------------------------')

        if (in_vars.malhdr==1):
            logging.info(f'STH      = {in_vars.sth:10.4f} - Initial width of the sheet \n'+
                         f'SLEN     = {in_vars.slen:10.4f} - Initial X1-length of the sheet \n'+
                         f'SHIG     = {in_vars.shig:10.4f} - Initial thickness of the sheet \n'+
                         f'NLAY     = {in_vars.nlay:10.4f} - Number of layers along sheet width \n'+
                         f'NZ       = {in_vars.nz:10.4f} - Number of zones along sheet length \n')

        elif(in_vars.malhdr==2):
            logging.info(f'STH      = {in_vars.sth:10.4f} - Initial width of the sheet \n'+
                         f'SLEN     = {in_vars.slen:10.4f} - Initial X1-length of the sheet \n'+
                         f'SHIG     = {in_vars.shig:10.4f} - Initial width of the sheet \n'+
                         f'NLAY     = {in_vars.nlay:10.4f} - Number of layers along thickness \n'+
                         f'NZ       = {mesh.nz:10.4f} - Number of zones along sheet length \n')

        else: raise ValueError("Mesh direction must be either '1' or '2'")

        logging.info('   Layer  wid/thick  No.rows  Mat.id.no  ITYPE')
        for i in range(in_vars.nlay):
            logging.info(f'{i+1:>6}   {in_vars.thl[i]:10.3f}{in_vars.nly[i]:>7}{in_vars.matl[i]:>9}{in_vars.nityp[i]:>9}')
        logging.info(' ')

        logging.info('   Zone      length   No. of columns')
        for i in range(in_vars.nz):
            logging.info(f'{i+1:>6}   {in_vars.elz[i]:10.3f}{in_vars.ncz[i]:>9}')
        logging.info(' ')

        logging.info('   Corner nodes on front surface:'+''.join(f'{i:>6}' for i in corner_nodes[0:4]))
        logging.info('   Corner nodes on back surface::'+''.join(f'{i:>6}' for i in corner_nodes[4:8]))
        logging.info(' ')

        logging.info('   Nodal co-ordinates')
        logging.info('    NODE    X1        X2        X3     ')
        for i in range(mesh.nn):
            logging.info(f'{i+1:>7}'+''.join(f'{j:10.4f}' for j in mesh.xinit[:,i]))
        logging.info(' ')

        logging.info('   Elemental data')
        logging.info('   ELEM MAT ITYPE NINT  NEL INTABL MC      GLOBAL NODES')
        
        nel = in_vars.nelem
        nnod1 = nel+1
        for i in range(mesh.ne):
            mc=mesh.mctabl[i]-1
            logging.info(f'{i+1:>7}{mesh.mcon[mc+nnod1]:>3}'
                    +f'{mesh.ntype[i]:>5}{mesh.ngauss[i]:>5}{mesh.nnode[i]:>5}{mesh.intabl[i]:>5}'
                    +f'{mesh.mctabl[i]:>6}    '
                    +''.join(f'{mesh.mcon[mc+k]:>6}' for k in range(1,nel+1)))
        logging.info(' ')
        
    def log_material_data(self, in_vars, mats):

        rind = in_vars.mref
        mind = in_vars.mmat

        reinf = mats.materials["reinforcements"][rind-1]
        mat = mats.materials["matrixes"][mind-1]

        logging.info('Material Parameters: \n-------------------------------------')
        logging.info(f'R_MODY   ={reinf["r_mody"]:11.3e}  - Modulo de Young do reforco\n'+
                        f'R_POISS  ={reinf["r_poiss"]:11.3e}  - Coefic de Poisson do reforco\n'+
                        f'R_Y0     ={reinf["r_y0"]:11.3e}  - Limite elastico do reforco\n'+
                        f'R_ALFA   ={reinf["r_alfa"]:11.3e}  - Coeficiente de expansao termica do reforco\n'+
                        f'XM_MODY  ={mat["xm_mody"]:11.3e}  - Modulo de Young da matriz\n'+
                        f'XM_POISS ={mat["xm_poiss"]:11.3e}  - Coefic de Poisson da matriz\n'+
                        f'XM_Y0    ={mat["xm_y0"]:11.3e}  - Limite elastico da matriz\n'+
                        f'XM_ALFA  ={mat["xm_alfa"]:11.3e}  - Coeficiente de expansao termica da matriz\n'+
                        f'HF       ={mat["hf"]:11.3e}  - Coeficiente F de anisotropia \n'+
                        f'HG       ={mat["hg"]:11.3e}  - Coeficiente G de anisotropia \n'+
                        f'HH       ={mat["hh"]:11.3e}  - Coeficiente H de anisotropia \n'+
                        f'HL       ={mat["hl"]:11.3e}  - Coeficiente L de anisotropia \n'+
                        f'HM       ={mat["hm"]:11.3e}  - Coeficiente M de anisotropia \n'+
                        f'HN       ={mat["hn"]:11.3e}  - Coeficiente N de anisotropia \n'+
                        f'AANAND   ={mat["aanand"]:11.3e}  - Coeficiente A de Anand\n'+
                        f'QANAND   ={mat["qanand"]:11.3e}  - Coeficiente Q de Anand\n'+
                        f'CSIANAND ={mat["csianand"]:11.3e}  - Coeficiente csi de Anand\n'+
                        f'EMANAND  ={mat["emanand"]:11.3e}  - Coeficiente m de Anand\n'+
                        f'ANANN    ={mat["anann"]:11.3e}  - Coeficiente n de Anand\n'+
                        f'S0ANAND  ={mat["s0anand"]:11.3e}  - Valor inicial de s\n'+
                        f'ANSBAR   ={mat["ansbar"]:11.3e}  - Valor medio de s\n'+
                        f'ANH0     ={mat["anh0"]:11.3e}  - Valor h0 de Anand\n'+
                        f'ANANA    ={mat["anana"]:11.3e}  - Coeficiente a de Anand\n')

    def log_element_types(self, elements):


        logging.info('   FIS, DFILS, PS=')
        string = '\n'.join(f'{elements.fis4[i]:11.4e} '+' '.join(f'{j:11.4e}' 
            for j in elements.dfils4[:,i]) for i in range(4))
        string += f'{elements.ps4:11.4e}'
        logging.info(string)
        logging.info(' ')

        logging.info('   FIS, DFILS, PS=')
        string = '\n'.join(f'{elements.fis6[i]:11.4e} '+' '.join(f'{j:11.4e}' 
            for j in elements.dfils6[:,i]) for i in range(6))
        string += f'{elements.ps6:11.4e}'
        logging.info(string)
        logging.info(' ')

        logging.info('   FIS, DFILS, PS=')
        string = '\n'.join(f'{elements.fis8[i]:11.4e} '+' '.join(f'{j:11.4e}' 
            for j in elements.dfils8[:,i]) for i in range(8))
        string += f'{elements.ps8:11.4e}'
        logging.info(string)
        logging.info(' ')

        logging.info('   FIP, DFILP, PP=')
        string =  '\n'.join('\n'.join(f'{elements.fip6[i,k]:11.4e} '
            +' '.join(f'{j:11.4e}' for j in elements.dfilp6[:,i,k]) 
            for i in range(6)) for k in range(2))
        string += ' '.join(f'{elements.pp6[k]:11.4e}' for k in range(2))
        logging.info(string)
        logging.info(' ')

        logging.info('   FIP, DFILP, PP=')
        string =  '\n'.join('\n'.join(f'{elements.fip8[i,k]:11.4e} '
            +' '.join(f'{j:11.4e}' for j in elements.dfilp8[:,i,k]) 
            for i in range(8)) for k in range(8))
        string += ' '.join(f'{elements.pp8[k]:11.4e}' for k in range(8))
        logging.info(string)
        logging.info(' ')

        logging.info('   DG=')
        string =  '\n'.join(' '.join(' '.join(f'{j:11.4e}' for j in elements.dg[:,i,k]) for i in range(3)) for k in range(8))
        logging.info(string)
        logging.info(' ')

        logging.info('   DDG=')
        string =  ' '.join(f'{j:11.4e}' for j in elements.ddg)
        logging.info(string)
        logging.info(' ')
        