from __future__ import print_function
from datetime import datetime
from colorama import Fore, Back, Style
import sys
import netmiko
import os
import argparse
import yaml

# ============================================================== #
# =================== FONCTION ET PROCEDURE ==================== #
# ============================================================== #
def get_public_key(path: str) -> str:
    """
    Ouvre et lit un fichier contenant une clé publique SSH.

    Args:
        path (str): Le chemin du fichier contenant la clé publique.

    Returns:
        str: La clé publique lue dans le fichier.

    Raises:
        FileNotFoundError: Si le fichier spécifié par `path` n'existe pas et qu'aucune
            clé publique par défaut n'est trouvée dans le fichier `~/.ssh/id_rsa.pub`.

    Si le fichier spécifié par `path` est introuvable, la fonction tente de trouver une clé
    publique par défaut dans le fichier `~/.ssh/id_rsa.pub`. Si cette clé publique est trouvée,
    l'utilisateur est invité à choisir s'il souhaite l'utiliser ou non. S'il choisit de ne pas
    l'utiliser, la fonction retourne un code de sortie de 1. Sinon, la clé publique par défaut
    est retournée.
    """
    try:
        with open(os.path.expanduser(path)) as f:
            public_key = f.read().strip()
    except FileNotFoundError:
        print(f"{Back.RED}ERREUR{Style.RESET_ALL} : le fichier {path} est introuvable.\n")
        try:
            with open(os.path.expanduser("~/.ssh/id_rsa.pub")) as f:
                default_key = f.read().strip()
                use_default = input(f"{Back.YELLOW}HINT{Style.RESET_ALL} : La clé publique par défaut a été trouvée dans ~/.ssh/id_rsa.pub. Voulez-vous l'utiliser ? (y/n): ")
                if use_default.lower() == "y":
                    public_key = default_key
                else:
                    sys.exit(1)
        except FileNotFoundError:
            print(f"{Back.RED}ERREUR{Style.RESET_ALL} : le fichier ~/.ssh/id_rsa.pub est introuvable.")
            sys.exit(1)
    return public_key

# def test_ssh_with_priv_key(device: dict, private_key_file: str) -> bool:
#     """
#     Teste la connexion SSH avec une clé privée

#     Args:
#         ip (str): adresse IP du périphérique
#         username (str): nom d'utilisateur pour la connexion SSH
#         private_key_file (str): chemin vers le fichier de la clé privée

#     Returns:
#         bool: True si la connexion est établie avec succès, False sinon
#     """
#     device["use_keys"] = True
#     device["key_file"] = private_key_file
#     try:
#         with netmiko.ConnectHandler(**device) as conn:
#             conn.send_command('conf t')
#         return True
#     except netmiko.exceptions.NetmikoAuthenticationException:
#         print(f"La connexion SSH avec clé privée a échoué pour l'adresse IP {device['ip']}")
#         return False

def yaml_to_netmiko_dico(inventory):
    with open(inventory, 'r') as f:
        inventory = yaml.safe_load(f)
    
    devices = []
    for host in inventory['hpProCurve']['hosts'].values():
        device = {
            'device_type': 'hp_procurve',
            'ip': host['ansible_host'],
            'username': inventory['hpProCurve']['vars']['ansible_ssh_user'],
            'port': inventory['hpProCurve']['vars']['ansible_port'],
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
                    output += connection.send_config_set(f"ip ssh public-key manager '{public_key}'")
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

def parse_arguments():
    parser = argparse.ArgumentParser(description='Script de deploiment SSH a clef public pour HP Procurve via Netmiko.')
    parser.add_argument('-p', '--port', help='Numéro de port SSH à configuré sur le switch', type=int, default=22)
    parser.add_argument('-k', '--pub-key', help='Chemin vers la clé publique SSH', default=os.path.expanduser("~/.ssh/id_rsa.pub"))
    parser.add_argument('-i', '--inventory', help='Chemin vers le fichier d\'inventaire', default='./hosts.yaml')
    #parser.add_argument('-K', '--priv-key', help='Chemin vers la clé privé SSH', default=os.path.expanduser("~/.ssh/id_rsa"))
    return parser.parse_args()


# ============================================================== #
# =========================== MAIN ============================= #
# ============================================================== #
def main():
    start_time_tot = datetime.now()
    args = parse_arguments()
    hpProcurves = yaml_to_netmiko_dico(args.inventory)
    configure_hp_procurve(args.port, get_public_key(args.pub_key), *hpProcurves)
    end_time_tot = datetime.now()
    print(f"{Fore.MAGENTA}{'Exec time tot : ':<25}{Style.RESET_ALL}{end_time_tot - start_time_tot}")


if __name__ == "__main__":
    main()
