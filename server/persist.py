import json
from json.decoder import JSONDecodeError


class DB(object):
    def __init__(self, path, logging=False):
        self.logging = logging
        self.log('DB(\'{}\')'.format(path))
        self.path = path

    def log(self, text):
        if self.logging:
            print("persist: {}".format(text))

    def read_db(self):
        pass
        with open(self.path) as file:
            pass
            contents = file.read()
            try:
                data = json.loads(contents)
            except JSONDecodeError:
                self.write_db({})
                self.log("Error reading data")
                data = {}
            return data

    def write_db(self, data):
        with open(self.path, 'w') as file:
            contents = json.dumps(data)
            file.write(contents)
            self.log('Just wrote: {}'.format(contents))

    def get(self, key):
        self.log('db.get(\'{}\')'.format(key))
        return self.read_db().get(str(key))

    def set(self, key, value):
        self.log('db.set(\'{}\',{})'.format(key, value))
        data = self.read_db()
        data[str(key)] = value
        self.write_db(data)

    def clear(self):
        self.log('db.clear()')
        self.write_db({})
