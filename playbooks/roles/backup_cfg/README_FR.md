backup_cfg
=========
Language
---------
- [English](./README.md)

Description
------------
Ce rôle Ansible sauvegarde la configuration des équipements réseau. Il supporte à la fois les appareils Cisco NX-OS, Cisco IOS et HP ProCurve.

Les fichiers de sauvegarde sont nommés selon le format "{{ ansible_host }}_{{ ansible_date_time.time }}_{{ ansible_date_time.date }}.cfg". Par exemple, "192.168.1.1_14:30:00_2023-05-31.cfg". Ces variables sont accessibles grâce à la tâche `retrieving_ansible_variables.yaml` qui permet la récupération des variables Ansible.

Exigences
------------

Pour ce rôle, vous devez avoir Ansible version 2.9 ou supérieure.

Variables du Rôle
--------------

Le rôle n'a pas de variables par défaut définies.

- `ansible_network_os`: Le système d'exploitation, qui peut être 'cisco.nxos.nxos' ou 'hp.procurve'.
- `ansible_host`: L'hôte auquel se connecter pour exécuter le rôle.
- `ansible_ssh_user`: Le nom d'utilisateur pour se connecter à l'hôte.
- `ansible_ssh_pass`: Le mot de passe pour se connecter à l'hôte.
- `ansible_date_time`: Les informations de date et d'heure actuelles.

Dépendances
------------
 - cisco.nxos
 - netmiko (Custom module)

```bash
ansible-galaxy collection install cisco.nxos
```

Exemple de Playbook
----------------

Exemple d'utilisation du rôle `backup_cfg` :

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


