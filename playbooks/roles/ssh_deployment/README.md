# ssh_deployment

## Language

- [Francais](./README_FR.md)

## Description

This Ansible role configures SSH public key authentication on Cisco NX-OS and HP ProCurve network devices. It also disables password authentication when possible and the Telnet protocol on these devices.

## Variables

The following variables can be defined for this role:

- `ssh_users`: List of users for whom public keys should be deployed. Each user is a dictionary that includes a username and a public key.
  - `username`: User name to be configured (NX-OS).
  - `ssh_key` : Public key in OpenSSH format: `ssh-rsa AAAAB[...]wYJQ== raphael@alpes-book`
- `ssh_port`: The SSH port on which public key authentication will be configured.

## Example
File /path/to/role-directory/ssh_deployment/vars/main.yaml

```yaml
ssh_users:
  - username: raph
    ssh_key: "{{ lookup('file', '~/.ssh/raph.pub') }}"
  - username: jean
    ssh_key: "{{ lookup('file', '~/.ssh/jean.pub') }}"

ssh_port: 1234
```
## Dependencies

This role depends on the following collections and modules:

- cisco.nxos
- netmikli
```bash
ansible-galaxy collection install cisco.nxos
```
## Task

- **`main.yml`**

  - Includes various other tasks
    - retrieving_ansible_variables.yaml
    - disable_telnet.yaml 
    - ssh_configuration.yaml 
    - change_ssh_port.yaml 
    - disable_password_authentification.yaml 
    - check_if_private_key_work.yaml


- **`ssh_configuration.yaml`**
  - Configures SSH and adds the public key for Cisco NX-OS.
  - Configures SSH using the public key for HP ProCurve.

- **`disable_password_authentification.yaml`**

  - Disables password authentication for HP ProCurve.

- **`check_if_private_key_work.yaml`**

  - Checks if the connection works with the private key for HP ProCurve.

- **`disable_telnet.yaml`**

  - Disables Telnet for Cisco NX-OS.
  - Disables Telnet for HP ProCurve.

- **`retrieving_ansible_variables.yaml`**

  - Retrieves ansible variables.

- **`change_ssh_port.yaml`**

  - Changes the SSH port for HP ProCurve.

## Example Playbook
```yaml 
- hosts: servers
  roles:
    - role: username.ssh_deployment
      vars:
        ssh_users:
          - username: raph
            ssh_key: "{{ lookup('file', '~/.ssh/raph.pub') }}"
          - username: jean
            ssh_key: "{{ lookup('file', '~/.ssh/jean.pub') }}"
        ssh_port: 1234
```
License
-------

MIT

Author Information
------------------

Raphaël L.
