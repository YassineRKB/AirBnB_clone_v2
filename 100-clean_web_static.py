#!/usr/bin/python3
"""Fabric script (based on the file 3-deploy_web_static.py) that
deletes out-of-date archives, using the function do_clean:"""


import os
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
    if not os.path.exists(archive_path):
        return False
    try:
        fileFullName = archive_path.split("/")[-1]
        fileName = archive_path.split("/")[-1].split(".")[0]
        workPath = "/data/web_static/releases/"
        Makefolder = workPath + fileName
        put(archive_path, "/tmp/")
        run("mkdir -p " + Makefolder)
        run("tar -xzf /tmp/{} -C {}{}/".format(
            fileFullName, workPath, fileName)
            )
        run("rm /tmp/{}".format(fileFullName))
        run("mv {}{}/web_static/* {}{}/".format(workPath, fileName))
        run("rm -rf {}{}/web_static".format(workPath, fileName))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(workPath, fileName))
        print("New version deployed!")
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
    """localy and remotly cleans versions"""
    num = 1
    if int(number) != 0:
        num = int(number)
    path = "/data/web_static/releases/*"
    run("ls -dt {} | head -n -{} | xargs rm -fr".format(path, num))
    local("ls -dt ./versions/* | head -n -{} | xargs rm -fr".format(num))
