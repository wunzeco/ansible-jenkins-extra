#!/usr/bin/env python
#
# Description:  
#   Automate creation of credentials on Jenkins
#       *  ssh private key
#       *  secret text
# ToDo: 
#   * username-password
#   * secret file

#
# Author:       Ogonna Iwunze
#
# Date:         08.02.2016
#
# Version:      0.1
#
###############################################################################


import argparse
import requests
import logging
import json
import sys
import os


logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s'
)


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SCOPE = 'GLOBAL'
BASE_URL = 'http://localhost:8080'


def username_password_credentials_payload(opts):
    """ Return secret text payload """
    data = {
        'credentials': {
            'scope': opts['scope'],
            'id': opts['creds_id'],
            'description': opts['description'],
            'username': opts['creds_user'],
            'password': opts['creds_pass'],
            'stapler-class': "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl"
            
        }
    }
    payload = {
        'json': json.dumps(data),
        'Submit': "OK",
    }
    
    return payload


def string_credentials_payload(opts):
    """ Return secret text payload """
    data = {
        'credentials': {
            'scope': opts['scope'],
            'id': opts['creds_id'],
            'description': opts['description'],
            'secret': opts['creds_secret'],
            'stapler-class': "org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl"
        }
    }
    payload = {
        'json': json.dumps(data),
        'Submit': "OK",
    }
    
    return payload


def private_key_source(opts):
    """ Return private key source hash """

    if opts['creds_key_file']:
        private_key_source = {
            'privateKeyFile': opts['creds_key_file'],
            'stapler-class': "com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey$FileOnMasterPrivateKeySource"
        }

    if opts['creds_key_src']:
        with open(opts['creds_key_src'], 'r') as f:
            key = f.read()
        private_key_source = {
            'privateKey': key,
            'stapler-class': "com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey$DirectEntryPrivateKeySource"
        }

    return private_key_source


def ssh_private_key_payload(opts):
    """ Return payload for ssh private key """

    data = {
        'credentials': {
            'scope': opts['scope'],
            'id': opts['creds_id'],
            'description': opts['description'],
            'username': opts['creds_user'],
            'privateKeySource': private_key_source(opts),
            'stapler-class': "com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey"
        }
    }
    payload = {
        'json': json.dumps(data),
        'Submit': "OK",
    }
    
    return payload


def create_credentials(opts):
    """ Create credentials config on Jenkins """

    url = "{0}/credential-store/domain/_/createCredentials".format(opts['base_url'])

    auth = None
    if opts['username'] and opts['password']:
        auth = requests.auth.HTTPBasicAuth(opts['username'], opts['password'])

    r = requests.post(url, auth=auth, data=opts['payload'])
    if r.status_code != requests.codes.ok:
        print r.text
    logging.info('Credentials created - id: (%s)', opts['creds_id'])

    return True


##################
## Args Parsing ##
##################
parser = argparse.ArgumentParser(description='Fetches list of stash repositories')

subparsers = parser.add_subparsers(dest='sub_command')
ssh_priv_key = subparsers.add_parser('ssh-private-key', help='Create SSH user with private key')
ssh_priv_key.add_argument('-u', dest='username', default=False, help='Username for Jenkins login')
ssh_priv_key.add_argument('-p', dest='password', default=False, help='Password for Jenkins login')
ssh_priv_key.add_argument('-l', dest='base_url', default=BASE_URL, help='Jenkins base url')
ssh_priv_key.add_argument('-I', dest='creds_id', required=True, help='Credentials ID')
ssh_priv_key.add_argument('-U', dest='creds_user', required=True, help='SSH Username to configure')
ssh_priv_key.add_argument('-F', dest='creds_key_file', help='Path of ssh private key file on Jenkins master')
ssh_priv_key.add_argument('-K', dest='creds_key_src', help='Source file of private key to read from (locally)')
ssh_priv_key.add_argument('-D', dest='description', default='', help='Description of credentials')
ssh_priv_key.add_argument('-S', dest='creds_scope', default=SCOPE, help='Credentials domain scope')

userpass = subparsers.add_parser('userpass', help='Create username with password')
userpass.add_argument('-u', dest='username', default=False, help='Username for Jenkins login')
userpass.add_argument('-p', dest='password', default=False, help='Password for Jenkins login')
userpass.add_argument('-l', dest='base_url', default=BASE_URL, help='Jenkins base url')
userpass.add_argument('-I', dest='creds_id', required=True, help='Credentials ID')
userpass.add_argument('-U', dest='creds_user', required=True, help='Credentials username to configure')
userpass.add_argument('-P', dest='creds_pass', required=True, help='Credentials password to configure')
userpass.add_argument('-D', dest='description', default='', help='Description of credentials')
userpass.add_argument('-S', dest='creds_scope', default=SCOPE, help='Credentials domain scope')

secret_text = subparsers.add_parser('secret-text', help='Create secrete text')
secret_text.add_argument('-u', dest='username', default=False, help='Username for Jenkins login')
secret_text.add_argument('-p', dest='password', default=False, help='Password for Jenkins login')
secret_text.add_argument('-l', dest='base_url', default=BASE_URL, help='Jenkins base url')
secret_text.add_argument('-I', dest='creds_id', required=True, help='Credentials ID')
secret_text.add_argument('-T', dest='creds_secret', required=True, help='Credentials username to configure')
secret_text.add_argument('-D', dest='description', default='', help='Description of credentials')
secret_text.add_argument('-S', dest='creds_scope', default=SCOPE, help='Credentials domain scope')


args = parser.parse_args()


if __name__ == '__main__':
    opts = vars(args)
    logging.debug("Arguments: %s", opts)
    
    opts['scope'] = SCOPE

    if opts['sub_command'] == 'ssh-private-key':
        if opts['creds_key_file'] and opts['creds_key_src']:
            print 'Specify either key file or key source'
        if not (opts['creds_key_file'] or opts['creds_key_src']):
            print 'Missing key file or key source'
            sys.exit(1)
        opts['payload'] = ssh_private_key_payload(opts)
        create_credentials(opts)
    elif opts['sub_command'] == 'userpass':
        opts['payload'] = username_password_credentials_payload(opts)
        create_credentials(opts)
    elif opts['sub_command'] == 'secret-text':
        opts['payload'] = string_credentials_payload(opts)
        create_credentials(opts)

    sys.exit(0)

