#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using the
function do_deploy:"""


import os.path as Path
from fabric.decorators import task
from fabric.api import env, put, run

# Define your remote server hosts
env.hosts = [
    "100.25.192.79",
    "54.84.27.255"
]

@task
def do_deploy(archive_path):
    """Deploy an archive to web servers."""
    if not Path.exists(archive_path):
        return False
    filename = Path.basename(archive_path)
    notExtSplit = f'/data/web_static/releases/{filename.split(".")[0]}'
    tmp = f"/tmp/{filename}"
    if put(archive_path, tmp).failed:
        return False
    if run(f"mkdir -p {notExtSplit}/").failed:
        return False
    if run(f"tar -xzf {tmp} -C {notExtSplit}/").failed:
        return False
    if run(f"rm {tmp}").failed:
        return False
    if run(f"mv {notExtSplit}/web_static/* {notExtSplit}/").failed:
        return False
    if run(f"rm -rf {notExtSplit}/web_static").failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run(f"ln -s {notExtSplit}/ /data/web_static/current", warn=True).failed:
        return False
    return True
    
