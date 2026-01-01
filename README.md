# Ansible utils

## Wazuh tools: simple docker single node setup, agents on Rhel / Rocky / MaxOSX setup
Tools to setup Wazuh agents and server. Server is set up as single node with docker.

### How to use
###### Clone collection git repo
`git clone git@github.com:pyurin/ansible_utils.git ./collections/ansible_collections/pyurin/utils`
###### Add collection to config
add `collections_path = ./collections` to `ansible.cfg`
###### Use in playbook
```
- name: Setup wazuh agent
  hosts: all
  collections:
    - pyurin.utils

  tasks:

    - include_role:
      name: wazuh_agent_setup
```
refer to other playbook examples in `./playbooks` directory.

#### Current roles:
##### get_telegram_chat_id
Gets telegram chat id. 
You should provide bot api key, telegram user id and send a message to bot first.

##### wazuh_agent_requirements
Installs requirements for Wazuh agent (python & python libs).

##### wazuh_agent_setup
Wazuh agent setup (redirects to platform-specific setup).

##### wazuh_agent_setup_osx
Wazuh agent setup on MacOSX.

##### wazuh_agent_setup_rhel
Wazuh agent setup on Rhel / Rocky.

##### wazuh_server_requirements
Installs Wazuh server requirements: docker, python, python libs.

##### wazuh_server_setup_certbot
Installs certbot on Wazuh server as a separate docker container 
and replaces dashboard certificates.

##### wazuh_server_setup_certificates
Replaces Wazuh dashboard certificates (w/o certbot installation).
Certificates copied from `WAZUH_SERVER_CERTIFICATE_FULLCHAIN` and `WAZUH_SERVER_CERTIFICATE_PRIVATEKEY`.

##### wazuh_server_setup_core
Core Wazuh server components setup (using docker single node).

##### wazuh_server_setup_rules
Basic rule fixes for Wazuh server.

##### wazuh_server_telegram_channel
Sets up telegram channel container on Wazuh server for Wazuh notifications.

##### wazuh_server_telegram_integration
Sets up telegram integration for Wazuh server.

#### Vars
###### WAZUH_SERVER_EXTERNAL_HOST
External Wazuh server host (expected to be same for dashboard and manager). 
For example, example-wazuh-server-host.com

###### WAZUH_SERVER_HOST_DIR
Host work dir.  
For example, /private/wazuh or /usr/share/wazuh.

###### WAZUH_DASHBOARD_PASS:
Dashboard password.
For example TEMP_PASSWORD.

###### WAZUH_API_PASS:
API password.
For example TEMP_PASSWORD.

###### WAZUH_AGENT_PASS:
Agent password.
For example TEMP_PASSWORD

###### WAZUH_TELEGRAM_BOT_API_TOKEN
Telegram bot api token.
For example 822332322:XXXXXXXXXXXXX.

###### WAZUH_TELEGRAM_DST_USER:
Telegram user nickname. 
For example, tg_user.

###### WAZUH_TELEGRAM_CHAT_ID
Telegram chat id (between bot and destination user). 
Can be retrieved using role get_telegram_chat_id.
For example, 237123.


## Notes
Currently dev state: 
 - few platforms supported
 - little flexibility
 - not enough documentation
 - not ready for ansible galaxy
For any questions message: p.yurin@gmail.com