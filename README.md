Valar
=====

[![Valar in action](https://github.com/frodopwns/valar/wiki/valar-thumbnail.png)](https://github.com/frodopwns/valar/wiki/valar.png)

Watching over middle earth since....forever

## To install:

1. Install python
2. Install mongodb
3. Install the following python libraries  
    `sudo pip install flask`  
    `sudo pip install celery`  
    `sudo pip install eve`  
4. Clone valar repo
5. Create and configure valar/valar_settings.py:

> gmail_user  = 'gmail username'
> gmail_password = 'gmail application specific password'  
> toaddrs = ['recipient1@example.com', 'recipient2@example.com']  
> email_sender = "youruser@gmail.com"
> hosts = [
>  'hostname1',
>  'hostname2',
> ]

Note:  The hosts found in valar_settings.py should be set in /etc/hosts or you should use an ip instead

## To run:

`cd path/to/valar/`

1. Start the mongodb daemon  
`mongod`
2. Start the python celery worker which aggregates your data  
`celery -A valar.tasks worker --loglevel=info --beat`
3. `python runserver.py`

