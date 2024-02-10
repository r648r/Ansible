#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
---
module: netmikli
short_description: Execute commands on a network devices using Netmiko
description:
    - This Ansible module allows you to execute one or multiple commands on a network devices devices using the Netmiko library.
    - It allows to test if the authentication by public key is functional
    - It requires a username, password or a private key path for authentication.
    - You can optionally save the device configuration using the "saverunpath" parameter.
version_added: "1.0"
author: Raphaël LECHAPPE (@r.lechappe)"
options:
    netmiko_device_type:
        description:
            - The Netmiko device type. Required.
            - List of device supported http://ktbyers.github.io/netmiko/PLATFORMS.html
        required: true
    host:
        description:
            - The IP address of the device. Required.
        required: true
        type: str
    port:
        description:
            - The SSH port number to connect to. Default is 22.
        required: false
        default: 22
        type: int
    username:
        description:
            - The username to use for ssh authentication. Required.
        required: true
        type: str
    password:
        description:
            - The password to use for ssh authentication. 
        required: false
        no_log: true
        type: str
    commands:
        description:
            - List of commands to execute on the device.
        required: false
        type: list
    privkeypath:
        description:
            - The path to the private key file to use for authentication. Required if password is not provided.
        required: false
        type: str
    saverunpath:
        description:
            - The path to save the device configuration to.
        required: false
        type: str
requirements:
    - ansible 7.5.0
    - paramiko 3.1.0
    - netmiko 4.2.0
    - genie 23.4
    - pyats 23.4
seealso:
    - Netmiko library: https://github.com/ktbyers/netmiko
    - Ansible documentation on developing modules: https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html
notes:
    - This module work with many devices inconsistent with ansible.builtin.raw module
'''

EXEMPLES = '''
vars:
    ssh_key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"

- name: Backing up the configuration file
netmikli:
    host: "{{ ansible_host }}"
    username: "{{ ansible_ssh_user }}"
    password: "{{ ansible_ssh_pass }}"
    netmiko_device_type: hp_procurve
    saverunpath: /home/raphael/Projects/gitlab/log/show-run

- name: SSH configuration by public key on HP ProCurve
netmikli:
    host: "{{ ansible_host }}"
    username: "{{ ansible_ssh_user }}"
    password: "{{ ansible_ssh_pass }}"
    netmiko_device_type: hp_procurve

    commands:
    - no telnet-server
    - ip ssh port 22
    - ip ssh cipher aes256-cbc
    - ip ssh mac hmac-sha1
    - ip ssh filetransfer
    - aaa authentication ssh login public-key none
    - aaa authentication ssh enable public-key
    - ip ssh public-key manager '{{ ssh_key }}'
register: result
when: ansible_network_os == 'hp.procurve'
- debug:
    var: result.msg
'''

RETURN = r''' # ''' 

from ansible.module_utils.basic import AnsibleModule
import logging
import netmiko
import os
import traceback
import datetime

LOG_DIRECTORY = os.environ.get('ANSIBLE_NETMIKLI_LOG', '/home/ansible/Ansible-clef-publique/log/')
SESSION_LOG_DIRECTORY = f'{LOG_DIRECTORY}session/'
# PAS ENCORE TEST
# Faire des test avec un env virtuel pour voir si ca marche bien 


def check_dependencies(MODULE, LIBS_NEEDED):
    """
    Check for required Python libraries and fails if any are missing.

    Args:
        MODULE: A module object.
        LIBS_NEEDED (list, optional): A list of required libraries. Defaults to ['netmiko', 'paramiko', 'genie', 'pyats', 'argcomplete', 'os'].

    This function checks if the required Python libraries are installed on the system by attempting to import each one using `__import__`.
    If any of the required libraries are missing, the MODULE's fail_json method is called with a message listing the missing libraries.
    """
    missingLibrary = []
    for lib in LIBS_NEEDED:
        try:
            __import__(lib)
        except ImportError:
            missingLibrary.append(lib)
    if missingLibrary:
        errorMessage = "Missing required Python library(ies): {}".format(', '.join(missingLibrary))
        MODULE.fail_json(msg=errorMessage)
    
