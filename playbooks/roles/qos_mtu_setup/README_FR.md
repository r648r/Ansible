# qos_mtu_setup

## Language

- [English](./README.md)

Ce rôle Ansible configure les paramètres de qualité de service (QoS) du réseau et met en place une politique de trame jumbo sur un dispositif réseau Cisco NX-OS.

## Dépendances

Ce rôle dépend des collections et modules suivants :
- cisco.nxos

Pour installer ces dépendances, utilisez la commande suivante :
```
ansible-galaxy collection install cisco.nxos
```

## Playbook exemple
Voici un exemple de playbook utilisant ce rôle.
```yaml
---
- hosts: all
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
