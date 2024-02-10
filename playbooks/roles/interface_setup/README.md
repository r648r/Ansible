# interface_setup

## Language

- [Francais](./README_FR.md)

## Description
This Ansible role allows for the configuration of interfaces on a Cisco NX-OS network device.

## Requirements

A Cisco NX-OS network device must be available and accessible. The `cisco.nxos` Ansible module must also be installed.

## Role Variables

No default variables are defined for this role.

However, some variables can be user-defined:

### l2_interfaces

A list of Layer 2 interfaces to configure. Each interface is defined by a dictionary with the following keys:

- `name`: the name of the interface (e.g., `Ethernet1/1`).
- `description`: a description of the interface.
- `enable`: a boolean value to indicate whether the interface is enabled.
- `mode`: the mode of the interface, either `trunk` or `access`.
- `allowed_vlans`: a list of allowed VLANs on the interface (only applicable if mode is `trunk`).
- `vlan`: a single VLAN assigned to the interface (only applicable if mode is `access`).
- `speed`: the speed of the interface in Mbps.

### l3_interfaces

A list of Layer 3 interfaces to configure. Each interface is defined by a dictionary with the following keys:

- `name`: the name of the interface (e.g., `Ethernet1/5`).
- `description`: a description of the interface.
- `enable`: a boolean value to indicate whether the interface is enabled.
- `mtu`: the MTU of the interface.
- `ipv4`: the IPv4 address of the interface.
- `speed`: the speed of the interface in Mbps.

### STP

A dictionary for configuring the STP protocol with the following keys:

- `mode`: the mode of STP (e.g., `rapid-pvst`).
- `root`: a range of VLANs to be configured as root primary.
- `root_secondary`: a range of VLANs to be configured as root secondary.
- `loopguard`: a boolean value to indicate whether Loop Guard is enabled.

## Dependencies

None.
## Tasks
- **`main.yml`**
Includes the following tasks:
  - `create_vlan.yaml`: Creates the VLANs.
  - `layer_2.yaml`: Configures layer 2 interfaces.
  - `layer_3.yaml`: Configures layer 3 interfaces.
  - `speed.yaml`: Configures interface speed.
  - `description.yaml`: Configures description and state for each interface.

- **`description.yaml`**
  - Configures description and state for each interface (NX-OS).
  - Uses the `cisco.nxos.nxos_interfaces` module to perform the configuration.
  - Loops through the interfaces defined in the `l2_interfaces` and `l3_interfaces` dictionaries.

- **`layer_3.yaml`**
  - Deletes interface configuration (NX-OS).
  - Disables switchport mode to allow layer 3 commands execution (NX-OS).
  - Configures interfaces with a specified IPv4 address.
  - Configures MTU for each interface (NX-OS).
  - Uses the **cisco.nxos.nxos_l3_interfaces** module to perform the configuration.
  - Loops through the interfaces defined in the `l3_interfaces` variable.

- **`speed.yaml`**
  - Configures speed for each interface (NX-OS).
  - Uses the **cisco.nxos.nxos_interfaces** module to perform the configuration.
  - Loops through the interfaces defined in the `l2_interfaces` and `l3_interfaces` variables.

- **`create_vlan.yaml`**
  - Flushes all existing VLANs (NX-OS).
  - Creates the specified VLANs (NX-OS).
  - Uses the **cisco.nxos.nxos_command** module to perform the operations.
  - Ignores errors for deleting existing VLANs.
  - The commands for creating VLANs are defined in this file.

- **`layer_2.yaml`**
  - Enables switchport mode to allow layer 2 commands execution (NX-OS).
  - Configures interfaces in access mode for specified VLANs.
  - Configures interfaces in trunk mode with specified allowed VLANs.
  - Uses the **cisco.nxos.nxos_command** and **cisco.nxos.nxos_l2_interfaces** modules to perform the configuration.
  - Loops through the interfaces defined in the `l2_interfaces` variable.

## Example Playbook

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
            description: "Edge: weeee"
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
