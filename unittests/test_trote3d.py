import unittest

from src.trote3d_file_reader import Trote3d_file_reader
from src.trote3d_mesh import Trote3d_mesh
from src.trote3d_logger import Trote3d_logger
from src.trote3d_material_loader import Trote3d_material_loader
from src.trote3d_constants import Trote3d_constants
from src.trote3d_elements import Trote3d_elements
from src.trote3d_time_integration import Trote3d_time_integration
from src.trote3d_temperature_integration import Trote3d_temperature_integration

class test_Trote3d_material_loader(unittest.TestCase):

    def test_material_loader(self):
        # Specifying the test material with known parameters
        material = 'materials.json'
        
        # Loading the test material
        materials = Trote3d_material_loader(material)

        reinfs = materials.materials["reinforcements"]
        matrixes = materials.materials["matrixes"]
        
        # Tests to check that the material has been loaded correctly
        self.assertEqual(reinfs[0]["name"   ],'reinf1')
        self.assertEqual(reinfs[0]["r_mody" ],4.1e5)
        self.assertEqual(reinfs[0]["r_poiss"],0.24e0)
        self.assertEqual(reinfs[0]["r_y0"   ],0.0e0)
        self.assertEqual(reinfs[0]["r_alfa" ],0.43e-5)

        self.assertEqual(reinfs[1]["name"   ],'testreinf')
        self.assertEqual(reinfs[1]["r_mody" ],4.1e5)
        self.assertEqual(reinfs[1]["r_poiss"],0.24e0)
        self.assertEqual(reinfs[1]["r_y0"   ],0.0e0)
        self.assertEqual(reinfs[1]["r_alfa" ],0.43e-5)

        self.assertEqual(matrixes[0]["name"     ], "mat1")
        self.assertEqual(matrixes[0]["xm_mody"  ], 0.448e5)
        self.assertEqual(matrixes[0]["xm_poiss" ], 0.357e0)
        self.assertEqual(matrixes[0]["xm_y0"    ], 0.0e0)
        self.assertEqual(matrixes[0]["xm_alfa"  ], 0.287e-4)
        self.assertEqual(matrixes[0]["hf"       ], 5.0e-1)
        self.assertEqual(matrixes[0]["hg"       ], 5.0e-1)
        self.assertEqual(matrixes[0]["hh"       ], 5.0e-1)
        self.assertEqual(matrixes[0]["hl"       ], 1.5e0)
        self.assertEqual(matrixes[0]["hm"       ], 1.5e0)
        self.assertEqual(matrixes[0]["hn"       ], 1.5e0)
        self.assertEqual(matrixes[0]["aanand"   ], 1.91e7)
        self.assertEqual(matrixes[0]["qanand"   ], 1.7535e5)
        self.assertEqual(matrixes[0]["csianand" ], 7.00e0)
        self.assertEqual(matrixes[0]["emanand"  ], 0.23348e0)
        self.assertEqual(matrixes[0]["anann"    ], 0.07049e0)
        self.assertEqual(matrixes[0]["s0anand"  ], 18.0e0)
        self.assertEqual(matrixes[0]["ansbar"   ], 18.9e0)
        self.assertEqual(matrixes[0]["anh0"     ], 1115.6e0)
        self.assertEqual(matrixes[0]["anana"    ], 1.3e0)

        self.assertEqual(matrixes[1]["name"     ], "testmat")
        self.assertEqual(matrixes[1]["xm_mody"  ], 0.448e5)
        self.assertEqual(matrixes[1]["xm_poiss" ], 0.357e0)
        self.assertEqual(matrixes[1]["xm_y0"    ], 0.0e0)
        self.assertEqual(matrixes[1]["xm_alfa"  ], 0.287e-4)
        self.assertEqual(matrixes[1]["hf"       ], 5.0e-1)
        self.assertEqual(matrixes[1]["hg"       ], 5.0e-1)
        self.assertEqual(matrixes[1]["hh"       ], 5.0e-1)
        self.assertEqual(matrixes[1]["hl"       ], 1.5e0)
        self.assertEqual(matrixes[1]["hm"       ], 1.5e0)
        self.assertEqual(matrixes[1]["hn"       ], 1.5e0)
        self.assertEqual(matrixes[1]["aanand"   ], 1.91e7)
        self.assertEqual(matrixes[1]["qanand"   ], 1.7535e5)
        self.assertEqual(matrixes[1]["csianand" ], 7.00e0)
        self.assertEqual(matrixes[1]["emanand"  ], 0.23348e0)
        self.assertEqual(matrixes[1]["anann"    ], 0.07049e0)
        self.assertEqual(matrixes[1]["s0anand"  ], 18.0e0)
        self.assertEqual(matrixes[1]["ansbar"   ], 18.9e0)
        self.assertEqual(matrixes[1]["anh0"     ], 1115.6e0)
        self.assertEqual(matrixes[1]["anana"    ], 1.3e0)


class test_Trote3d_constants(unittest.TestCase):
    def setUp(self):
        self.constants = Trote3d_constants()
    
    # def tearDown(self):
    #     self.constants.CODEFORTEARDOWN()

    def test_constants_calc_material_constants(self):
        # Specifying the test material with known parameters
        material = 'materials.json'
        
        # Loading the test material
        materials = Trote3d_material_loader(material)
        
        # Calculating the material constants of the test material
        self.constants.calc_material_constants(materials, 0, 0)

        # Tests to check that the material constants are calculated correctly
        self.assertAlmostEqual(self.constants.r_lambda,0.24e0*4.1e5/((1.0e0+0.24e0)*(1.0e0-2.0e0*0.24e0)))
        self.assertAlmostEqual(self.constants.r_miu,4.1e5/(2.0e0*(1.0e0+0.24e0)))
        self.assertAlmostEqual(self.constants.r_kapa,self.constants.r_lambda+self.constants.r_miu*2.e0/3.e0)
        self.assertAlmostEqual(self.constants.xm_lambda,0.357e0*0.448e5/((1.0e0+0.357e0)*(1.0e0-2.0e0*0.357e0)))
        self.assertAlmostEqual(self.constants.xm_miu,0.448e5/(2.0e0*(1.0e0+0.357e0)))
        self.assertAlmostEqual(self.constants.xm_kapa,self.constants.xm_lambda+self.constants.xm_miu*2.e0/3.e0)

    def test_constants_set_temp_and_time_variables(self):
        
        # Load the input file and store the paramters
        input_variables = Trote3d_file_reader('Tinput.tro', version="1.03b")
        
        self.constants.set_temp_and_time_variables(input_variables)
        
        # Tests to check that the material constants are calculated correctly
        self.assertAlmostEqual(self.constants.temp,933.00)
        self.assertAlmostEqual(self.constants.dtemp,-1.0e2*1.0e-2)
        self.assertAlmostEqual(self.constants.t,0.e0)
        self.assertAlmostEqual(self.constants.dtn,0.e0)

if __name__ == '__main__':
    unittest.main()
