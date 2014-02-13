from valar_settings import ssh_user, ssh_password
from fabric.api import *
env.user = ssh_user
env.password = ssh_password
def restart(host):
    with settings(host_string=host):
        run("hostname; pwd; ls -al")
