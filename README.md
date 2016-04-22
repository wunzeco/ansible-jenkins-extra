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

For more complete example on configuration please see `defaults/main.yml`.

```
- hosts: jenkins

  ##Remember to keep secrets/passwords in encrypted vault file 
  ## vars_files:
  ##   - /path/to/your/encrypted-vault.file

  vars:
    jenkins_extra_job_creds_config:
      - id: infra-myawesomerepo-git-creds-id
        description: infra-myawesomerepo
        key_file: /var/lib/jenkins/.ssh/infra-myawesomerepo
        user: jenkins
        type: ssh-private-key
      - id: infra-aws-access-key-id-creds-id
        description: infra-aws-access-key-id
        secret: 'someAwsAccessKeyId'
        type: secret-text
      - id: infra-nexus-login-creds-id
        description: infra-nexus-login
        user: jenkins
        pass: P@ssword!
        type: userpass

  roles:
    - jenkins-extra
```


## Dependencies

none
