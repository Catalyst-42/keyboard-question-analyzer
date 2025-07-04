class PhysicalKey():
    def __init__(self):
        self.name
        self.x
        self.y
        self.w
        self.h
        self.row
        self.hand    


class Key():
    def __init__(self, physical_key: str, physical_key_mapping: dict, is_control_key: bool):
        self.physical_key = physical_key
        self.physical_key_mapping = physical_key_mapping
        self.is_control_key = is_control_key


class Keyboard():
    def __init__(self, physical_layout: dict, logical_layout: dict, keys_frequencies: dict):
        self.physical_layout = physical_layout
        self.logical_layout = logical_layout
        self.keys_frequencies = keys_frequencies
    
    def get_legend(self, physical_key: str, layer: int):
        if physical_key in self.logical_layout["Controls"]:
            return self.logical_layout["Controls"][physical_key]["Icon"]

        elif physical_key in self.logical_layout["Mappings"]:
            return self.logical_layout["Mappings"][physical_key][str(layer)]

        else:
            return ""

    def get_key(self, physical_key: str):
        physical_spec = self.physical_layout.get(physical_key, {None})

    #    return Key(physical_specs, ) 
    
    