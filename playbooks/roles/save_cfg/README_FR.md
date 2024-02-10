# save_cfg

## Langue

- [Anglais](./README.md)

Ce rôle Ansible permet de sauvegarder la configuration en cours d'un périphérique réseau Cisco NX-OS ou Cisco IOS dans la NVRAM.

## Dépendances

Ce rôle dépend des collections et modules suivants :
- cisco.nxos

Pour installer ces dépendances, utilisez la commande suivante :
```bash
ansible-galaxy collection install cisco.nxos
```

## Exemple de playbook

Voici un exemple de playbook utilisant ce rôle.
```yaml
---
- hosts: nxos_switches
  gather_facts: no
  roles:
    - save_cfg
```

License
-------

MIT

Author Information
------------------

Raphaël L.
