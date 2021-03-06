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
reset_song=False

def start_listening():
    """
    Retrieve REMOTE song
    :return:
    """
    while True:
        # Will block:
        res = get('http://172.27.37.183:8090/get_song/{}'.format(client_id))

        if 'spotify' in res.text:
            data = res.json()

            song_id = data['song']


            global last_url, reset_song
            last_url = song_id
            reset_song = True
            if song_id != get_url():
                print("Playing song: {}".format(song_id))
                play_url(song_id)

        sleep(.5)


t = threading.Thread(target=start_listening, args=())
t.start()

while True:
    """Send LOCAL Song"""
    reset_song = False
    url = get_url()
    if last_url != url and not reset_song:
        print("Last, cur = {}, {}".format(last_url, url))
        print("Setting song: {}".format(url))
        res = post(
            'http://172.27.37.183:8090/set_song/{}'.format(client_id),
            data={
                'song': url,
            }
        )
    last_url = url