def log_exception(e: Exception, message: str, level='error'):
    """
    Logs an exception with a custom message.

    Args:
        e (Exception): The exception to log.
        message (str): The custom message to log with the exception.
        level (str): The level at which to log the exception. Default is 'error'.
    """
    log_func = getattr(logging, level)
    log_func(f"{message}. Exception occurred", exc_info=e)

def create_show_run_dir(net_device_local: dict[str, str], outputDirectory: str) -> bool:
    """
    Connects to a network device using the authentication information provided in the net_device_local
    dictionary and sends the 'show run' command to retrieve the current configuration. The configuration
    is saved to a file named 'show_run_<IP_address>.txt' in the directory specified by outputDirectory.

    Args:
        net_device_local (dict[str, str]): A dictionary containing the authentication information
            necessary to connect to the network device. Must contain the following keys:
            - 'device_type': The type of device to connect to (e.g. 'cisco_ios')
            - 'ip': The IP address or hostname of the device
            - 'username': The username to use for authentication
            - 'password': The password to use for authentication
            - 'secret': (optional) The enable secret to use for privileged mode access
        outputDirectory (str): The path to the directory where the show run output file should be saved.

    Returns:
        bool: True if the configuration was successfully saved, False otherwise (e.g. if authentication
            failed or a connection timeout occurred).
    """
    try:
        with netmiko.ConnectHandler(**net_device_local) as con:
            showRunOutput = con.send_command("show run", use_genie=True)

        if not os.path.exists(outputDirectory):
            os.makedirs(outputDirectory)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        with open(os.path.join(outputDirectory, f"{net_device_local['ip']}_{current_time}.cfg"), 'w') as f:
            f.write(showRunOutput)
            return True
    except (netmiko.exceptions.NetmikoAuthenticationException, netmiko.exceptions.NetmikoTimeoutException) as e:
        return False

def save_show_run(MODULE, net_device):
    if MODULE.params['saverunpath'] is not None:
        try:
            if not create_show_run_dir(net_device, MODULE.params['saverunpath']):
                raise Exception("Failed to save show run")
            else:
                MODULE.exit_json(changed=False, msg=f"Saving the configuration file successfully in the directory : {MODULE.params['saverunpath']}")
        except Exception as e:
            MSG_ERROR = "Unable to save show run, verify your username and password"
            log_exception(e, MSG_ERROR, 'warning')
            MODULE.fail_json(msg=MSG_ERROR)

def test_key_path(module_local: dict) -> bool:
    """
    Tests the existence of a private key file at the given path. If the path is wrong then the function check 
    if a private key exist here ~/.ssh/id_rsa

    Args:
        path (str): The path to the private key file.
        module_local (dict) dictionary containing the connection details for the network device.

    Returns:
        bool: True if the private key file exists, False otherwise. 

    Raises:
        FileNotFoundError: If the private key file is not found at the given path or at the default path (~/.ssh/id_rsa).
    """
    PATH = os.path.expanduser(module_local.params['privkeypath'])
    
    if os.path.isfile(PATH):
        return True
    else:
        log_exception(FileNotFoundError(f"No such file or directory: '{PATH}'"), "Failed to open private key file, it possible exist in ~/.ssh/id_rsa")
        
        DEFAULT_PATH = os.path.expanduser("~/.ssh/id_rsa")
        
        if os.path.isfile(DEFAULT_PATH):
            module_local.fail_json(msg=f"The private key was not found in {PATH}, but exists in ~/.ssh/id_rsa, try privkeypath: ~/.ssh/id_rsa in your playbook")
            return False
        else:
            MSG_ERROR = f"The private key was not found in {PATH}, and also does not exist in ~/.ssh/id_rsa"
            log_exception(FileNotFoundError(f"No such file or directory: '{DEFAULT_PATH}'"), MSG_ERROR)
            module_local.fail_json(msg=MSG_ERROR)
            return False


