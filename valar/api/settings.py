# -*- coding: utf-8 -*-

"""
    Valar API settings and schema
"""

import os


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'valar'
#SERVER_NAME = '127.0.0.1:5000'


RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

ITEM_METHODS = ['GET', 'PATCH', 'DELETE']



miner = {
    'item_title': 'miner',


    'schema': {
        'name': {
            'type': 'string',
            'required': True,
        },
        'hostname': {
            'type': 'string',
        },

    }
}

stats = {

    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/nicolaiarocci/cerberus) for details.
    'schema': {
        'firstname': {
            'type': 'string',
        },
        'lastname': {
            'type': 'string',
            'unique': True,
        },

        'when': {
            'type': 'datetime',
        },
        'miner': {
            'type': 'objectid',
            'required': True,
            # referential integrity constraint: value must exist in the
            # 'miner' collection. Since we aren't declaring a 'field' key,
            # will default to `miner._id` (or, more precisely, to whatever
            # ID_FIELD value is).
            'data_relation': {
                'resource': 'miner'
            }
        },
    }
}



# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = {
    'miner': miner,
    'stats': stats,
}
