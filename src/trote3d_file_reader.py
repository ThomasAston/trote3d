import os

def format_line(lines, type, line, end, start=0):
    if (type==int): return list(map(int,lines[line].split()[start:end]))
    else: return list(map(float,lines[line].replace('d', 'e').split()[start:end]))
    
class Trote3d_file_reader:

    def __init__(self, filename, version):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../input_files/', filename)
        file = open(filename, 'r')
        lines = file.readlines()
        file.close()
        self.fprnome = str.split(lines[0])[0]
        self.ninici, self.nimax, self.nrmax, self.ngrav = format_line(lines, int, 2, 4)
        self.nmalh, self.ncondl, self.noptim, self.nph, self.irs = format_line(lines, int, 3, 5)
        self.phi, self.delta, self.deptol = format_line(lines, float, 4, 3)
        self.t0, self.tfim = format_line(lines, float, 5, 2)
        self.dt, self.varr = format_line(lines, float, 6, 2)

        line_count = 8  # Need to check how this might vary
        if (self.nmalh==1):
            self.malhdr, self.nelem = format_line(lines, int, line_count, 2)
            self.nl, self.nc, self.nh = format_line(lines, int, line_count+1, 3)
            self.sth, self.slen, self.shig = format_line(lines, float, line_count+2, 3)
            self.nlay, self.nz, self.nmat = format_line(lines, int, line_count+3, 3)
            line_count += 4

            # Mesh definition
            self.thl,self.nly, self.matl, self.nityp = [],[],[],[]
            self.elz, self.ncz = [],[]
            for i in range(self.nlay):
                temp = lines[line_count].split()[0:4]
                self.thl.append(float(temp[0].replace('d', 'e')))
                self.nly.append(int(temp[1]))
                self.matl.append(int(temp[2]))
                self.nityp.append(int(temp[3]))
                line_count+=1

            for i in range(self.nz):
                temp = lines[line_count].split()[0:3]
                self.elz.append(float(temp[0].replace('d', 'e')))
                self.ncz.append(int(temp[1]))
                line_count+=1

        else: line_count = 12 + self.nlay + self.nz # Looks like the file type is fixed and these lines are just skipped
        
        # Boundary conditions
        if (self.ncondl==0):
            line_count+=1
            self.icfx, self.icfy, self.icfz = format_line(lines, int, line_count, 3)
            line_count+=1
            self.iplx, self.iply, self.iplz = format_line(lines, int, line_count, 3)
            line_count+=1
            self.cplx, self.cply, self.cplz = format_line(lines, float, line_count, 3)
            line_count+=2
        else: line_count +=5

        # Material definition
        self.mref, self.mmat = format_line(lines, int, line_count, 2)
        line_count +=2

        # Saidas para exterior (Outings to the outside?)
        self.ipgau, self.ipecr, self.ipmsg1 = format_line(lines, int, line_count, 3)

        if (self.ninici!=1):
            line_count +=2
            self.reinome = lines[line_count].split()[0]
        else: # Not checking version if reinitialising? Seems strange.
            line_count+=4
            if(lines[line_count][50:55]!=version):
                raise ValueError("You are not using the latest version of the Data Input File \n"+
                "Please use version " + version + "\n" + "Thank you ...")

        if(self.nmalh!=1): raise ValueError("nmalh must be set to 1, code cannot currenly load COSMOS/M files")