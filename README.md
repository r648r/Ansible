<!-- HEADER -->

# Netmikli

**Objectif** : Rendre des periférique qui ne possède pas de module dédier ([All Module](https://docs.ansible.com/ansible/2.9/modules/list_of_all_modules.html)) ou qui sont pas pris en charge par [ansible.builtin.raw](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/raw_module.html) compatible avec Ansible pour de l'execution de commande brut via SSH.

## Installation

**One-line install**

Pour Bash :

```bash
apt update -y && apt install python python3-pip git curl nginx -y && git clone https://git.[..].com/r.lechappe/Ansible-clef-publique.git && cd Ansible-clef-publique && pip install -r requirements.txt && ansible-galaxy collection install sshnaidm.openai && ansible-galaxy collection install cisco.nxos && echo 'export ANSIBLE_LIBRARY="./library/"' >> ~/.bashrc && echo 'export ANSIBLE_NETMIKLI_LOG=./log/' >> ~/.bashrc && source ~/.bashrc
```

Pour Zsh :

```bash
apt update -y && apt install python python3-pip git -y && git clone https://git.[...].com/r.lechappe/Ansible-clef-publique.git && cd Ansible-clef-publique && pip install -r requirements.txt && ansible-galaxy collection install sshnaidm.openai && ansible-galaxy collection install cisco.nxos && echo 'export ANSIBLE_LIBRARY="./library/"' >> ~/.zshrc && echo 'export ANSIBLE_NETMIKLI_LOG=./log/' >> ~/.zshrc && source ~/.zshrc
```

**Exigences**

- Ansible 7.5.0
- Paramiko 3.1.0
- Netmiko 4.2.0
- Genie 23.4
- PyATS 23.4
- openai 0.27.7

```bash
pip install -r requirements.txt
```

ou

```bash
pip install ansible
pip install paramiko --upgrade
pip install genie
pip install pyats
pip install argcomplete
pip install ansible-pylibssh 
pip install openai
```

#### Options

##### Obligatoire

- **`netmiko_device_type`** (str) : Le type d'appareil Netmiko. Vous pouvez trouver la liste des appareils supportés [ici](http://ktbyers.github.io/netmiko/PLATFORMS.html).
- **`host`** (str) : L'adresse IP de l'appareil.
- **`username`** (str) : Le nom d'utilisateur à utiliser pour l'authentification SSH.

##### Facultatif

- **`port`** (int) : Le numéro de port SSH pour la connexion. Par défaut, il s'agit du port 22.
- **`password`** (str) : Le mot de passe à utiliser pour l'authentification SSH.
- **`commands`** (list) : Liste des commandes à exécuter sur l'appareil.
- **`privkeypath`** (str) : Le chemin vers le fichier de clé privée à utiliser pour l'authentification. Permet simplement de tester si l'authentification par clef publique est fonctionnelle.
- **`saverunpath`** (str) : Le chemin où sauvegarder la configuration de l'appareil.
- **`HP_procurve_public_key_deployment`** (str) : Clef publique à déployer sur un switch HP ProCurve au format OpenSSH RSA. (exemple : ssh-rsa AAA[...]== raphael@alpes-book)
- **`HP_procurve_disable_telnet`** (bool) : Boolean permettant de désactiver telnet sur un switch HP ProCurve.

#### Variable d'environnement

##### Obligatoire
bash

```bash
echo 'export ANSIBLE_LIBRARY="./library"' >> ~/.bashrc 
echo 'export ANSIBLE_NETMIKLI_LOG=./log/' >> ~/.bashrc 
source ~/.bashrc
```

zsh
```bash
echo 'export ANSIBLE_LIBRARY="./library"' >> ~/.zshrc
echo 'export ANSIBLE_NETMIKLI_LOG=./log/' >> ~/.bashrc 
source ~/.zshrc
```

##### Facultatif

```bash
export OPENAI_API_KEY=token
```

#### Structure des logs

```
─ log
  ├── netmikli.log
  ├── session
  │   ├── hp_procurve_10.200.80.222.log
  │   └── hp_procurve_10.200.80.224.log
  └── show_run
      ├── show_run_10.200.80.222
      └── show_run_10.200.80.224
```

L'organisation des fichiers log pour ce module Ansible est structurée de manière à faciliter la compréhension et le débogage de tout problème qui pourrait survenir lors de l'exécution du module. Voici une brève explication de chaque fichier log :

- **`netmikli.log`** : Ce fichier contient les logs générales de l'application. Il enregistre toutes les activités lié a une erreur du module.
- **`session`** : Ce répertoire contient les logs de session pour chaque appareil avec lequel le module interagit. Chaque appareil a son propre fichier log nommé `<device_type>_<ip>.log`, où `<device_type>` est la [reference Netmiko](http://ktbyers.github.io/netmiko/PLATFORMS.html). Ces logs contiennent des informations spécifiques à chaque appareil, y compris les commandes envoyées à l'appareil et les réponses reçues.
- **`show_run`** : Ce répertoire contient des fichiers avec la configuration actuelle de chaque appareil. Chaque appareil a son propre fichier nommé `<ip>_YYYY-MM-DD_hh:mm:ss.cfg`. Ces fichiers contiennent le résultat de la commande `show running-config` exécutée sur l'appareil.

## Rôle
- [backup_cfg](./playbooks/roles/backup_cfg/README_FR.md)
- [feature_setup](./playbooks/roles/feature_setup/README_FR.md)
- [interface_setup](./playbooks/roles/interface_setup/README_FR.md)
- [qos_mtu_setup](./playbooks/roles/qos_mtu_setup/README_FR.md)
- [save_cfg](./playbooks/roles/save_cfg/README_FR.md)
- [snmp_setup](./playbooks/roles/snmp_setup/README_FR.md)
- [spanning-tree_setup](./playbooks/roles/spanning-tree_setup/README_FR.md)
- [ssh_deployment](./playbooks/roles/ssh_deployment/README_FR.md)

## Inventory

### Arborescence de l'inventaire

```
─ inventory
  ├── network
  │   ├── router
  │   └── switch
  │       ├── cisco
  │       │   ├── group_vars
  │       │   │   ├── all
  │       │   │   │   └── all.yaml     # Variables communes à tous les switch Cisco
  │       │   │   └── nx-os.yaml       # Variables spécifiques aux switch Cisco ayant pour OS NX-OS.
  │       │   ├── hosts.yaml           # Inventaire des switchs Cisco
  │       │   └── host_vars            # Répertoire contenant les variables spécifiques de chaque switch Cisco
  │       └── hp
  │           ├── group_vars
  │           │   ├── all
  │           │   │   └── all.yaml     # Variables communes à tous les switch HP
  │           │   └── hpProCurve.yaml  # Variables spécifiques au modèle HP Procurve
  │           ├── hosts.yaml           # Inventaire des switchs HP
  │           └── host_vars            # Répertoire contenant les variables spécifiques de chaque switch HP
  └── server
```

- **`network/router`**: Répertoire contenant l'inventaire et les varibles spécifiques aux routeurs.
- **`network/switch/<constructeur>/group_vars/all/all.yaml`**: Fichier contenant les variables communes à tous les équipements du constructeur <constructeur> dans la catégorie switch.
- **`network/switch/<constructeur>/group_vars/<modèle>.yaml`**: Fichier contenant les variables spécifiques aux modèles du constructeur.
- **`network/switch/<constructeur>/hosts.yaml`**: Fichier contenant l'inventaire des hôtes pour les équipements du constructeur <constructeur>.
- **`network/switch/<constructeur>/host_vars`**: Répertoire contenant les variables spécifiques à chaque équipement du constructeur <constructeur>.

### Ansible Vaul

#### Définir le mot de passe global de vaultage

```bash
echo "MotDePasseDeMonVault" > /etc/vault.txt
chmod 600 /etc/vault.txt
```

#### Ajouté une entré sécurisé dans mon inventaire ansible

**Exemple d'inventory avant chiffrement**

```yaml
MonGroupe:
  hosts:
    switch:
      ansible_host: 192.168.1.1
  vars:
    ansible_port: 22
    ansible_ssh_user: admin
    ansible_ssh_pass: password
```

**Chiffré une entrée en claire**

```bash
ansible-vault encrypt_string 'password' --name 'ansible_ssh_pass'
# Resultat
Encryption successful
ansible_ssh_pass: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  32363830336432346664323533346533613265626635616135316132376434663432396164303036
  3461316662613561653039666531353836626330356261320a623233653138336263663336393763
  39383136616535326262336335656262316438633034626233653135316333353235323538613237
  3339356264343135350a363831366230333536383363643165303766303564333363313562386633
  3136
```

**Exemple d'inventory après chiffrement**

```yaml
MonGroupe:
  hosts:
    switch:
      ansible_host: 192.168.1.1
  vars:
    ansible_port: 22
    ansible_ssh_user: admin
    ansible_ssh_pass: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          32363830336432346664323533346533613265626635616135316132376434663432396164303036
          3461316662613561653039666531353836626330356261320a623233653138336263663336393763
          39383136616535326262336335656262316438633034626233653135316333353235323538613237
          3339356264343135350a363831366230333536383363643165303766303564333363313562386633
          3136
```

**Utilisé un inventaire avec des password vaulté**

```bash
ansible-playbook -i hosts.yaml playbooks/SSH_public_key.yaml --vault-password-file=/etc/vault.txt
```

## Configuration du controlleur Ansible
```
       _,met$$$$$gg.
    ,g$$$$$$$$$$$$$$$P.
  ,g$$P"     """Y$$.".
 ,$$P'              `$$$.
',$$P       ,ggs.     `$$b:   ansible@ansible 
`d$$'     ,$P"'   .    $$$    --------------- 
 $$P      d$'     ,    $$P    OS: Debian GNU/Linux 11 (bullseye) x86_64 
 $$:      $$.   -    ,d$$'    Host: KVM/QEMU (Standard PC (i440FX + PIIX, 1996) pc-i440fx-6.2) 
 $$;      Y$b._   _,d$P'      Kernel: 5.10.0-23-amd64 
 Y$$.    `.`"Y$$$$P"'         Uptime: 7 days, 20 hours, 46 mins 
 `$$b      "-.__              Packages: 513 (dpkg) 
  `Y$$                        Shell: bash 5.1.4 
   `Y$$.                      Resolution: 1024x768 
     `$$b.                    Terminal: vscode 
       `Y$$b.                 CPU: Common KVM (2) @ 2.992GHz 
          `"Y$b._             GPU: 00:02.0 Vendor 1234 Device 1111 
              `"""            Memory: 949MiB / 1970MiB
```
### Mise en place de l'utilisateur

```bash
su root

# Ajout de l'utilisateur 
adduser ansible sudo 

# Modification du groupe propriétaire du répertoire
sudo chown -R ansible:ansible /home/ansible/Ansible-clef-publique

# Modification des autorisations des répertoires
find /home/ansible/Ansible-clef-publique -type d -print0 | sudo xargs -0 chmod 700

# Modification des autorisations des fichiers
find /home/ansible/Ansible-clef-publique -type f -print0 | sudo xargs -0 chmod 600
```

### Git
**Généré un couple de clef (mettre un mot de passe est très important ! Cette clef sera par la suite en lecture publique sur le serveur)**
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/ansible
Enter passphrase (empty for no passphrase): 
```

**Mettre la clef publique dans son trousseau de clef gitlab : [lien](https://git.[...].com/-/profile/keys)**

**Cloner le repo**
```bash
git clone git@git.[...].com:r.lechappe/Ansible-clef-publique.git
```

**Configuration d'un alias pour git push plus facilement (Le mot de passe de la clef privé vous sera demandé ici)**

Bash
```bash
echo 'alias gitset="eval `ssh-agent -s` && ssh-add ~/.ssh/ansible"' >> ~/.bashrc && source ~/.bashrc && git push
```
Zsh
```bash
echo 'alias gitset="eval `ssh-agent -s` && ssh-add ~/.ssh/ansible"' >> ~/.zshrc && source ~/.zshrc && git push
```
### Installation d'un serveur Visual Studio Code Server

**Installation de visual studio code server (version : 4.13.0)**

```bash
su ansible
export VERSION=4.13.0
curl -fOL https://github.com/coder/code-server/releases/download/v$VERSION/code-server_${VERSION}_amd64.deb
sudo dpkg -i code-server_${VERSION}_amd64.deb
sudo systemctl enable --now code-server@ansible
sudo echo "<ip>    ansible" >> /etc/hosts
```

**Assurez-vous que Nginx est installé sur votre machine :**

```bash
sudo apt update
sudo apt install -y nginx
```

**Ouvrez le fichier de configuration de Nginx avec un éditeur de texte :**
```bash
sudo nano /etc/nginx/sites-available/code-server
```

**Remplacez le contenu du fichier avec la configuration suivante :**
```conf
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name 10.2.1.84;
        ssl_certificate /etc/nginx/cert.crt;
        ssl_certificate_key /etc/nginx/cert.key;


    location / {
        proxy_pass http://localhost:8080/;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection upgrade;
        proxy_set_header Accept-Encoding gzip;
    }
}
```

**Générez un certificat auto-signé en utilisant les commandes suivantes :**

```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/cert.key -out /etc/nginx/cert.crt
```

**Activez la configuration en créant un lien symbolique :**

```bash
sudo ln -s /etc/nginx/sites-available/code-server /etc/nginx/sites-enabled/code-server
```

**Verification de la syntaxe du fichier de conf**
```
sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

**Redémarrez Nginx pour appliquer les modifications :**

```bash
sudo systemctl restart nginx && sudo systemctl status nginx
```

**Afficher le password**

```bash
cat ~/.config/code-server/config.yaml
```

## Tips and Triks

### Demander a ChatGPT un avis sur chaqune des task effectuer par ton playbook
**Installation du plugin**
```bash
ansible-galaxy collection install sshnaidm.openai
```

**Placé la configuration suivante dans le fichier `ansible.cfg`**
```ini
[callback_openai]
 openai_model="gpt-3.5-turbo"
 temperature_ai="0.8"
 tokens_ai="2048"
```

**L'utilisation du plugin pour tester un playbook se fait grace a la commande suivante :**
```bash
export OPENAI_API_KEY=token
ANSIBLE_CALLBACKS_ENABLED=sshnaidm.openai.openai ansible-playbook playbooks/SSH_public_key.yaml --vault-password-file /etc/vault.txt
```
<details>
  <summary><strong>Resultat de sa reponse</strong></summary>

**`PLAY [Playbook pour le déploiement SSH]`** *****************************************************************

**Explanation**: 
This Ansible playbook is designed to deploy SSH and backup configuration files on all hosts specified in the inventory. It disables the default behavior of gathering facts about the hosts before executing the playbook, and then runs two roles: backup_cfg and ssh_deployment.

**Suggestions**:
- It is a good practice to include a description of the playbook's purpose in a comment at the beginning of the file.
- It is recommended to use a more descriptive name for the playbook, such as "Deploy SSH and backup configuration files".
- Since the playbook is targeting all hosts in the inventory, it may be helpful to specify a specific group of hosts using the "hosts" parameter.
- If the backup_cfg and ssh_deployment roles are not already included in the playbook's directory, it is important to ensure that they are properly installed or referenced in the playbook's requirements file.

`TASK [backup_cfg : include_tasks] `***********************************************************************

**Explanation**: 
The current Ansible code includes a task to retrieve Ansible variables from a separate YAML file named "retrieving_ansible_variables.yaml". 

No suggestions.
included: /home/ansible/Ansible-clef-publique/playbooks/roles/backup_cfg/tasks/retrieving_ansible_variables.yaml for nx-1, hp-1, hp-2

`TASK [backup_cfg : Recuperation des variables ansible]` **************************************************

**Explanation**: 
The current Ansible code is using the "setup" module to gather a subset of Ansible variables, specifically the "min" subset. This will collect basic system information such as the hostname, IP address, and operating system details.

**Suggestions**:
- It is recommended to use a more descriptive name for the task, such as "Gather Ansible Facts". This will make the code more readable and easier to understand for other team members.
- It may be useful to specify the specific variables needed instead of using the "min" subset. This will reduce the amount of data collected and improve performance. For example, "gather_subset: [network, hardware]" will only collect network and hardware related variables.
ok: [hp-1]
ok: [hp-2]
ok: [nx-1]

`TASK [backup_cfg : include_tasks] `***********************************************************************

**Explanation**: 
The current Ansible code is using the "include_tasks" module to include the tasks defined in the "backup_configuration.yaml" file. This means that the tasks in the "backup_configuration.yaml" file will be executed as part of the playbook.

**Suggestions**:
- It is generally a good practice to use descriptive names for the files and tasks in Ansible. Consider renaming the "backup_configuration.yaml" file to something more descriptive, such as "backup_database.yaml" or "backup_files.yaml".
- It is also a good practice to include comments in the code to explain what each task is doing. Consider adding comments to the tasks in the "backup_configuration.yaml" file to make it easier for others to understand the code.
- If the "backup_configuration.yaml" file contains tasks that are only applicable to certain hosts or groups, consider using the "when" condition to limit the execution of those tasks to only the relevant hosts or groups.
included: /home/ansible/Ansible-clef-publique/playbooks/roles/backup_cfg/tasks/backup_configuration.yaml for nx-1, hp-1, hp-2

`TASK [backup_cfg : Backup Configuration (HP ProCurve)] `**************************************************

**Explanation**: 
The current Ansible code performs a backup of the configuration for an HP ProCurve network device using the netmiko module. It specifies the device type as "hp_procurve", provides the necessary login credentials, and sets the path for where to save the configuration backup file. The result of the backup operation is registered for later use, but the task will only run if the network operating system is identified as "hp.procurve".

**Suggestions**:
- It is recommended to use Ansible Vault to encrypt sensitive information such as passwords, instead of storing them in plain text in the playbook.
- The saverunpath should be parameterized to allow for flexibility in where the backup file is saved. This can be achieved by using a variable or prompt for user input.
- Consider adding error handling and logging to the task to provide better visibility into any issues that may arise during the backup operation.
ok: [hp-1]
ok: [hp-2]

[...]

</details>




### Changer ton tout l'arborescence de ton projet la valeur d'un paramètre de ton module :

```bash
grep -r -l 'ancien' /chemin/vers/projet | xargs sed -i -e 's/ancien/nouveau/g'
```

**Explication sur la commande**

- `grep` :
  
  - `-r` : Recherche récursive dans tous les fichiers et répertoires à partir du chemin spécifié.
  - `-l` : Affiche uniquement les noms des fichiers contenant le motif recherché.
- `xargs` : Prend la liste des fichiers trouvés en entrée et exécute la commande sed pour effectuer le remplacement
- `sed` :
  
  - `-i` : Modifie les fichiers en place.
  - `-e` : Spécifie l'expression de remplacement qui suit (ici, la commande de substitution).
  - `s/ancien/nouveau/g` : Remplace toutes les occurrences du motif 'pubkeyhpcurv' par 'nouveau_parametre' sur chaque ligne.

### One line pour donner a Chat GPT tout le contenue d'un role

```bash
find path/to/role -type f ! -name "README.md" -exec sh -c 'echo "---- File: {} ----"; cat -n -v {}' \;
```

<details>
  <summary>Menu déroulant</summary>

```
  ---- File: ssh_deployment/tasks/ssh_configuration.yaml ----
     1  ---
     2  - name: Configure SSH and add public key (NX-OS)
     3    when: ansible_network_os == 'cisco.nxos.nxos'
     4    cisco.nxos.nxos_command:
     5      commands:
     6        - configure terminal
     7        - username {{ username }} role network-admin
     8        - username {{ username }} sshkey {{ ssh_key }}
     9        - command: "username {{ username }} keypair generate rsa 2048 force"
    10
    11  - name: Configure SSH using public key (HP ProCurve)
    12    when: ansible_network_os == 'hp.procurve'
    13    netmikli:
    14      host: "{{ ansible_host }}"
    15      username: "{{ ansible_ssh_user }}"
    16      password: "{{ ansible_ssh_pass }}"
    17      netmiko_device_type: hp_procurve  
    18      HP_procurve_public_key_deployment: "{{ ssh_key }}"
    19      privkeypath: "~/.ssh/id_rsa"
    20    register: result
---- File: ssh_deployment/tasks/disable_telnet.yaml ----
     1  ---
     2  - name: Disable Telnet (NX-OS)
     3    when: ansible_network_os == 'cisco.nxos.nxos'
     4    cisco.nxos.nxos_feature:
     5      feature: telnet
     6      state: disabled
     7
     8
     9  - name: Disable Telnet (HP ProCurve)
    10    when: ansible_network_os == 'hp.procurve'
    11    netmikli:
    12      host: "{{ ansible_host }}"
    13      username: "{{ ansible_ssh_user }}"
    14      password: "{{ ansible_ssh_pass }}"
    15      netmiko_device_type: hp_procurve
    16      HP_procurve_disable_telnet: True
    17    register: result
    18
    19  - debug:
    20      var: result.msg
---- File: ssh_deployment/tasks/setup.yaml ----
     1  ---
     2  - name: Recuperation des variables ansible
     3    setup:  
     4    # Permet d'accM-CM-)dM-CM-) a certaine varible ex : ansible_date_time
     5      gather_subset:
     6      - 'min'---- File: ssh_deployment/tasks/save_configuration.yaml ----
     1  ---
     2  - name: Save Configuration (NX-OS)
     3    when: ansible_network_os == 'cisco.nxos.nxos'
     4    cisco.nxos.nxos_command:
     5      commands:
     6        - copy running-config startup-config
     7
     8  - name: Test deployment (HP ProCurve)
     9    when: ansible_network_os == 'hp.procurve'
    10    netmikli:
    11      host: "{{ ansible_host }}"
    12      username: "{{ ansible_ssh_user }}"
    13      password: "{{ ansible_ssh_pass }}"
    14      netmiko_device_type: hp_procurve
    15  
    16      commands:
    17        - write memory
    18    register: result
---- File: ssh_deployment/tasks/main.yml ----
     1  ---
     2  - name: Include Backup Role
     3    include_role:
     4      name: backup_cfg
     5  
     6  - include_tasks: setup.yaml
     7
     8  - include_tasks: disable_telnet.yaml
     9
    10  - include_tasks: ssh_configuration.yaml
    11
    12  - include_tasks: save_configuration.yaml
---- File: ssh_deployment/meta/main.yml ----
     1  ---
     2  galaxy_info:
     3    role_name: ssh_deployment
     4    author: RaphaM-CM-+l LECHAPPE
     5    description: RM-CM-4le Ansible permettant le dM-CM-)ploiement de clef publique SSH sur des M-CM-)quipements rM-CM-)seaux
     6    company: 
     7    license: MIT
     8    min_ansible_version: 2.14.15
     9    galaxy_tags:
    10      - ssh
    11      - public key
    12      - key
    13      - private key
---- File: ssh_deployment/handlers/main.yml ----
     1  ---
     2  # handlers file for ssh_deployment
---- File: ssh_deployment/vars/main.yaml ----
     1  ---
     2  ssh_key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
---- File: ssh_deployment/defaults/main.yml ----
     1  ---
     2  # defaults file for ssh_deployment
---- File: ssh_deployment/tests/test.yml ----
     1  ---
     2  - hosts: localhost
     3    remote_user: root
     4    roles:
     5      - ssh_deployment
---- File: ssh_deployment/tests/inventory ----
     1  localhost
     2
```
</details>
