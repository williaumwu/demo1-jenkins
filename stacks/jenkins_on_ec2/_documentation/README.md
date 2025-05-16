# Jenkins Installation Stack

## Description
This stack creates and installs Jenkins on ec2 server.

## Variables

### Required
| Name | Description | Default |
|------|-------------|---------|
| hostname | Server hostname | &nbsp; |
| ssh_key_name | Name label for SSH key | &nbsp; |

### Optional
| Name | Description | Default |
|------|-------------|---------|
| ansible_docker_image | Ansible container image | "config0/ansible-run-env" |
