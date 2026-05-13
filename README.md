Icecast FFmpeg metadata updater
===============================

My favorite internet radio stream changed to HLS which 
icecast (at time of this writing) does not support as a relay.

I configured ffmpeg to relay into icecast and then this project set the title.

This will connect to icecast and check for streams being used, 
as long as the stream description contains ffmpeg, 
it will then connect to that source url and obtain the title.


## Environment Variables:
    - ICECAST_URL=http://127.0.0.1:8654
    - ICECAST_USERNAME=my-username
    - ICECAST_PASSWORD=changeme

    - REFRESH_INTERVAL=30

        How often to check for stream title updates

    - REQUESTS_USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0"

    - LOGGING_LEVEL=INFO

    - TITLE_CONTAINS_REFRESH_INTERVALS=

        Change the refresh interval based on the stream title containing a value:
            
            e.g.
                If title contains "ULTRA DRIVE" change refresh interval to 120s
                If title contains "SATURDAY NIGHT MIX" change refresh interval to 240s
                
                Use | (pipe) to divide assignments and semi-colons to separate title from seconds.
                TITLE;SECONDS|TITLE 2;SECONDS 2
            
            TITLE_CONTAINS_REFRESH_INTERVALS=ULTRA DRIVE;120|SATURDAY NIGHT MIX;240
            
# Icecast configuration expectations:
    
    <authentication>
        <admin-user>my-username</admin-user>
        <source-password>changeme</source-password>
    </authentication>

    <mount type="normal">
        <charset>UTF-8</charset>
        <mount-name>/stream1</mount-name>
        <stream-name>stream1</stream-name>
        <stream-description>stream1 ffmpeg</stream-description>
        <stream-url>http://url-to-hls-stream</stream-url>
    </mount>

    # Ensure "ffmpeg" is within the mounts description

# docker compose example:

    services:

      icecast:
        restart: always
        image: libretime/icecast
        ports:
          - "8654:8654"
        volumes:
          - /mnt/user/appdata/icecast/logs/:/data/
          - /mnt/user/appdata/icecast/icecast-main.xml:/etc/icecast.xml

      ffmpeg-restreamer:
        restart: always
        image: linuxserver/ffmpeg
        command: "-re -i \"http://url-to-hls-stream\" -c:a aac -profile:a aac_low -b:a 128k -vn -content_type 'audio/aac' -f adts \"icecast://source:changeme@icecast:8654/stream1\""
        depends_on:
          - icecast
    
      ffmpeg-metadata:
        restart: always
        image: ghcr.io/iarp/icecast-ffmpeg-metadata-updater:latest
        env_file:
          - ./.env
        depends_on:
          - icecast
          - ffmpeg-restreamer
