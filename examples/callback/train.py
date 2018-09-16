import time

import legion.model

import store


legion.model.init('callback-test', '1.0')
legion.model.define_property('a', 1.0)
legion.model.define_property('b', 0.1)


def process_data(val):
    return val


# Callback function
def on_new_properties():
    print('Entering callback function')
    print('Recalculating....')
    time.sleep(10)
    data_object = {
        'a': legion.model.properties.get('a', cast=legion.model.float32),
        'b': legion.model.properties.get('b', cast=legion.model.float32)
    }
    print('Writing data')
    store.STORAGE.data = data_object
    print('Data has been updated')
    print('Exiting callback function')


# Subscribe to event with callback
legion.model.on_property_update(on_new_properties)


def ep_a(x):
    v = process_data(store.STORAGE.data)
    return {'e': 'a', 'data': v}


def ep_b(x):
    v = process_data(store.STORAGE.data)
    return {'e': 'b', 'data': v}


legion.model.export_untyped(ep_a, endpoint='ep_a')
legion.model.export_untyped(ep_b, endpoint='ep_b')
legion.model.save()