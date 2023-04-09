#!/usr/bin/python3
"""Generates a .tgz archive from the contents of the web_static folder."""
from fabric.api import local
import time


def do_pack():
    """
    Generate a .tgz archive from web_static folder.
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
