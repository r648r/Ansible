# snmp_setup
## Language

- [Francais](./README_FR.md)

## Description
This Ansible role allows you to configure SNMP (Simple Network Management Protocol) on Cisco NX-OS network devices.

## Included Tasks

This role includes the following tasks:

### logging.yaml

- Delete all logging configurations (NX-OS).
- Configure logging (NX-OS) for the "link-status default" event.

### users.yaml

- Apply SNMP configuration for users specified in the variables.
- Use the "md5" hashing algorithm and hashed passwords for each user.

### location.yaml

- Configure SNMP server location with the value "Chavanod, France".

### community.yaml

- Replace SNMP configuration by defining a community and its group.
- Use the community "Alpn74" with the "network-operator" group.

### main.yaml

- Include tasks for configuration of location, users, community, and logging.

## Variables

The following variables are used in this role:

- `snmp_users`: This variable contains a list of SNMP users to configure. Each list item represents a user.
  - `name`: The name of the user.
  - `auth`: The user's authentication information.
    - `password`: The MD5 hashed password for the user.

Dependencies

This role depends on the following collections and modules:

- cisco.nxos

To install these dependencies, use the following command:

```bash
ansible-galaxy collection install cisco.nxos
```
## Example Playbook

Here is an example playbook using this role:

```yaml
- hosts: nxos_switches
  gather_facts: no
  roles:
    - snmp_setup
```
License
-------

MIT

Author Information
------------------

Raphaël L.