# feature_setup

## Language

- [English](./README.md)

## Description
Permet la configuration de feature sur les Cisco NX-OS et HP ProCurve. Les fonctionnalités concernées sont :

1. Activation du serveur SCP (uniquement sur NX-OS)
2. Activation de LLDP (uniquement sur NX-OS)
3. Activation de l'interface VLAN (uniquement sur NX-OS)
4. Activation de LACP (uniquement sur NX-OS)
5. Désactivation de Telnet (sur NX-OS et HP ProCurve)

## Exigences
Ce rôle nécessite Ansible version 2.1 ou supérieure.

## Variables
Les variables suivantes sont utilisées par ce rôle:

- `ansible_network_os`: Le système d'exploitation de l'appareil, qui peut être 'cisco.nxos.nxos' ou 'hp.procurve'.
- `ansible_host`: L'hôte sur lequel le rôle doit être exécuté.
- `ansible_ssh_user`: Le nom d'utilisateur pour se connecter à l'hôte.
- `ansible_ssh_pass`: Le mot de passe pour se connecter à l'hôte.

Fichier `feature_setup/vars/main.yaml`
```yaml
features_nxos: # Dictionnaire contenant les feature a ajouter ou supprimer sur un NX-OS
  enabled:
    - scp-server
    - lldp
    - interface-vlan
    - lacp
    - telnet
  disabled:
    - telnet
```
## Dépendances
Ce rôle dépend des collections et modules suivants :
- cisco.nxos
- netmiko

Pour installer ces dépendances, utilisez les commandes suivantes :
```bash
ansible-galaxy collection install cisco.nxos
```
## Note
`ignore_errors: yes` est utilisé pour ignorer les erreurs lors de l'activation du serveur SCP car cette fonctionnalité peut ne pas être disponible sur certains switchs.

Example de Playbook
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