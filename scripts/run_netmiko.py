import json
from netmiko import ConnectHandler


def question_9(net_connect):
    # Affichez, l’adresse ip et le device type de l’objet net_connect
    print(net_connect.host)
    print(net_connect.device_type)
    return net_connect.host, net_connect.device_type


def question_10(net_connect):
    # send command to the remote device
    output = net_connect.send_command("show ip int brief")
    print(output)
    return output


def question_11(net_connect):
    # Utilisez le paramètre use_textfsm=True à la commande de la question précédente et affichez le résultat, que remarquez-vous ?
    output = net_connect.send_command("show ip int brief", use_textfsm=True)
    return output


def question_12(net_connect):
    output = net_connect.send_command("show ip route", use_textfsm=True)
    return output


def question_13(net_connect):
    output = net_connect.send_command("show ip int brief", use_textfsm=True)
    print(output)
    for interface in output:
        print(net_connect.send_command(f"show run int {interface['intf']}"))
    return output


def question_14(net_connect):
    output = net_connect.send_config_set(["interface Loopback1", "ip address 192.168.1.1 255.255.255.255", "description 'loopback interface from netmiko'", "no shut"])
    net_connect.save_config()
    print(output)


def question_15(net_connect):
    output = net_connect.send_config_set("no interface Loopback1")
    net_connect.save_config()
    print(output)


def question_16(net_connect):
    with open("config/loopback_R01.conf") as f:
        config = f.read()
    output = net_connect.send_config_set(config)
    net_connect.save_config()
    print(output)


def question_17(net_connect):
    output = net_connect.send_config_set("no interface Loopback1\nno interface Loopback2\nno interface Loopback3\nno interface Loopback4")
    net_connect.save_config()
    print(output)


def get_inventory():
    with open("inventory/hosts.json") as f:
        hosts = json.load(f)
    return hosts


def question_20(net_connect, hosts):
    for host in hosts:
        if "R" in host["hostname"]:
            output = net_connect.send_command(f"show run interface Gigabit0/0.99", use_textfsm=True)
            print(output)


def question_21(hosts):
    try:
        for host in hosts:
            hostname = host["hostname"]
            var_temp = {
                'device_type': host["device_type"],
                'host': host["host"],
                'username': host["username"],
                'password': host["password"]
            }

            # Instancier la connexion SSH
            connect = ConnectHandler(**var_temp)

            # Se connecte au périphérique en mode configuration
            connect.config_mode()

            # Définit le fichier de config à utiliser :
            config_file = "config/vlan_" + host["hostname"] + ".conf"
            print(config_file)

            # Ouvre le fichier de configuration en mode lecture
            with open(config_file, "r") as file:
                config_data = file.read()
            print(config_data)

            # Envoye la configuration au périphérique
            output = connect.send_config_from_file(config_file, exit_config_mode=False)

            # Enregistre la configuration (facultatif)
            output += connect.save_config()

            # Ferme la connexion
            connect.disconnect()

            print("Configuration envoyée avec succès.")
            print(output)

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")


if __name__ == "__main__":
    r01 = {
        'device_type': 'cisco_ios',
        'host': '172.16.100.62',
        'username': 'cisco',
        'password': 'cisco'
    }

    net_connect = ConnectHandler(**r01)
    hosts = get_inventory()

    # print(net_connect)
    # print type of net_connect
    # print(type(net_connect))
    # question_9(net_connect)
    # question_10(net_connect)
    # question_11(net_connect)
    # question_12(net_connect)
    # question_13(net_connect)
    # question_14(net_connect)
    # question_15(net_connect)
    # question_16(net_connect)
    # question_17(net_connect)
    # print(hosts)
    # question_20()
    # question_21()