def connect_with_private_key(net_device_local: dict[str, str], keyFilename: str) -> bool:
    """
    This function connects to a network device using Netmiko and a private key.

    Parameters:
        net_device_local (Dict[str, str]): A dictionary containing the connection details for the network device.
        keyFilename (str): The path of the private key to use for authentication.

    Returns:
        bool: True if the connection was successful, False otherwise.

    This function attempts to establish a SSH connection to a network device using Netmiko and a private key.
    It takes in a dictionary containing the connection details for the network device, the path of the private key to use for authentication, and the IP address of the network device.
    If the connection is successful, the function returns True, otherwise it returns False.
    """
    net_device_local['use_keys'] = True
    net_device_local['key_file'] = keyFilename
    del net_device_local['session_log']

    try:
        with netmiko.ConnectHandler(**net_device_local):
            net_device_local['session_log'] = f'{SESSION_LOG_DIRECTORY}{net_device_local["device_type"]}_{net_device_local["ip"]}.log'
            del net_device_local['use_keys']
            del net_device_local['key_file']
            return True
    except (netmiko.exceptions.NetmikoAuthenticationException, netmiko.exceptions.NetmikoTimeoutException):
        net_device_local['session_log'] = f'{SESSION_LOG_DIRECTORY}{net_device_local["device_type"]}_{net_device_local["ip"]}.log'
        return False

def error_to_json(error: Exception, message: str) -> dict:
    """
    Converts a Python error and a custom message to a JSON format.

    Parameters:
        error (Exception): The Python error to be converted to JSON format.
        message (str): A custom message to be included in the JSON output.

    Returns:
        dict: A dictionary containing the converted error and the custom message in a JSON-like format.

    This function takes in a Python error and a custom message, and converts them to a JSON-like dictionary format.
    The output dictionary contains the following keys:
    - 'achieve': The custom message passed as an argument.
    - 'Debug_log': The path to a log file.
    - 'debug': A nested dictionary containing the following keys:
        - 'Error': A dictionary containing information about the error, including its type, message, and traceback.
        - 'traceback': A nested dictionary containing information about each frame in the error's traceback, including the filename, line number, function name, and source code line.
    """
    frames = []

    for frame in traceback.extract_tb(error.__traceback__):
        frames.append({
            'filename': frame.filename,
            'lineno': frame.lineno,
            'name': frame.name,
            'text': frame.line
        })

    json_error = dict(achieve= message,
                        Debug_log = f'{LOG_DIRECTORY}netmikli.log',
                        debug = {
                            "Error" : {
                                "type": type(error).__name__,
                                "message": [item for item in str(error).split("\n") if item.strip()],
                                "traceback": {
                                    'exception_type': str(error.__class__),
                                    'frames': frames
                                            }
                                    }
                                }                                        
                        )
    return json_error

def push_command(net_device_local, module_local, command):
    try:
        with netmiko.ConnectHandler(**net_device_local) as connection:
            result=dict(achieve= "Succesfull ! Without any error")
            try:
                connection.send_config_set(command)
            except netmiko.exceptions.ReadTimeout as e:
                log_exception(e, "Exception timeout", 'warning')                   
                result = error_to_json(e, "Succesfull ! But timeout error")
            finally:
                module_local.exit_json(**dict(changed=True, msg=result))


    except (netmiko.exceptions.NetmikoAuthenticationException, netmiko.exceptions.NetmikoTimeoutException) as e:
        log_exception(e, "An authentication or timeout exception occurred", level='error')
        if module_local.params['privkeypath'] is not None:
            if connect_with_private_key(net_device_local, module_local.params['privkeypath']):
                module_exit_priv_key_work(module_local)
            else:
                result = error_to_json(e, "The command execution failed due to authentication error, impossible to connect with the private key or password")
                module_local.fail_json(**dict(changed=False, msg=result))
        else:
            result = error_to_json(e, "The command execution failed due to authentication error impossible to connect with password")
            module_local.fail_json(**dict(changed=False, msg=result))

