from trote3d_file_reader import Trote3d_file_reader
from trote3d_mesh import Trote3d_mesh
from trote3d_logger import Trote3d_logger
from trote3d_material_loader import Trote3d_material_loader
from trote3d_constants import Trote3d_constants
from trote3d_elements import Trote3d_elements
from trote3d_time_integration import Trote3d_time_integration
from trote3d_temperature_integration import Trote3d_temperature_integration

if __name__ == "__main__":

    # Input file and materials file
    filename = 'Tinput.tro'
    material = 'materials.json'

    # Create an instance of the logger class, pass filename to use as log file name
    log = Trote3d_logger(filename)

    # Load the input file and store the paramters
    input_variables = Trote3d_file_reader('Tinput.tro', version="1.03b")

    # Create an instance of the mesh class and set attributes based on the input file
    mesh = Trote3d_mesh(input_variables, mel=43)

    # Write the parameters loaded from the input file to log file
    log.log_inputs_and_mesh(input_variables,mesh) 

    # Generate the mesh 
    corner_nodes = mesh.generate_mesh()

    # Load the materials file
    materials = Trote3d_material_loader(material)

    # Calculate general purpose and material constants based on material selection in input file
    constants = Trote3d_constants()
    constants.calc_material_constants(materials, input_variables.mref, input_variables.mmat)

    # If this is the first step then log the material data 
    # TODO - This is strange behaviour, why only if not the fist step?
    if (input_variables.ninici==1):
        log.log_material_data(input_variables, materials) # Log the materials chosen

    # Log data corresponding to the mesh that was generated
    log.log_mesh_data(input_variables, mesh, corner_nodes)

    # Initialise the elements class and populate the various element arrays
    # TODO - Seems silly to create all these arrays if only using a subset of them
    elements = Trote3d_elements(constants)

    # Log the element types
    log.log_element_types(elements)

    # Apply symmetry planes defined in the input file
    mesh.apply_symmetry_planes(constants)

    # If this is the first step then:
    if (input_variables.ninici==1):
        # Attach the material specified in the input file (and calculated material constants) to the mesh
        mesh.attach_material(constants, materials)
        # Set the temperature and time variables (T, dT, t, and dt) from the input file
        constants.set_temp_and_time_variables(input_variables)
    else: # Otherwise load these from file
        #TODO - pointless loading old "unformatted" files as we won't
        # be writing this anymore. Needs to be updated with a new format.
        raise ValueError("Cannot yet read from file")

    # Setting up the global stiffness matrix and ids
    mesh.calc_global_stiffness_matrix()

    # Initialising the temperature integration class and using the in-built condition for the while loop 
    temp_int = Trote3d_temperature_integration(constants, input_variables, condition=None)

    # Initialising the time integration class and using the in-built condition for the while loop 
    #TODO - Why is the nrmax from the input file overwritten here?
    time_int = Trote3d_time_integration(input_variables, nred=1, nrmax=10, condition=None)

    # Carrying out the temperature integration with the specified time integration scheme
    temp_int.integrate(input_variables, mesh, constants, time_int)

