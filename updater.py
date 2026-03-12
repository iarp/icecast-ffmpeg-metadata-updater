import logging
import json
import time

import urllib.error
import urllib.request

import helpers, settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(threadName)s] [%(name)s::%(funcName)s:%(lineno)s] %(levelname)s %(message)s'
)

log = logging.getLogger(__name__)

attempted = False
while True:

    try:
        with urllib.request.urlopen(f"{settings.ICECAST_URL}/status-json.xsl") as resp:
            resp_data = json.load(resp)
    except (urllib.error.HTTPError, urllib.error.URLError):
        if not attempted:
            log.info('urllib error connecting to icecast, waiting and retrying')
            time.sleep(10)
            attempted = True
            continue
        log.info("urllib failed to connect to icecast, its down.")
        break

    icecast_status_data = resp_data['icestats']

    for source in icecast_status_data['source']:

        # Only update streams with listeners and based on ffmpeg re-streaming.
        if not source['listeners'] or "ffmpeg" not in source['server_description']:
            continue

        title_from_stream = helpers.get_hls_stream_title(stream_url=source['server_url'])
        log.debug(f"Raw {title_from_stream=}")

        new_title = helpers.get_clean_title(title_from_stream)
        log.debug(f"Cleaned {new_title=}")

        if source.get('title') == new_title:
            log.info(f'Stream title already matches {new_title=}')
            continue

        _, mountpoint = source['listenurl'].rsplit('/', 1)
        mountpoint = f"/{mountpoint}".strip()

        log.info(f"Updating {mountpoint=} with {new_title=}")

        helpers.update_icecast_metadata(
            server_url=settings.ICECAST_URL,
            username=settings.ICECAST_USERNAME,
            password=settings.ICECAST_PASSWORD,
            mountpoint=mountpoint,
            title=new_title,
        )

    log.info(f"Waiting {settings.REFRESH_INTERVAL}s for next refresh.")
    time.sleep(settings.REFRESH_INTERVAL)
