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
        return
