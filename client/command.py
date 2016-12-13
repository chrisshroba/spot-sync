import subprocess
from datetime import datetime, timedelta


def runProcess(exe):
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while (True):
        retcode = p.poll()  # returns None while subprocess is running
        line = p.stdout.readline()
        yield line
        if (retcode is not None):
            break


def run_applescript(script):
    return list(filter(None, (runProcess([
        'osascript',
        '-e',
        script
    ]
    ))))


def run_sl_applescript(script):
    """
    Single-line-output  Applescript
    """
    try:
        return list(filter(None, (runProcess([
            'osascript',
            '-e',
            script
        ]
        ))))[0].decode("utf-8").strip()
    except Exception:
        return None


def play_url(url, position=None):
    run_applescript('tell application "Spotify" to play track"{}"'.format(url))
    if position:
        set_player_position(position)


def get_url():
    return run_sl_applescript(
        'tell application "Spotify" to spotify url of current track as string')


def _get_one_start_time():
    cur_time = datetime.now()
    pos = run_sl_applescript('tell application "Spotify" to player position')
    start_time = cur_time + timedelta(seconds=-float(pos))
    return start_time


def get_start_time():
    return max([_get_one_start_time() for i in range(3)])


def set_player_position(position):
    run_applescript(
        'tell application "Spotify" to set player position to {}'.format(
            position))

# get_start_time()
