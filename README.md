Valar
=====

[![Valar in action](https://github.com/frodopwns/valar/wiki/valar-thumbnail.png)](https://github.com/frodopwns/valar/wiki/valar.png)

Watching over middle earth since....forever

## To install:

1. Install python
2. Install mongodb
3. Install the following python libraries  
    `sudo pip install requests`  
    `sudo pip install flask`  
    `sudo pip install celery`  
    `sudo pip install eve`  
4. Clone valar repo
5. `cp valar/example.valar_settings.py valar/valar_settings.py`
6. Make any adjustments to valar/valar_settings.py

## To run:

`cd path/to/valar/`

1. Start mongodb  
`sudo service mondodb start`
2. Start the python eve api  
`python valar/api/run.py`
3. Start the python celery worker which aggregates your data  
`celery -A valar.tasks worker --loglevel=info --beat`
4. `python runserver.py`

