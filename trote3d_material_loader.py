import json

class Trote3d_material_loader:

    def __init__(self, material_file_name):
        f = open(material_file_name,)
        self.materials = json.load(f, object_hook=float_object_hook)
        f.close()

def float_object_hook(obj):
    """If a value in obj is a string, try to convert it to a float"""
    rv = {}
    for k, v in obj.items():
        if isinstance(v, str):
            try:
                rv[k] = float(v)
            except ValueError:
                rv[k] = v
        else:
            rv[k] = v
    return rv
