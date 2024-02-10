# ssh_deployment

## Langue

- [Anglais](./README.md)

## Description

Ce rôle Ansible configure l'authentification SSH par clé publique sur des équipements réseau Cisco NX-OS et HP ProCurve. Il désactive également l'authentification par mot de passe quand cela est possible et le protocole Telnet sur ces équipements.

## Variables

Les variables suivantes peuvent être définies pour ce rôle :

- `ssh_users` : Liste des utilisateurs pour lesquels les clés publiques doivent être déployées. Chaque utilisateur est un dictionnaire qui comprend un nom d'utilisateur et une clé publique.
  - `username` : Nom de l'utilisateur à configurer (NX-OS).
  - `ssh_key` : Clef publique au format OpenSSH : `ssh-rsa AAAAB[...]wYJQ== raphael@alpes-book`
- `ssh_port` : Le port SSH sur lequel l'authentification par clé publique sera configurée.

## Exemple
fichier /path/to/role-directory/ssh_deployment/vars/main.yaml*

```yaml
ssh_users:
  - username: raph
    ssh_key: "{{ lookup('file', '~/.ssh/raph.pub') }}"
  - username: jean
    ssh_key: "{{ lookup('file', '~/.ssh/jean.pub') }}"

ssh_port: 1234
```
## Dépendances

Ce rôle dépend des collections et modules suivants :

- cisco.nxos
- netmikli

```bash
ansible-galaxy collection install cisco.nxos
```

## Task

- **`main.yml`**

  - Inclut diverses autres tâches
    - retrieving_ansible_variables.yaml
    - disable_telnet.yaml 
    - ssh_configuration.yaml 
    - change_ssh_port.yaml 
    - disable_password_authentification.yaml 
    - check_if_private_key_work.yaml


- **`ssh_configuration.yaml`**
  - Configure SSH et ajoute la clé publique pour Cisco NX-OS.
  - Configure SSH à l'aide de la clé publique pour HP ProCurve.

- **`disable_password_authentification.yaml`**

  - Désactive l'authentification par mot de passe pour HP ProCurve.

- **`check_if_private_key_work.yaml`**

  - Vérifie si la connexion fonctionne avec la clé privée pour HP ProCurve.

- **`disable_telnet.yaml`**

  - Désactive Telnet pour Cisco NX-OS.
  - Désactive Telnet pour HP ProCurve.

- **`retrieving_ansible_variables.yaml`**

  - Récupère les variables ansible.

- **`change_ssh_port.yaml`**

  - Change le port SSH pour HP ProCurve.



## Exemple de playbook

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
