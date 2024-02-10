# spanning-tree_setup

## Langue

- [Anglais](./README.md)

## Description

Ce rôle configure les paramètres Spanning Tree sur les périphériques Cisco NX-OS.

## Variables

Les variables suivantes peuvent être définies pour ce rôle :
**Fichier : spanning-tree_setup/vars/main.yml**
- `mode` : Le mode Spanning Tree à configurer. Par défaut, il est défini sur rapid-pvst.
- `loopguard` : Valeur booléenne indiquant si le loopguard doit être activé. Par défaut, il est défini sur true.

**Fichier : inventory/network/switch/cisco/host_vars/<hostname>**
- `STP.root` : La plage de VLAN pour le pont racine. Par défaut, il est défini sur 10-20.
- `STP.root_secondary` : La plage de VLAN pour le pont racine secondaire. Par défaut, il est défini sur 21-30.

## Dependence

Ce rôle dépend des collections et modules suivants :

- cisco.nxos

Pour installer ces dépendances, utilisez la commande suivante :
```bash
ansible-galaxy collection install cisco.nxos
```

## Example Playbook

Voici un exemple d'utilisation de ce rôle dans un playbook :

```yaml
- hosts: servers
  roles:
    - role: username.rolename
      vars:
        STP:
          mode: rapid-pvst
          root: 10-20
          root_secondary: 21-30
          loopguard: true
```

License
-------

MIT

Author Information
------------------

Raphaël L.