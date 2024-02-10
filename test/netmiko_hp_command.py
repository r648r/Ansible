#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from colorama import Fore, Back, Style
from datetime import datetime
import netmiko
import yaml
import os


def yaml_to_netmiko_dico(inventory_local):
    with open(inventory_local, 'r') as f:
        inventory_local = yaml.safe_load(f)
    
    devices = []
    for host in inventory_local['hpProCurve']['hosts'].values():
        device = {
            'device_type': 'hp_procurve',
            'ip': host['ansible_host'],
            'username': inventory_local['hpProCurve']['vars']['ansible_ssh_user'],
            'port': inventory_local['hpProCurve']['vars']['ansible_port'],
            'password': os.environ['PWD_HP'],
            'session_log': f'netmiko_session_{host["ansible_host"]}.log'
        }
        devices.append(device)
    return devices

def configure_hp_procurve(port, public_key, *devices):
    """
    Configure the SSH settings and public key authentication on a list of HP ProCurve devices.

    Args:
        port (int): The TCP port to use for SSH connections.
        public_key (str): The public key string to deploy on the devices.
        *devices (dict): Variable-length argument list of dictionaries, where each dictionary contains the device
                         connection details, including the IP address, username, and password.

    Returns:
        None.

    Raises:
        NetmikoAuthenticationException: If the SSH authentication fails for any of the devices.
        NetmikoTimeoutException: If the connection to any of the devices times out.

    Note:
        The function sends the following configuration commands to the devices:
        - no telnet-server
        - ip ssh port <port>
        - ip ssh cipher aes256-cbc
        - ip ssh mac hmac-sha1
        - ip ssh filetransfer
        - aaa authentication ssh login public-key none
        - aaa authentication ssh enable public-key
        It also deploys the provided public key on the devices and displays the execution time for each device.
        If a timeout occurs during the deployment of the public key, the function will print a message indicating
        that the deployment was successful, but with a small timeout issue.

    """
    commands = [
        "no telnet-server",
        f"ip ssh port {port}",
        "ip ssh cipher aes256-cbc",
        "ip ssh mac hmac-sha1",
        "ip ssh filetransfer",
        "aaa authentication ssh login public-key none",
        "aaa authentication ssh enable public-key"
    ]
    for device in devices:
        try:
            with netmiko.ConnectHandler(**device) as connection:
                start_time = datetime.now()
                output = connection.send_config_set(commands)
                try:
                    output += connection.send_command(
                        f"ip ssh public-key manager '{public_key}'",
                        expect_string=r"#", 
                        read_timeout=100)
                    # Cette commande réalise constament un timeout elle est donc traité a l'écart des autres pour pouvoir affiché les commande executé
                except netmiko.exceptions.ReadTimeout:
                    timeout = True
                    print(f"{Back.BLUE}Déploiment réussit !{Style.RESET_ALL} : Petit soucis de timeout mais rien de grave\n")
                    print(f"{Fore.BLUE}Commande de vérification : {Style.RESET_ALL}")
                    print("show crypto client-public-key")
                    print(f"ssh -i /path/to/myprivatekey {device['ip']}@{device['ip']}\n")
                end_time = datetime.now()
            if (not timeout):
                print(f"{Back.BLUE}Déploiment réussit !{Style.RESET_ALL} : Tout est OK")
            print(f"{Fore.BLUE}Commande effectué : {Style.RESET_ALL}{output}\n")
            print(f"{Back.MAGENTA}Benchmark{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}{'Exec time for 1 device : ':<25}{Style.RESET_ALL}{end_time - start_time}")

        except netmiko.exceptions.NetmikoAuthenticationException as e:
            err = str(e).replace("Authentication to device failed.\n", "").replace("Common causes of this problem are:\n", "").replace("\n\n\nAuthentication failed.", "").replace("\nDevice settings: hp_procurve 192.168.1.22:22", "")
            print(f"{Back.RED}ERREUR{Style.RESET_ALL}: Authentification Fail")
            print(f"{Fore.RED}Message personnel de debug :{Style.RESET_ALL}\n0. L'authentification par clef publique est déjà déployer\n")
            print(f"{Fore.RED}Message de Netmiko:{Style.RESET_ALL} {err}\n")
            #sys.exit(1)
        except netmiko.exceptions.NetmikoTimeoutException as e:
            print(f"\n{Back.RED}ERREUR{Style.RESET_ALL} : {e}")

def main():
    module = AnsibleModule(
        argument_spec=dict(
            # username=dict(type='str', required=True),
            # password=dict(type='str', required=True),
            command=dict(type='str', required=True),
        )
    )

    command = module.params['command']

    device = yaml_to_netmiko_dico("../hosts.yaml")
    net_connect = netmiko.ConnectHandler(**device)
    output = net_connect.send_command(command)
    net_connect.disconnect()

    module.exit_json(changed=False, stdout=output)

if __name__ == '__main__':
    main()
