import base64
import urllib.error
import urllib.parse
import urllib.request

import settings


def update_icecast_metadata(server_url, username, password, mountpoint, title):
    """
    Updates the Icecast metadata for a specific mountpoint.

    :param server_url: The url of the Icecast server. (e.g. http://127.0.0.1:8000)
    :param username: The username for the admin interface (usually 'admin').
    :param password: The admin password set in the Icecast config.
    :param mountpoint: The specific mountpoint to update (e.g., '/mystream').
    :param title: The new StreamTitle to set (e.g., 'Artist - Song Title').
    """
    # The 'StreamTitle' parameter is the standard way to update the "now playing" info.
    # Other metadata fields are not generally supported for legacy streams.
    params = {
        'mount': mountpoint,
        'mode': 'updinfo',
        'song': title
    }

    # URL-encode the parameters
    encoded_params = urllib.parse.urlencode(params)
    url = f"{server_url}/admin/metadata?{encoded_params}"

    try:
        # Send the GET request with authentication
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": settings.REQUESTS_USER_AGENT,
                "Authorization": f"Basic {encoded_credentials}",
            },
        )

        with urllib.request.urlopen(req) as resp:

            if resp.status == 200:
                print(f"Metadata updated successfully to: '{title}'")
            else:
                print(f"Failed to update metadata. Status code: {resp.status}")

    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"An error occurred: {e}")


def get_hls_stream_metadata(stream_url):
    req = urllib.request.Request(stream_url, headers={"User-Agent": settings.REQUESTS_USER_AGENT,})
    with urllib.request.urlopen(req) as resp:
        next_url = resp.read().splitlines()[-1].decode('utf8')

    req = urllib.request.Request(next_url, headers={"User-Agent": settings.REQUESTS_USER_AGENT,})
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode('utf8')


def get_hls_stream_title(stream_url):
    metadata = get_hls_stream_metadata(stream_url=stream_url)

    for line in metadata.splitlines():
        if "#EXTINF" in line:
            _, title = line.split(',', 1)
            return title.strip()


def get_clean_title(value):
    return " ".join(value.split())
