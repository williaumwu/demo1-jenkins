def run(stackargs):
    import json

    # Instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="hostname")
    stack.parse.add_required(key="public_ip")
    stack.parse.add_required(key="private_key_base64")

    # Use docker container to execute ansible playbooks
    stack.parse.add_optional(key="ansible_docker_image",
                             default="config0/ansible-run-env")

    # Add execgroup
    stack.add_execgroup("williaumwu:::demo1-jenkins::jenkins_with_docker")

    # Add substack that fetches the contents of a file on the server
    # using the private key and ipaddress and outputs to the ui
    stack.add_substack("config0-publish:::config0_core::get_contents_host_file")

    # Initialize
    stack.init_variables()
    stack.init_execgroups()
    stack.init_substacks()

    ansible_hosts_file_content = json.dumps({
        "all": [stack.public_ip]
    })

    # Generate stateful id
    stateful_id = stack.random_id(size=10)

    inputargs = {
        "display": True,
        "human_description": "Install Jenkins for Ansible",
        "env_vars": json.dumps({
            "STATEFUL_ID": stateful_id,
            "DOCKER_IMAGE": stack.ansible_docker_image,
            "ANSIBLE_DIR": "var/tmp/ansible",  # provide subdirectory to execute code
            "ANS_VAR_private_key": stack.private_key_base64,  # expects base64
            "ANS_VAR_hosts": stack.b64_encode(ansible_hosts_file_content),  # expects base64
            "ANS_VAR_exec_ymls": "install.yml"
        }),
        "stateful_id": stateful_id,
        "automation_phase": "infrastructure",
        "hostname": stack.hostname
    }

    stack.jenkins_with_docker.insert(**inputargs)

    # Output to ui
    stack.output_to_ui({
        "hostname": stack.hostname,
        "jenkins_ipaddress": stack.public_ip,
        "jenkins_url": f"https://{stack.public_ip}",
        "jenkins_user": "admin"
    })

    # Fetch and outputs jenkins admin password using the stack get_contents_host_file
    arguments = {
        "remote_file": "/var/lib/jenkins/secrets/initialAdminPassword",
        "key": "jenkins_password",
        "ipaddress": stack.public_ip,
        "private_key_base64": stack.private_key_base64
    }

    human_description = "Publish jenkins admin init password"
    inputargs = {
        "arguments": arguments,
        "automation_phase": "infrastructure",
        "human_description": human_description
    }

    stack.get_contents_host_file.insert(display=True, **inputargs)

    return stack.get_results()
