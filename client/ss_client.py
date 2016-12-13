import threading

from requests import get, post
from sys import argv, stderr
from client.command import *
from time import sleep
import dateutil.parser


try:
    client_id = argv[1]
except IndexError:
    stderr.write('Usage: {} <client_id>\n')
    stderr.write('Hint: Use either 1 or 2 for client_id.')
    exit(1)

last_url = None


def start_listening():
    while True:
        # Will block:
        res = get('http://172.27.37.183:8090/get_song/{}'.format(client_id))

        if 'spotify' in res.text:
            data = res.json()

            song_id = data['song']
            start_time = dateutil.parser.parse(data['start_time'])

            print("Playing song: {}".format(song_id))

            cur_time = datetime.now()
            diff = cur_time-start_time
            position = diff.seconds + (diff.microseconds / 1000000.)

            play_url(song_id, position=position)
            global last_url
            last_url = song_id
        sleep(.5)


t = threading.Thread(target=start_listening, args=())
t.start()

while True:
    url = get_url()
    if last_url != url:
        print ("Last, cur = {}, {}".format(last_url, url))
        print("Setting song: {}".format(url))
        res = post(
            'http://172.27.37.183:8090/set_song/{}'.format(client_id),
            data={
                'song': url,
                'start_time': get_start_time().isoformat()
            }
        )
        last_url = url
