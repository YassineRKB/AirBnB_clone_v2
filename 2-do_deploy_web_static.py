#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using the
function do_deploy:"""


import os.path as Path
from fabric.decorators import task
from fabric.api import env, put, run


env.hosts = [
    "100.25.192.79",
    "54.84.27.255"
]


@task
def do_deploy(archive_path):
    """func to distribute archive to web servers"""
    try:
        if not Path.exists(archive_path):
            return False
        filename = Path.basename(archive_path)
        notExtSplit = f'/data/web_static/releases/{filename.split(".")[0]}'
        tmp = f"/tmp/{filename}"
        put(archive_path, tmp)
        run(f"mkdir -p {notExtSplit}/")
        run(f"tar -xzf {tmp} -C {notExtSplit}/")
        run(f"rm {tmp}")
        run(f"mv {notExtSplit}/web_static/* {notExtSplit}/")
        run("rm -rf /data/web_static/current")
        run(f"rm -rf {notExtSplit}/web_static")
        run(f"ln -s {notExtSplit}/ /data/web_static/current")
        return True
    except:
        return False
