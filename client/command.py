import subprocess


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


def play_url(url):
    run_applescript('tell application "Spotify" to play track"{}"'.format(url))


def get_url():
    return run_sl_applescript(
        'tell application "Spotify" to spotify url of current track as string')


