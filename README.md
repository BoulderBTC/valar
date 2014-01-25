Valar
=====

[![Valar in action](https://github.com/frodopwns/valar/wiki/valar-thumbnail.png)](https://github.com/frodopwns/valar/wiki/valar.png)

Watching over middle earth since....forever

Note:  The hosts found in settings.py should be set in /etc/hosts or you should use an ip instead

In order for email notifications to work you need a settings.py file.
Put this in valar/ next to views.py

    gmail_user  = 'gmail username'
    gmail_password = 'gmail application specific password'
    toaddrs = ['recipient1@example.com', 'recipient2@example.com']
    email_sender = "youruser@gmail.com"
    hosts = [
      'hostname1',
      'hostname2',
    ]

## To install:

1. Install python
2. Install mongodb
3. Install the following python libraries  
    `sudo pip install flask`  
    `sudo pip install celery`
    `sudo pip install eve`

## To run:

`cd path/to/valar/`

1. Start the mongodb daemon  
`mongod`
2. Start the python celery worker which aggregates your data  
`celery -A tasks worker --loglevel=info --beat`
3. `python runserver.py`

