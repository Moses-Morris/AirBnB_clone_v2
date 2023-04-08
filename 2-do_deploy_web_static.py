#!/usr/bin/pythion3
"""
 	Generating a tgz file with the contents of a web static folder using tar commands
	Using fabric to send data to remote servers.
"""

import os
from fabric.api import *
from datetime import datetime

"""
	import environment hosts: the webservers ip addresses
	you can also import the user variable eg.
	env.user = "ubuntu"
"""

env.hosts = ["54.152.135.110", "54.237.14.152"]

def do_pack():
    """
    	This is an archive of the contents in web static folder
	The archive has a format that includes the time it was compressed.
    """
    currentTime = datetime.now()
    Archive = "versions/web_static_{}{}{}{}{}{}.tgz".format(currentTime.year,
                                                                currentTime.month,
                                                                currentTime.day,
                                                                currentTime.hour,
                                                                currentTime.minute,
                                                                currentTime.second)
    print("Packing web_static to {}".format(Archive))
    """
	Creation of the directory called versions

    """
    local("mkdir -p versions")
    ArchivedFiles = local("tar -cvzf {} web_static".format(Archive))
    if ArchivedFiles.succeeded:
        return (Archive)
    else:
        return None

    """
    	These creates and distributes an  archive to your web servers via fabfic api commands execution
    """

def do_deploy(archive_path):
    """
	Deploying the archivedFiles to the web servers: environment hosts
    """
    pathName = archive_path.split("/")[1]
    if not os.path.exists(archive_path):
        return False

    pathResult = put(archive_path, "/tmp/")
    if pathResult.failed:
        return False
    #Create a directory
    run("mkdir -p /data/web_static/releases/{}".format(pathName[:-4]))

    cmd = "tar -xvzf /tmp/{} -C /data/web_static/releases/{}".format(pathName,
                                                                     pathName[:-4])
    pathResult = run(cmd)
    if pathResult.failed:
        return False

    pathResult = run("rm /tmp/{}".format(pathName))
    if pathResult.failed:
        return False

    run("cp -rp /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}/".format(pathName[:-4], pathName[:-4]))

    run("rm -rf /data/web_static/releases/{}/web_static/".format(pathName[:-4]))
    pathResult = run("rm /data/web_static/current")
    if pathResult.failed:
        return False

    pathUncompress = "/data/web_static/releases/{}".format(pathName[:-4])
    cmd = "ln -sf {} /data/web_static/current".format(pathUncompress)
    pathResult = run(cmd)
    if pathResult.failed:
        return False
    return True
