import os, sys
from fabric.api import *
sys.path.append(os.path.abspath("../"))

from valar.valar_settings import ssh_user, ssh_password
from valar.utils import find_sick_workers
env.user = ssh_user
env.password = ssh_password


def restart(host):
    with settings(host_string=host):
        sudo("/sbin/reboot", shell=False)



    
