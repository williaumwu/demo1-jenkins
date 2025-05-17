def run(stackargs):
    import json

    # Instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="aws_default_region", default="us-east-1")
    stack.parse.add_required(key="hostname")
    stack.parse.add_required(key="ssh_key_name")
    stack.parse.add_optional(key="public_ip",
                             default="null")

    # Use docker container to execute ansible playbooks
    stack.parse.add_optional(key="ansible_docker_image",
                             default="config0/ansible-run-env")

    # Add stacks
    stack.add_substack("williaumwu:::aws_key_gen_and_upload")
    stack.add_substack("williaumwu:::aws_ec2_server")
    stack.add_substack("williaumwu:::jenkins_on_docker")

    # Initialize
    stack.init_variables()
    stack.init_substacks()

    # ssh key gen and upload
    arguments = {
        "ssh_key_name": stack.ssh_key_name,
        "aws_default_region": stack.aws_default_region
    }

    human_description = "Create ssh keys and upload to AWS"
    inputargs = {
        "arguments": arguments,
        "automation_phase": "infrastructure",
        "human_description": human_description
    }

    stack.aws_key_gen_and_upload.insert(display=True, **inputargs)


    # create ec2 server
    arguments = {
        "hostname": stack.hostname,
        "ssh_key_name": stack.ssh_key_name,
        "aws_default_region": stack.aws_default_region
    }

    human_description = "Create ec2 server"
    inputargs = {
        "arguments": arguments,
        "automation_phase": "infrastructure",
        "human_description": human_description
    }

    stack.aws_ec2_server.insert(display=True, **inputargs)

    # install jenkins
    arguments = {
        "hostname": stack.hostname,
        "ssh_key_name": stack.ssh_key_name
    }

    if stack.public_ip:
        arguments["public_ip"] = stack.public_ip

    human_description = "Install and configure Jenkins"
    inputargs = {
        "arguments": arguments,
        "automation_phase": "infrastructure",
        "human_description": human_description
    }

    stack.jenkins_on_docker.insert(display=True, **inputargs)

    return stack.get_results()
