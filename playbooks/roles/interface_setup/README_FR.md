# interface_setup

## Langue

- [English](./README.md)

## Description
Ce rôle Ansible permet la configuration des interfaces sur un appareil réseau Cisco NX-OS.

## Variables de rôle

Impossible d'utilisé cisco.nxos.nxos_vlans 
 ```
 show vlan | json % Invalid command at '^' marker.
 ```

Et l'utilisation d'une boucle ralentie considérablement l'execution du rôle, les vlan a créé son donc dans le fichier `role/interface_setup/tasks/create_vlan.yaml`

Cependant, certaines variables peuvent être définies par l'utilisateur :
Dans notre cas elle seront dans ce fichier suivant `inventory/network/switch/cisco/host_vars/nx-1.yaml`
### l2_interfaces

Une liste d'interfaces Layer 2 à configurer. Chaque interface est définie par un dictionnaire avec les clés suivantes :

- `name`: le nom de l'interface (par exemple, `Ethernet1/1`).
- `description`: une description de l'interface.
- `enable`: une valeur booléenne pour indiquer si l'interface est activée.
- `mode`: le mode de l'interface, soit `trunk` ou `access`.
- `allowed_vlans`: une liste de VLANs autorisés sur l'interface (seulement applicable si le mode est `trunk`).
- `vlan`: un seul VLAN assigné à l'interface (seulement applicable si le mode est `access`).
- `speed`: la vitesse de l'interface en Mbps.

### l3_interfaces

Une liste d'interfaces Layer 3 à configurer. Chaque interface est définie par un dictionnaire avec les clés suivantes :

- `name`: le nom de l'interface (par exemple, `Ethernet1/5`).
- `description`: une description de l'interface.
- `enable`: une valeur booléenne pour indiquer si l'interface est activée.
- `mtu`: la MTU de l'interface.
- `ipv4`: l'adresse IPv4 de l'interface.
- `speed`: la vitesse de l'interface en Mbps.


## Task
- **`main.yml`**    
Inclut les tâches suivantes :
  - `create_vlan.yaml` : Crée les VLANs.
  - `layer_2.yaml` : Configure les interfaces de couche 2.
  - `layer_3.yaml` : Configure les interfaces de couche 3.
  - `speed.yaml` : Configure la vitesse des interfaces.
  - `description.yaml` : Configure la description et l'état de chaque interface.

- **`description.yaml`**
  - Configure la description et l'état pour chaque interface (NX-OS).
  - Utilise le module cisco.nxos.nxos_interfaces pour effectuer la configuration.
  - Boucle à travers les interfaces définies dans les dictionnaire `l2_interfaces` et `l3_interfaces`.

- **`layer_3.yaml`**
  - Supprime la configuration des interfaces (NX-OS).
  - Désactive le mode switchport pour permettre l'exécution de commandes de couche 3 (NX-OS).
  - Configure les interfaces avec une adresse IPv4 spécifiée.
  - Configure la MTU pour chaque interface (NX-OS).
  - Utilise le module **cisco.nxos.nxos_l3_interfaces** pour effectuer la configuration.
  - Boucle à travers les interfaces définies dans la variable l3_interfaces.

- **`speed.yaml`**
  - Configure la vitesse pour chaque interface (NX-OS).
  - Utilise le module **cisco.nxos.nxos_interfaces** pour effectuer la configuration.
  - Boucle à travers les interfaces définies dans les variables `l2_interfaces` et `l3_interfaces`.

- **`create_vlan.yaml`**
  - Supprime tous les VLANs existants (NX-OS).
  - Crée les VLANs spécifiés (NX-OS).
  - Utilise le module **cisco.nxos.nxos_command** pour effectuer les opérations.
  - Ignorer les erreurs pour la suppression des VLANs existants.
  - Les commandes de création des VLANs sont définies dans ce fichier.

- **`layer_2.yaml`**
  - Active le mode switchport pour permettre l'exécution de commandes de couche 2 (NX-OS).
  - Configure les interfaces en mode access pour les VLANs spécifiés.
  - Configure les interfaces en mode trunk avec les VLANs autorisés spécifiés.
  - Utilise les modules **cisco.nxos.nxos_command** et **cisco.nxos.nxos_l2_interfaces** pour effectuer la configuration.
  - Boucle à travers les interfaces définies dans la variable `l2_interfaces`.

## Exemple de playbook

```yaml
- hosts: nxos_switches
  gather_facts: no

  roles:
    - role: interface_setup
      vars:
        l2_interfaces:
          - name: Ethernet1/1
            description: "Core: bar"
            enable: true
            mode: trunk
            allowed_vlans: "30,40,50"
            speed: 1000
        l3_interfaces:
          - name: Ethernet1/5
            description: "Edge: foo"
            enable: true
            mtu: 9216
            ipv4: "10.1.1.1/24"
            speed: 1000
```

License
-------

MIT

Author Information
------------------

Raphaël L.