import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
env_file = BASE_DIR / ".env"
if env_file.exists():
    with env_file.open() as fo:
        for line in fo.readlines():
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()

            os.environ[key] = value


ICECAST_URL = os.environ['ICECAST_URL']
ICECAST_USERNAME = os.environ['ICECAST_USERNAME']
ICECAST_PASSWORD = os.environ['ICECAST_PASSWORD']

REFRESH_INTERVAL = os.environ.get('REFRESH_INTERVAL', 30)

REQUESTS_USER_AGENT = os.environ.get("REQUESTS_USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0")

