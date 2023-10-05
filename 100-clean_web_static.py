#!/usr/bin/python3
"""Fabric script (based on the file 3-deploy_web_static.py) that
deletes out-of-date archives, using the function do_clean:"""


import os.path as Path
from datetime import datetime
from fabric.decorators import task
from fabric.api import env, put, run, local, lcd, cd
env.hosts = [
    "100.25.192.79",
    "54.84.27.255"
]


@task
def do_deploy(archive_path):
    """Deploy an archive to web servers."""
    if not Path.exists(archive_path):
        return False
    try:
        filename = Path.basename(archive_path)
        notExtSplit = "/data/web_static/releases/{}".format(
            filename.split('.')[0]
        )
        tmp = "/tmp/{}".format(filename)
        put(archive_path, tmp)
        run("mkdir -p {}/".format(notExtSplit))
        run("tar -xzf {} -C {}/".format(tmp, notExtSplit))
        run("rm {}".format(tmp))
        run("mv {}/web_static/* {}/".format(notExtSplit, notExtSplit))
        run("rm -rf {}/web_static".format(notExtSplit))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(notExtSplit))
        return True
    except Exception:
        return False


@task
def do_pack():
    """func for generating archive from web_static"""
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(stamp)
    local("mkdir -p versions && tar -cvzf {} web_static/".format(archive_name))

@task
def deploy():
    """distributes archive to web servers"""
    archivePath = do_pack()
    if archivePath is None:
        return False
    deployStatus = do_deploy(archivePath)
    return deployStatus


@task
def do_clean(number=0):
    """Cleans old version's archives from servers."""
    num = 1
    if int(number) != 0:
        num = int(number)
    local("find ./versions/* -type d -prune -print | \
  sort -r | \
  tail -n +{} | \
  xargs rm -fr".format(num+1))
    run("find /data/web_static/releases/* -type d -prune -print | \
  sort -r | \
  tail -n +{} | \
  xargs rm -fr".format(num+1))