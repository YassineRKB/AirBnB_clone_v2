#!/usr/bin/python3
"""Fabric script (based on the file 2-do_deploy_web_static.py) that
creates and distributes an archive to your web servers, using the
function deploy:"""


import os.path as Path
from datetime import datetime
from fabric.decorators import task
from fabric.api import env, put, run, local
env.hosts = [
    "100.25.192.79",
    "54.84.27.255"
]


def deploy():
    """distributes archive to web servers"""
    archivePath = do_pack()
    if archivePath is None:
        return False
    deployStatus = do_deploy(archivePath)
    return deployStatus


@task
def do_deploy(archive_path):
    """Deploy an archive to web servers."""
    if not Path.exists(archive_path):
        return False
    try:
        filename = Path.basename(archive_path)
        notExtSplit = f"/data/web_static/releases/{filename.split(".")[0]}"
        tmp = f"/tmp/{filename}"
        put(archive_path, tmp)
        run(f"mkdir -p {notExtSplit}/")
        run(f"tar -xzf {tmp} -C {notExtSplit}/")
        run(f"rm {tmp}")
        run(f"mv {notExtSplit}/web_static/* {notExtSplit}/")
        run(f"rm -rf {notExtSplit}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {notExtSplit}/ /data/web_static/current")
        return True
    except Exception:
        return False


@task
def do_pack():
    """func for generating archive from web_static"""
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"versions/web_static_{stamp}.tgz"
    local(f"mkdir -p versions && tar -cvzf {archive_name} web_static/")