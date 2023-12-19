import json
import yaml
from jinja2 import Template, Environment,  FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))

def load_json_data_from_file(file_path):
    verify_path(file_path)
    if verify_path(file_path) == False:
        print(f"File {file_path} not found")
        return False
    else:
        with open(file_path)as json_file:
            data=json.load(json_file)
            return data


def load_yaml_data_from_file(file_path):
    verify_path(file_path)
    if verify_path(file_path) == False:
        print(f"File {file_path} not found")
        return False
    else:
        with open(file_path)as yaml_file:
            data = yaml.safe_load(open(file_path))
            return data


def render_network_config(template_name, data):
    template = env.get_template(template_name)
    return template.render(data)


def save_built_config(file_name, data):
    with open(file_name, 'w') as config_file:
        config_file.write(data)
    return True

# ------ create vlan confs ------------------------------------------------------------
def create_vlan_config_cpe_marseille():
    """
        Must return two values : router config and the switch config
    """
    load_json_data_from_file(file_path='data/vlan_ESW2.json')
    load_json_data_from_file(file_path='data/vlan_R02.json')
    return render_network_config('vlan_router.j2', r2_datajson()), render_network_config('vlan_switch.j2', esw2_datajson())
    

def create_vlan_config_cpe_paris():
    """
        Must return two values : router config and the switch config
    """
    load_json_data_from_file(file_path='data/vlan_ESW3.json')
    return render_network_config('vlan_router.j2', r3_datajson()), render_network_config('vlan_switch.j2', esw3_datajson())


# ------ create ospf confs ------------------------------------------------------------

def create_ospf_config_cpe_marseille():
    try:
        load_json_data_from_file(file_path='data/ospf_r02.json')
        return render_network_config('ospf.j2', r2_ospf_datajson())
    except Exception as e:
        print(f"Une erreur s'est produite lors de la mise en place ospf Marseille : {str(e)}")
        return None


def create_ospf_config_cpe_lyon():
    try:
        load_json_data_from_file(file_path='data/ospf_r02.json')
        return render_network_config('ospf.j2', r1_ospf_datajson())
    except Exception as e:
        print(f"Une erreur s'est produite lors de la mise en place ospf Lyon : {str(e)}")
        return None
    
    
def create_ospf_config_cpe_paris():
    try:
        load_json_data_from_file(file_path='data/ospf_r02.json')
        return render_network_config('ospf.j2', r3_ospf_datajson())
    except Exception as e:
        print(f"Une erreur s'est produite lors de la mise en place ospf paris : {str(e)}")
        return None
    

# ------ verify path ------------------------------------------------------------
def verify_path(file_path):
    try:
        with open(file_path) as f:
            pass
    except FileNotFoundError:
        print(f"File {file_path} not found")
        return False


# ------ data -----------------------------------------------------------------
def r2_datajson():
    return load_json_data_from_file(file_path='data/vlan_ESW2.json')
    
def esw2_datajson():
    return load_json_data_from_file(file_path='data/vlan_R02.json')

def r2_datayaml():
    return load_yaml_data_from_file(file_path='data/vlan_R02.yaml')

def esw2_datayaml():
    return load_yaml_data_from_file(file_path='data/vlan_ESW2.yaml')

def esw3_datajson():
    return load_json_data_from_file(file_path='data/vlan_ESW3.json')

def r3_datajson():
    return load_json_data_from_file(file_path='data/vlan_R03.json')

def r1_ospf_datajson():
    return load_json_data_from_file(file_path='data/ospf_R01.json')

def r2_ospf_datajson():
    return load_json_data_from_file(file_path='data/ospf_R02.json')

def r3_ospf_datajson():
    return load_json_data_from_file(file_path='data/ospf_R03.json')

def ospf_datajson():
    return load_json_data_from_file(file_path='data/ospf.json')


# ------ main -----------------------------------------------------------------
if __name__ == "__main__":
    """
        Appeler les fonctions de création et de sauvegarde des configurations
    """
    save_built_config('config/ospf_R01.conf', r01_osfp_config)
    
    r02_config, esw2_config = create_vlan_config_cpe_marseille()
    #save_built_config('config/vlan_R02.conf', r02_config)
    #save_built_config('config/vlan_ESW2.conf', esw2_config)
    
    r03_config, esw3_config = create_vlan_config_cpe_paris()
    # save_built_config('config/vlan_R03.conf', r03_config)
    # save_built_config('config/vlan_ESW3.conf', esw3_config)
