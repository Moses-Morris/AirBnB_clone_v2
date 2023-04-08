#!/usr/bin/python3
"""
	How to generate a tgz file with the contents of a web static folder using fabric api
"""


from fabric.api import *
"""
	what is fabric? It is an api or library that allows user to 
	execute commands remotely Or locally via linux shell
"""
from datetime import datetime


def do_pack():
    """
    this is an archive of the contents in web static folder
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
	Creation of the directory called versions and then checking out : mkdir -p
    """

    local("mkdir -p versions")
    newArchivedFile = local("tar -cvzf {} web_static".format(Archive))
    if newArchivedFile.succeeded:
        return (Archive)
    else:
        return None
