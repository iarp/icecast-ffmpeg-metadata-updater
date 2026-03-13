import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
env_file = BASE_DIR / ".env"
if env_file.exists():
    with env_file.open() as fo:
        for line in fo.readlines():
            line = line.strip()
            if not line:
                continue
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()

            os.environ[key] = value


ICECAST_URL = os.environ['ICECAST_URL']
ICECAST_USERNAME = os.environ['ICECAST_USERNAME']
ICECAST_PASSWORD = os.environ['ICECAST_PASSWORD']

REFRESH_INTERVAL = os.environ.get('REFRESH_INTERVAL', 30)

REQUESTS_USER_AGENT = os.environ.get("REQUESTS_USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0")

LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO')

TITLE_CONTAINS_REFRESH_INTERVALS = {}
if _tcri := os.environ.get('TITLE_CONTAINS_REFRESH_INTERVALS'):
    """ Change the refresh interval based on the stream title containing a value:
    
    e.g.
        If title contains "ULTRA DRIVE" change refresh interval to 120s
        If title contains "SATURDAY NIGHT MIX" change refresh interval to 240s
        
        Use | (pipe) to divide assignments and semi-colons to separate title from seconds.
        TITLE;SECONDS|TITLE 2;SECONDS 2
    
    TITLE_CONTAINS_REFRESH_INTERVALS=ULTRA DRIVE;120|SATURDAY NIGHT MIX;240
    
    """
    for line in _tcri.split('|'):
        line = line.strip()
        if not line:
            continue
        tc, ri = line.split(';', )
        TITLE_CONTAINS_REFRESH_INTERVALS[tc] = int(ri)
