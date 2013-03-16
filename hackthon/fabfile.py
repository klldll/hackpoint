from fabric.api import *


env.hosts = ['zaebee@hackpoint.ru']


def update():
    with cd('/home/zaebee/projects/hackpoint/hackthon'):
        run('git pull')


def status():
    run('sudo supervisorctl status')


def upgrade():
    update()
    status()
