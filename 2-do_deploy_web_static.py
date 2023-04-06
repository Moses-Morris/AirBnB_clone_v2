#!/usr/bin/python3
"""
 generating a tgz file with the contents of a web static folder
"""

import os
from fabric.api import *
from datetime import datetime

env.hosts = ["100.26.230.92", "107.22.142.247"]

def do_pack():
    """
    this is an archive of the contents in web static folder
    """
    current = datetime.now()
    fileArchive = "versions/web_static_{}{}{}{}{}{}.tgz".format(current.year,
                                                                current.month,
                                                                current.day,
                                                                current.hour,
                                                                current.minute,
                                                                current.second)
    print("Packing web_static to {}".format(fileArchive))
    """creation of the directory versions
    """
    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(fileArchive))
    if result.succeeded:
        return (fileArchive)
    else:
        return None

    """
    these creates and distributes an  archive to your web servers
    """

def do_deploy(archive_path):
    """deploying the archive to the web servers
    """
    name_path = archive_path.split("/")[1]
    if not os.path.exists(archive_path):
        return False

    result_path = put(archive_path, "/tmp/")
    if result_path.failed:
        return False

    run("mkdir -p /data/web_static/releases/{}".format(name_path[:-4]))

    cmd = "tar -xvzf /tmp/{} -C /data/web_static/releases/{}".format(name_path,
                                                                     name_path[:-4])
    result_path = run(cmd)
    if result_path.failed:
        return False

    result_path = run("rm /tmp/{}".format(name_path))
    if result_path.failed:
        return False

    run("cp -rp /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}/".format(name_path[:-4], name_path[:-4]))

    run("rm -rf /data/web_static/releases/{}/web_static/".format(name_path[:-4]))
    result_path = run("rm /data/web_static/current")
    if result_path.failed:
        return False

    path = "/data/web_static/releases/{}".format(name_path[:-4])
    cmd = "ln -sf {} /data/web_static/current".format(path)
    result_path = run(cmd)
    if result_path.failed:
        return False
    return True
