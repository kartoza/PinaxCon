FOSS4G 2016 Talk Submission System
==================================

This system is based on [PinaxCon](https://github.com/pinax/PinaxCon). It was the fastest way to get started with [Symposion](https://github.com/pinax/symposion), so PinaxCon was simply forked for the [FOSS4G 2016](http://2016.foss4g.org/) conference.


Getting Started
----------------

Make sure you are using a virtual environment of some sort (e.g. `virtualenv`).
From outside this checkout:

    virtualenv env_foss4g
    source env_foss4g/bin/activate

When you are inside the virtual environment, get into this checkout:

    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py loaddata sites conference proposal_base sitetree sponsor_benefits sponsor_levels
    ./manage.py createsuperuser
    ./manage.py runserver

To leave the environment, just run `deactivate`.
