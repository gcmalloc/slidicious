from fabric.operations import put, run, sudo, env
from fabric.contrib.files import exists
from fabric.context_managers import cd

DEPENDENCIES = ['git', 'python', 'python-pip', 'libapache2-mod-wsgi', 'apache2', 'python-celery', 'python-redis']


def deploy():
    """deploy the application, if it already exist, it will just update it"""
    sudo("apt-get install {}".format(" ".join(DEPENDENCIES)))
    if exists("slidicious"):
        put("config/slidicious", "/etc/apache2/sites-available/", use_sudo=True)
        sudo("chown root:root /etc/apache2/sites-available/slidicious")
        sudo("ln -s /etc/apache2/sites-available/slidicious /etc/apache2/sites-enabled/001-slidicious")
        put("config/supervisord.conf", "slidicious/src")
        run("git clone git@github.com:gcmalloc/slidicious.git")
        sudo("service apache restart")

    with cd("slidicious"):
        run("git stash")
        run("git pull origin master")

        run("pip install --user -r pip_requirements")
        run("touch slidicious/src/app.py")

def redeploy():
    """Just remove the git repository"""
    run("rm -Rvf slidicious")

def uname():
    run("uname -a")