def module_exit_priv_key_work(MODULE_LOCAL):
    MODULE_LOCAL.exit_json(changed=False, msg=f"Not changed because auth by public key is already functionnal")

def setup_module():
    return AnsibleModule(
        argument_spec=dict(
            netmiko_device_type=dict(required=True),
            host=dict(required=True),
            port=dict(required=False, default=22),
            username=dict(required=True),
            password=dict(required=True, no_log=True),
            commands=dict(type='list', required=False),
            privkeypath=dict(required=False, type='str'),
            saverunpath=dict(required=False, type='str'),
            HP_procurve_public_key_deployment=dict(required=False, type='str'),
            HP_procurve_disable_telnet=dict(required=False, type='bool')
        ),
        supports_check_mode=False)

def setup_netmiko(MODULE):
    return {
        'device_type': MODULE.params['netmiko_device_type'],
        'ip': MODULE.params['host'],
        'port': int(MODULE.params['port']),
        'username': MODULE.params['username'],
        'password': MODULE.params['password'],
        'verbose': False,
        'session_log': f'{SESSION_LOG_DIRECTORY}{MODULE.params["netmiko_device_type"]}_{MODULE.params["host"]}.log'
    }

def setup_log():
    logging.basicConfig(filename=f'{LOG_DIRECTORY}netmikli.log', level=logging.WARNING, format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    if not os.path.exists(SESSION_LOG_DIRECTORY):
        os.makedirs(SESSION_LOG_DIRECTORY)

def groupe_commands(MODULE, net_device):
    commandes = []
    if MODULE.params["HP_procurve_disable_telnet"] is not None:
        commandes.append("no telnet-server")
    
    if MODULE.params["HP_procurve_public_key_deployment"] is not None:
        commandes.extend([
            "ip ssh port 22", 
            "ip ssh cipher aes256-cbc", 
            "ip ssh mac hmac-sha1", 
            "ip ssh filetransfer", 
            f"""ip ssh public-key manager '{MODULE.params["HP_procurve_public_key_deployment"]}'""",
        ])
    if MODULE.params['commands'] is not None:
        commandes.extend(MODULE.params['commands'])
        
    if MODULE.params["HP_procurve_disable_telnet"] or (MODULE.params["HP_procurve_public_key_deployment"] is not None) or (MODULE.params['commands'] is not None):
        # commandes.append("write memory")
        push_command(net_device, MODULE, commandes)

def test_priv_key_con(MODULE, net_device):
    if MODULE.params['privkeypath'] is not None:
        if test_key_path(MODULE):  # If the private key is found
            if connect_with_private_key(net_device, MODULE.params['privkeypath']):
                module_exit_priv_key_work(MODULE)
            else:
                MODULE.fail_json(**dict(changed=False, msg="The command execution failed due to authentication error, impossible to connect with the private key or password"))
        else:  # If the private key is not found
            MODULE.fail_json(msg=f"The private key was not found in {MODULE.params['privkeypath']}, and also not exist in ~/.ssh/id_rsa")


def main():
    MODULE = setup_module()
    net_device = setup_netmiko(MODULE)
    setup_log()
    check_dependencies(MODULE,  ['netmiko', 'paramiko', 'genie', 'pyats', 'argcomplete', 'os'])
    if (MODULE.params["HP_procurve_disable_telnet"] is None) and (MODULE.params["HP_procurve_public_key_deployment"] is None) and (MODULE.params['commands'] is None) and (MODULE.params['saverunpath'] is None) and (MODULE.params['privkeypath'] is None):
        MODULE.fail_json(msg=f"Tu n'as passé aucun argument !")
    
    save_show_run(MODULE, net_device)
    groupe_commands(MODULE, net_device)
    test_priv_key_con(MODULE, net_device)

if __name__ == "__main__":
    main()