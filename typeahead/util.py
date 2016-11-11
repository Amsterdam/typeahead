# -*- coding: utf-8 -*-
import os
import re

import settings


def get_docker_host():
    """
    Looks for the DOCKER_HOST environment variable to find the VM
    running docker-machine.

    If the environment variable is not found, it is assumed that
    you're running docker on localhost.
    """
    d_host = os.getenv('DOCKER_HOST', None)
    if d_host:
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', d_host):
            return d_host

        return re.match(r'tcp://(.*?):\d+', d_host).group(1)
    return 'localhost'


def in_docker():
    """
    Checks pid 1 cgroup settings to check with reasonable certainty we're in a
    docker env.
    :return: true when running in a docker container, false otherwise
    """
    try:
        return '1:name=openrc:/docker' in open('/proc/1/cgroup', 'r').read()
    except:
        return False


def get_consul_host():
    """
    Retrieve the consul '(host and port)' tuple
    """
    return {
        'host': get_docker_host(),
        'port': 8500 if in_docker() else settings.LOCAL_CONSUL_PORT
    }


def register(consul, agent):
    import socket
    hostport = get_docker_host()
    service_id = socket.gethostname()
    agent.register(settings.SERVICE_NAME,
                   service_id=service_id,
                   address=hostport,
                   port=settings.SERVICE_PORT,
                   http=settings.HEALTH_CHECK_ENDPOINT,
                   interval=settings.HEALTH_CHECK_INTERVAL,
                   tags=['python', 'typeahead'])
    return service_id


def get_env_variable(name, default_value=None):
    return os.getenv(name, default_value)


def _get_environment():
    return os.environ
