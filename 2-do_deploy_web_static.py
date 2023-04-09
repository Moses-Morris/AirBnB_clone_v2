#!/usr/bin/python3
"""The code Generates a .tgz archive from the contents of the web_static folder."""
from fabric.api import *
import time
import os

env.hosts = ["54.152.135.110", "54.237.14.152"]
env.user = "ubuntu"


def do_pack():
    """
    Generate a .tgz archive from web_static folder. and store to a versions folder
    """
    try:
        local("mkdir -p versions")
        file_name = "web_static_{}.tgz".format(
            time.strftime("%Y%m%d%H%M%S"))
        file_path = "versions/{}".format(file_name)
        local("tar -cvzf {} web_static/".format(file_path))
        return file_path
    except:
        return None

def do_deploy(archive_path):
    """
        Distribute archive to your remote server locations. The env.hosts.
    """
    if os.path.exists(archive_path): #This checks if the path exists throught the operating system.
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(newest_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             newest_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(newest_version,
                                                newest_version))
        run("sudo rm -rf {}/web_static".format(newest_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True

    return False
