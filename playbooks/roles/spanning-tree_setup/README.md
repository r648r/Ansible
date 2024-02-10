# spanning-tree_setup

## Language

- [Francais](./README_FR.md)

## Description

This role configures Spanning Tree parameters on Cisco NX-OS devices.
## Variables

The following variables can be defined for this role:

- `STP.mode`: The Spanning Tree mode to configure. By default, it is set to rapid-pvst.
- `STP.root`: The VLAN range for the root bridge. By default, it is set to 10-20.
- `STP.root_secondary`: The VLAN range for the secondary root bridge. By default, it is set to 21-30.
- `STP.loopguard`: Boolean value indicating whether loopguard should be enabled. By default, it is set to true.

## Dependencies

This role depends on the following collections and modules:

- cisco.nxos

To install these dependencies, use the following command:
```bash
ansible-galaxy collection install cisco.nxos
```
## Example Playbook
```yaml
- hosts: servers
  roles:
    - role: spanning-tree_setup
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