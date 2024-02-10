# feature_setup

## Language

- [English](./README.md)

### Description
The Ansible role `feature_setup` is used to configure certain features on Cisco NX-OS and HP ProCurve network devices. The features in question are:

1. Enable SCP server feature (NX-OS only)
2. Enable LLDP feature (NX-OS only)
3. Enable Interface VLAN feature (NX-OS only)
4. Enable LACP feature (NX-OS only)
5. Disable Telnet feature (NX-OS and HP ProCurve)

## Requirements
This role requires Ansible version 2.1 or higher.

## Variables
The following variables are used by this role:

- `ansible_network_os`: The operating system, which can be 'cisco.nxos.nxos' or 'hp.procurve'.
- `ansible_host`: The host on which the role should be executed.
- `ansible_ssh_user`: The username to connect to the host.
- `ansible_ssh_pass`: The password to connect to the host.

File `feature_setup/vars/main.yaml`

```yaml
features_nxos: # Dictionary of features to add or remove on NX-OS
  enabled: # List of features to enable
    - scp-server
    - lldp
    - interface-vlan
    - lacp
    - telnet
  disabled: # List of features to disable
    - telnet
```
## Dependencies
This role depends on the following collections and modules:
- cisco.nxos
- netmiko

To install these dependencies, use the following commands:
```bash
ansible-galaxy collection install cisco.nxos
```
Example Playbook
------------

```yaml
---
- hosts: all
  gather_facts: no
  roles:
    - feature_setup
```

License
-------

MIT

Author Information
------------------

Raphaël L.