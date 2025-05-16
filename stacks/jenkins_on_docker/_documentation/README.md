# Jenkins Installation Stack

## Description
This stack automates the installation of Jenkins on a pre-existing server using Ansible in a Docker container. It configures the server, publishes the Jenkins credentials, and makes them available for future use.

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
