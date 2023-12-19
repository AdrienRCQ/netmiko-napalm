import json
from napalm import get_network_driver
import create_config as cc


def get_inventory():
    with open("inventory/hosts.json") as f:hosts = json.load(f)
    return hosts

def get_routers():
    with open("inventory/routers.json") as f:routers = json.load(f)
    return routers

def get_json_data_from_file(file):
    pass

def question_26(device):
    #envoie la commande show interfaces au device.
    command ='sh int'
    result = device.cli([command])
    print(result)
    return result
    

def question_27(device):
    try:
        output = question_26(device)
        type_output = type(output)
        print(type_output)
        if output:
            # Récupérez la première clé en utilisant la méthode next(iter(dictionary))
            first_key = next(iter(output))
            print(first_key)
            return first_key
        else:
            # Si le dictionnaire est vide, on renvoie None pour la clé 
            return None
        
    except Exception as e:
        # Gérez les erreurs éventuelles, par exemple si le dictionnaire n'est pas sérialisable en JSON
        print(f"Une erreur s'est produite : {str(e)}")
        return None


def question_28(device):
    #récupère la table ARP du routeur R1
    try:
        arp_table = device.get_arp_table()
        print(arp_table)
        return arp_table
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération de la table ARP : {str(e)}")
        return None


def question_29(device):
    #récupère le type de l'objet retourné par la fonction question 28
    output_28 = question_28(device)
    outputype = type(output_28)
    print(outputype)
    return outputype


def question_30(device):
    with open("config/loopback_R01.conf") as f:
        config = f.read()
    output = device.load_merge_candidate(filename="config/loopback_R01.conf")
    device.commit_config() #sauvegarde la configuration
    print(output)
    zim = question_26(device)
    print(zim)


def question_31():
    r01_osfp_config = cc.create_ospf_config_cpe_lyon()
    print(r01_osfp_config)
    
    r02_ospf_config = cc.create_ospf_config_cpe_paris()
    print(r02_ospf_config)
    
    r03_ospf_config = cc.create_ospf_config_cpe_paris()
    print(r03_ospf_config)
    
    return True
    


def question_32(routers):
    try:
        for router in routers:
            hostname = router["hostname"]
            var_temp = {
                'device_type': router["device_type"],
                'host': router["host"],
                'username': router["username"],
                'password': router["password"]
            }

            # Définit le fichier de config à utiliser :
            config_file = "config/ospf" + router["hostname"] + ".conf"
            print(config_file)
            
            # Envoye la configuration au périphérique
            device.load_merge_candidate(filename="config/loopback_R01.conf")

            # Enregistre la configuration
            device.commit_config() #sauvegarde la configuration

            print("Configuration envoyée avec succès.")

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")


def question_34():
    try:
        for host in hosts:
            hostname = host["hostname"]
            var_temp = {
                'device_type': host["device_type"],
                'host': host["host"],
                'username': host["username"],
                'password': host["password"]
            }

            data = host.get_config()
            filename = "backup/" + host["hostname"] + ".bak"
            file1 = open(filename, "w")
            file1.write(data)
            file1.close()

            print("Configuration sauvegarder avec succès.")

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")



if __name__ == "__main__":
    r01 = {
    'hostname': '172.16.100.62',
    'username': 'cisco',
    'password': 'cisco'
    }

    driver = get_network_driver('ios') # le driver est ios
    device = driver(**r01)
    device.open()
    
    hosts = get_inventory() # Récupération des hosts via le fichier hosts.json
    routers = get_routers() # Récupération des routeurs via la fonction get_routers
    
    #question_26(device)
    #question_27(device)
    #question_28(device)
    #question_29(device)
    #question_30(device)
    #question_31()
    #question_32()
    #question_34()
    
    
    
