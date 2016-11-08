# -*- coding: utf-8 -*-
import os
import re


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


def get_consul_hosts_org():
    """
    Find consul hosts. As a precursor to autodiscovery this method checks for
    environment variables. Or falls back to localhost in case of running locally
    :return: a list of tuples: [(host, port)]
    """
    hosts = []
    hosts += [get_env_variable('CONSUL_HOST', '127.0.0.1:8500')]
    hosts += [get_env_variable('CONSUL_HOST_2')]
    hosts += [get_env_variable('CONSUL_HOST_3')]

    return [
        {
            'host': hostport.split(":")[0],
            'port': '8500' if len(hostport.split(':')) == 1 else
            hostport.split(':')[1]
        } for hostport in hosts if hostport is not None]


def get_consul_hosts():
    """
    Find consul hosts. As a precursor to autodiscovery this method checks for
    environment variables. Or falls back to localhost in case of running locally
    :return: a list of tuples: [(host, port)]
    """
    env = _get_environment()
    hosts = list(filter(None, [env[key] for key in env.keys() if
                               key.startswith("CONSUL_HOST")]))
    if len(hosts) == 0:
        hosts += ['localhost:8500']

    return [
        {
            'host': hostport.split(":")[0],
            'port': '8500' if len(hostport.split(':')) == 1 else
            hostport.split(':')[1]
        } for hostport in hosts if hostport is not None]


def register(consul):
    import socket
    s = consul.agent.service
    s.register("Python_app",
               service_id=socket.gethostname(),
               address="ip",
               port=5000,
               http="http://" + "ip" + ":5000/healthcheck",
               interval="10s",
               tags=['python'])


def get_env_variable(name, default_value=None):
    return os.getenv(name, default_value)


def _get_environment():
    return os.environ
