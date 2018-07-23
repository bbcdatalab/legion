import legion.model
import legion.k8s

legion.model.init('test summation', '1.0')

# py_model.properties['prop_1'] = 0.6
# py_model.on_property_change(lambda key: print(key))

secret_storage = K8SPropertyStorage('NAMEPSPACE', 'NAME')

download_from_s3(sk_id=secret_storage['key1'])

def calculate(x):
    # a = legion.model.properties['prop_1']
    return int(x['a']) + int(x['b'])


calculate({'a': 1.0, 'b': 20.1})

legion.model.export_untyped(lambda x: {'result': int(calculate(x))})
legion.model.save('abc.model')
