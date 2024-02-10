# qos_mtu_setup

## Language

- [Français](./README_FR.md)


## Description
This role is responsible for the configuration of the network Quality of Service (QoS) settings and the setup of the jumbo MTU on the switch. This is mainly for the Cisco NXOS network operating system.

## Dependencies

 - cisco.nxos
 - netmiko (Custom module)

You can install these dependencies using the following commands:

```bash
ansible-galaxy collection install cisco.nxos
```

## Usage

Here is an example of how to use this role:

```yaml
---
- hosts: nxos_switches
  gather_facts: no
  roles:
    - qos_mtu_setup
```
License
-------

MIT

Author Information
------------------

Raphaël L.