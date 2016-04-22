Jenkins-extra
=============

Applies extra configuration to Jenkins like create job credentials, set aws 
profile credentials, copy ssh keys etc

The password/secrets that will be configured by this role should be stored in
an ansible-vault encrypted file

Ensure `credentials` and `credentials-bindings` plugins are installed on Jenkins.

## Assumption

This role assumes that it will be applied on a host with a running Jenkins server


## Example

For example configuration please see `defaults/main.yml`.

```
- hosts: jenkins

  vars_files:
    - /path/to/your/encrypted-vault.file

  roles:
    - jenkins-extra
```


## Dependencies

none
