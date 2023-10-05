#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from
the contents of the web_static folder of your AirBnB
Clone repo, using the function do_pack"""


from datetime import datetime
from fabric.api import local
from fabric.decorators import task


@task
def do_pack():
    """func for generating archive from web_static"""
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{stamp}.tgz"
    local(f"mkdir -p versions && tar -cvzf {archive_name} web_static/")
