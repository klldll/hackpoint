from fabric.api import *


env.hosts = ['zaebee@hackpoint.ru']


def update():
    with cd('/home/zaebee/projects/hackpoint/hackthon'):
        run('git pull')


def status():
    run('sudo supervisorctl status')

def req():
    with cd('/home/zaebee/projects/hackpoint'):
        run('.env/bin/pip install -r hackthon/req.txt')


def upgrade():
    update()
    status()
