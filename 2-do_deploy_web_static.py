#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using the
function do_deploy:"""


from datetime import datetime
from fabric.api import local
from fabric.decorators import task


env.hosts = [
    "100.25.192.79",
    "54.84.27.255"
]


@task
def do_deploy(archive_path):
    """func to distribute archive to web servers"""
    try:
        with_ext = archive_path.split("/")[-1]
    except EXECPTION:
