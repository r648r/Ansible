# snmp_setup
## Langue

- [Anglais](./README.md)

## Description
Ce rôle Ansible permet de configurer le SNMP (Simple Network Management Protocol) sur les périphériques réseau Cisco NX-OS.

## Tâches incluses

Ce rôle comprend les tâches suivantes :

### logging.yaml

- Supprime toutes les configurations de logs (NX-OS).
- Configure les logs (NX-OS) pour l'événement "link-status default".

### users.yaml

- Applique la configuration SNMP pour les utilisateurs spécifiés dans les variables.
- Utilise l'algorithme de hashage "md5" et des mots de passe hashé pour chaque utilisateur.

### location.yaml

- Configure l'emplacement du serveur SNMP avec la valeur "Chavanod, France".

### community.yaml

- Remplace la configuration SNMP en définissant une communauté et son groupe.
- Utilise la communauté "Alpn74" avec le groupe "network-operator".

### main.yaml

- Inclut les tâches de configuration de l'emplacement, des utilisateurs, de la communauté et des logs.

## Variables

Les variables suivantes sont utilisées dans ce rôle :

- `snmp_users` : Cette variable contient une liste d'utilisateurs SNMP à configurer. Chaque élément de la liste représente un utilisateur.
  - `name` : Le nom de l'utilisateur.
  - `auth` : Les informations d'authentification de l'utilisateur.
    - `password` : Le mot de passe hashé en MD5 de l'utilisateur.
## Dépendances

Ce rôle dépend des collections et modules suivants :

- cisco.nxos

Pour installer ces dépendances, utilisez la commande suivante :
```bash
ansible-galaxy collection install cisco.nxos
```
## Exemple de playbook

Voici un exemple de playbook utilisant ce rôle :

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