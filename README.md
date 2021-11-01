# PyTrote3d [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) 

<a href="https://github.com/younjames/trote3d/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=younjames/trote3d" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

## Table of contents
* [About](#about)
* [Technologies](#technologies)
* [Setup](#setup)
* [To Do](#to_do)
* [Getting Involved](#getting_involved)


## About
PyTrote3d is a Python implementation of the Fortran 90 code Trote3D as written by Filipe Teixeira-Dias as part of his PhD thesis *Numerical simulation of tensile and shear tests in plane strain and plane stress* [[1][1]] [[2][2]].  
	
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
- [ ] Write unit tests.
- [ ] Specify input file and material when running command, not in python file.
- [ ] Investigate application of multiprocessing.

## Getting Involved
For any suggestions, please [create a new issue](https://github.com/younjames/trote3d/issues).

## Citations
1. Teixeira-Dias, F. (1995). *Numerical simulation of tensile and shear tests in plane strain and plane stress* (Doctoral dissertation)
2. Teixeira-Dias, F. and Menezes, L.F. (2001), *Numerical aspects of finite element simulations of residual stresses in metal matrix composites*. Int. J. Numer. Meth. Engng., 50: 629-644.


[1]: https://www.researchgate.net/publication/237021517_Numerical_simulation_of_tensile_and_shear_tests_in_plane_strain_and_plane_stress
[2]: https://doi.org/10.1002/1097-0207(20010130)50:3<629::AID-NME41>3.0.CO;2-7



