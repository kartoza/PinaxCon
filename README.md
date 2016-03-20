FOSS4G 2016 Talk Submission System
==================================

This system is based on [PinaxCon](https://github.com/pinax/PinaxCon). It was the fastest way to get started with [Symposion](https://github.com/pinax/symposion), so PinaxCon was simply forked for the [FOSS4G 2016](http://2016.foss4g.org/) conference.


Installing it on a new server
-----------------------------

The server needs at least git, python-dev and python-virtualenv installed (probably more).

### Creating directories

    sudo mkdir /opt/proposals
    sudo chown $USER:$USER /opt/proposals
    mkdir -p /opt/proposals/html /opt/proposals/logs


### Installing the Django application

Create directories and install dependencies:

    cd /opt/proposals
    virtualenv env_foss4g
    source env_foss4g/bin/activate
    git clone --recursive https://github.com/vmx/PinaxCon.git foss4g
    cd foss4g
    git submodule update --remote
    pip install -r requirements.txt -r symposion/requirements/base.txt

Create a new secret key:

    python -c'from django.utils.crypto import get_random_string;print(get_random_string(50, "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"))'

Add this key to `/opt/proposals/foss4g/foss4g/settings_prod.py` as the value of `SECRET_KEY`.

Populate the application:

    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py loaddata sites conference proposal_base sitetree sponsor_benefits sponsor_levels boxes
    ./manage.py collectstatic
    deactivate

before you deactivate the virtualenv.


### Creating the index page

Some paths and the virtualenv need to be setup correctly in order to run the Djangp application. The `index.wsgi` is put in a directory outside the actual application for better security. Create the `index.wsgi` in `/opt/proposals/html`:

```
#!/usr/bin/python
import os
import sys
import site

VIRTUALENV = '/opt/proposals/env_foss4g'
DJANGO_APP = '/opt/proposals/foss4g'

site.addsitedir(os.path.join(VIRTUALENV, 'lib/python2.7/site-packages'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'foss4g.settings_prod'

if DJANGO_APP not in sys.path:
    sys.path.append(DJANGO_APP)

activate_env = os.path.join(VIRTUALENV, 'bin/activate_this.py')
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
from dj_static import Cling, MediaCling
application = Cling(MediaCling(get_wsgi_application()))
```


### Setting permissions

    chmod g+w /opt/proposals/foss4g /opt/proposals/foss4g/foss4g.sqlite
    sudo chown $USER:www-data -R /opt/proposals


Setting up Apache
-----------------

It's expected that the server runs Apache 2.4 on a Debian based system (e.g. Ubunut).

Add a new virtual host to the Apache 2.4 server that serves up the Django application.
Create a new vhost file called `/etc/apache2/sites-available/001-proposals.conf`:

```
<VirtualHost *:80>
    ServerName proposals.2016.foss4g.org

    ServerAdmin webmaster@localhost
    DocumentRoot /opt/proposals/html

    ErrorLog /opt/proposals/logs/error.log
    CustomLog /opt/proposals/logs/access.log combined

    WSGIDaemonProcess proposals.2016.foss4g.org maximum-requests=1000
    WSGIProcessGroup proposals.2016.foss4g.org

    WSGIScriptAlias / /opt/proposals/html/index.wsgi

    <Directory /opt/proposals/html>
        Require all granted
    </Directory>
</VirtualHost>
```

Now activate the virtual host:

    sudo a2ensite 001-proposals.conf

And reload the configuration:

    sudo service apache2 reload


Updating generated files
------------------------

Currently the generated files are also committed to ease the deployment, but in case you
need to recreate them run:

    npm install
    ./node_modules/webpack/bin/webpack.js --config=static/webpack.config.js


Updating to newer checkout
--------------------------

    cd /opt/proposals/foss4g
    git pull
    git submodule update --remote
    . /opt/proposals/env_foss4g/bin/activate
    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py collectstatic
    touch /opt/proposals/html/index.wsgi


Adding reviewers
----------------

First create the permissions that are needed:

     ./manage.py create_review_permissions

Now add a new team (through /admin/teams/team/add/) which has the permissions for `can_review_{section_slug}`. Then add the users to the team via /admin/teams/membership/add/ .
