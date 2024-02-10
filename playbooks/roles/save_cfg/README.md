# save_cfg

## Language

- [Français](./README_FR.md)

This Ansible role allows you to save the current configuration of a Cisco NX-OS or Cisco IOS network device to NVRAM.

## Dependencies

This role depends on the following collections and modules:
- cisco.nxos

To install these dependencies, use the following command:
```bash
ansible-galaxy collection install cisco.nxos
```

To install these dependencies, use the following command:
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

