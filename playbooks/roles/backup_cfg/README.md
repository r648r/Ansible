backup_cfg
=========

Language
---------
- [Français](./README_FR.md)

Description
------------

This Ansible role backs up the configuration of network devices. It supports both Cisco NX-OS, Cisco IOS, and HP ProCurve devices.

Backup files are named using the format "{{ ansible_host }}_{{ ansible_date_time.time }}_{{ ansible_date_time.date }}.cfg", e.g. "192.168.1.1_14:30:00_2023-05-31.cfg". This information is accessible thanks to the `retrieving_ansible_variables.yaml` task, which allows the retrieval of Ansible variables.

Requirements
------------

For this role, you need Ansible version 2.9 or higher.

Role Variables
--------------

The role does not have default variables defined.

- `ansible_network_os`: The operating system, which can be 'cisco.nxos.nxos' or 'hp.procurve'.
- `ansible_host`: The host to connect to when executing the role.
- `ansible_ssh_user`: The username to connect to the host.
- `ansible_ssh_pass`: The password to connect to the host.
- `ansible_date_time`: Current date and time information.

Dependencies
------------

 - cisco.nxos
 - netmiko (Custom module)

You can install these dependencies using the following commands:

```bash
ansible-galaxy collection install cisco.nxos
```

Example Playbook
------------
Example of how to use the backup_cfg role:

```yaml
---
- hosts: all
  gather_facts: no
  roles:
    - backup_cfg
```

License
-------

MIT

Author Information
------------------

Raphaël L.