import time

from flask import *
from server import persist

app = Flask(__name__)
DATABASE_PATH = "/Users/christophershroba/Developer/projects/spotsync/data.json"


@app.before_first_request
def before_first_request():
    db = persist.DB(DATABASE_PATH)
    db.clear()
    db.set('song', None)
    db.set('client', None)
    db.set('has_set', True)


@app.before_request
def before_request():
    g.db = persist.DB(DATABASE_PATH)


@app.route("/")
def root():
    return "Hello world\n"


# @app.route('/wait_for_song/<client_id>')
# def wait_for_song(client_id):
#     g.db.get('has_set')
#     while True:
#         song = g.db.get('song')
#         client = g.db.get('client')
#         has_set = g.db.get('has_set')
#         print({
#             'song': song,
#             'client': client,
#             'has_set': has_set,
#             'I am': client_id
#         })
#         if client != client_id and not has_set and song is not None:
#             # client A chose a song, let's send it to client B
#             print('{} {}'.format(client, client_id))
#             g.db.set('has_set', True)
#
#             return song
#         time.sleep(.5)


@app.route('/get_song/<client_id>')
def get_song(client_id):
    g.db.get('has_set')

    song = g.db.get('song')
    start_time = g.db.get('start_time')
    client = g.db.get('client')
    has_set = g.db.get('has_set')
    # print({
    #     'song': song,
    #     'client': client,
    #     'has_set': has_set,
    #     'I am': client_id
    # })
    if client != client_id and not has_set and song is not None:
        # client A chose a song, let's send it to client B
        print('{} {}'.format(client, client_id))
        g.db.set('has_set', True)

        data = {
            'song': song,
            'start_time': start_time
        }
        return json.dumps(data)
    else:
        return "None"


@app.route('/set_song/<client_id>', methods=['POST'])
def set_song(client_id):
    song = request.form.get('song')
    start_time = request.form.get('start_time')
    g.db.set('song', song)
    g.db.set('start_time', start_time)
    g.db.set('client', client_id)
    g.db.set('has_set', False)
    return "Success"


@app.route('/rest_test', methods=['GET', 'POST'])
def rest_test():
    method = request.method
    form = request.form
    args = request.args
    data = {
        'method': method,
        'form': form,
        'args': args
    }
    return json.dumps(data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8090, threaded=True)
