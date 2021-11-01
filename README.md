# PyTrote3d
## Table of contents
* [About](#about)
* [Technologies](#technologies)
* [Setup](#setup)
* [To do](#to_do)


## About
PyTrote3d is a Python implementation of the Fortran 90 code Trote3D as written by Filipe Teixeira-Dias as part of his PhD thesis *Numerical simulation of tensile and shear tests in plane strain and plane stress* [[1][1]].  
	
## Technologies
Project is created with:
* Python 3.8.10
	
## Setup
To run this project, enter

```
$ cd ../pytrote3d
$ python3 trote_3d.py
```

The file that is run and the materials which are used are currently set in trote_3d.py by the following lines

```
# Input file and materials file
filename = 'Tinput.tro'
material = 'materials.json'
```
## To do
- [ ] Complete conversion of Fortran 90 code to Python 3 and complete verification.
- [ ] Specify input file and material when running command, not in python file.
- [ ] Investigate application of multiprocessing.

## Citations
1. Teixeira-Dias, F. (1995). *Numerical simulation of tensile and shear tests in plane strain and plane stress* (Doctoral dissertation)


[1]: https://www.researchgate.net/publication/237021517_Numerical_simulation_of_tensile_and_shear_tests_in_plane_strain_and_plane_stress



