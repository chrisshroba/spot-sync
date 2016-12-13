import threading

from requests import get, post
from sys import argv, stderr
from client.command import *
from time import sleep

try:
    client_id = argv[1]
except IndexError:
    stderr.write('Usage: {} <client_id>\n')
    stderr.write('Hint: Use either 1 or 2 for client_id.')
    exit(1)


def start_listening():
    while True:
        # Will block:
        print("Long polling...")
        res = get('http://172.27.37.183:8090/wait_for_song/{}'.format(client_id))
        print('Got response!')
        song_id = res.text.strip()
        print("Playing song: {}".format(song_id))
        play_url(song_id)
        sleep(.2)



t = threading.Thread(target=start_listening, args=())
t.start()

last_url = None
while True:
    url = get_url()
    if last_url != url:
        print("Setting song: {}".format(url))
        res = post(
            'http://172.27.37.183:8090/set_song/{}'.format(client_id),
            data={
                'song': url
            }
        )
        last_url = url
