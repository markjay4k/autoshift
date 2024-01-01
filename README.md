# AUTOSHIFT

Automatically transfers torrent media files from _Transmission_ to _Jellyfin_
library once seed threshold achieved.

## WHAT IT DOES

Autoshift routinely scans the _Transmission_ library to identify torrents ready
to transfer. A torrent is ready when 
- Download is complete
- Seed threshold is achieved

Once identified as _ready_, the media-type is determined by parsing with 
[`PTN`](https://github.com/divijbindlish/parse-torrent-name) to
determine the appropriate _Jellyfin_ directory. Finally, the torrent is removed 
from _Transmission_ following the transfer.

## LIMITATIONS

- Autoshift uses `transmission_rpc` and only works with [_Transmission Bittorrent
Client_](https://github.com/transmission/transmission).
- If using ZFS, it's recommended for both _Transmission_ and _Jellyfin_ to share the
    same dataset. This makes the torrent transfer simply an update of metadata,
    rather than moving large audio/video files.

## INSTALL

1. Install [Docker Engine and Compose](https://docs.docker.com/engine/install/).
2. Clone autoshift

    ```bash
    git clone git@github.com:markjay4k/autoshift.git
    cd autoshift
    ```

3. create a docker network called `torrents`

    ```bash
    docker network create torrents
    ```

3. create a `.env` file with the following environment variables

    ```yaml
    TR_PATH=/path/to/transmission/downloads/directory
    JF_MOVIES=/path/to/jellyfin/movies/directory
    JF_SHOWS=/path/to/jellyfin/shows/directory
    JF_PATH=/store/media/jellyfin
    TR_HOST_IP=transmission.torrents
    TR_HOST_PORT=9091
    TR_USER=username #optional
    TR_PASS=password #optional
    LOG_LEVEL=DEBUG
    CRON_SCHEDULE=0 */4 * * *
    ```
4. Choose an appropriate scan interval with the `CRON_SCHEDULE` variable. You
   can refer to [Cron GURU](https://crontab.guru/examples.html) for simple
   copy/paste options to use. The example provided is once every 4 hours.
