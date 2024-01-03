#!/usr/bin/env python3

from transmission_rpc import Client
from transmission_rpc import torrent
from direntree import DirEntree
import PTN as ptn
import clogger 
import os


class TClient:
    loglevel = os.getenv('LOG_LEVEL')
    jf_movies = os.getenv('JF_MOVIES')
    jf_shows = os.getenv('JF_SHOWS')
    tr_dir = os.getenv('TR_PATH')

    EPISODE = 'episode'
    SEASON = 'season'
    SHOW = 'show'
    MOVIE = 'movie'
    UNDEFINED = 'UNDEFINED'

    def __init__(self) -> None:
        self.log = clogger.log(self.loglevel, logger_name='client')
        self.mod = clogger.mods()
        self.client = Client(
            host=os.getenv('TR_HOST_IP'),
            port=os.getenv('TR_HOST_PORT'),
            username=os.getenv('TR_USER'),
            password=os.getenv('TR_PASS'),
        )
        self.log.debug(f'client connected ({self.client.server_version})')
        self.skipexts = ( 
            'txt', 'png', 'jpg', 'nfo', 'sfv', 'ske', 'ass', 'srt'
        )
        self.keepexts = ('mkv', 'mp4', 'avi')

    def _check_season(self, torr: torrent.Torrent) -> bool:
        data = {'title': [], 'season': []}
        self.log.debug(f'checking if season: {torr.name}')
        for file in torr.get_files():
            fname = os.path.basename(file.name)
            extension = os.path.splitext(fname)[-1]
            if extension in self.skipexts or file.size < 30e6:
                continue
            info = ptn.parse(fname)
            if self.SEASON in info and self.EPISODE in info:
                self.log.debug(
                    f'season: {info[self.SEASON]:02d}, episode {info[self.EPISODE]:02d}'
                )
                for k, v in info.items():
                    if k in data.keys():
                        data[k].append(v)
        _info = {k: set(data[k]) for k in data}
        if len(_info['title']) == 1 and len(_info['season']) == 1:
            _info = {k: data[k].pop() for k in _info}
            return _info, self.SEASON
        elif len(_info['title']) == 0 and len(_info['season']) == 0:
            return ptn.parse(torr.name), self.MOVIE
        else:
            return dict(), self.UNDEFINED 

    def _media_type(self, torr: torrent.Torrent) -> None:
        info = ptn.parse(torr.name)
        if self.SEASON in info and self.EPISODE in info:
            torr.mediatype = self.SHOW
            torr.info = info 
        else:
            info, mediatype = self._check_season(torr)
            torr.mediatype = mediatype
            torr.info = info

    def _download_status(self, torr: torrent.Torrent) -> None:
        if not torr.download_pending and not torr.downloading:
            torr.download_done = True
            return True

    def _seed_status(self, torr: torrent.Torrent) -> None:
        if not torr.seeding:
            torr.seed_done = True
            return True

    def remove_torrent(self, torr: torrent.Torrent) -> None:
        self.client.remove_torrent(torr.id)

    def get_torrents(self):
        return self.client.get_torrents()

    def done_torrents(self):
        """
        returns a generator of all torrents that are ready to transfer
        ready means the torrent met its seed threshold
        transfer means move to corresponding jellyfin directory
        """
        for torr in self.client.get_torrents():
            down_done = self._download_status(torr)
            seed_done = self._seed_status(torr)
            if down_done and seed_done:
                self._media_type(torr)
                try:
                    torrdir = DirEntree(torr)
                except (FileNotFoundError, ValueError) as e:
                    self.log.warning(f'{e}. skipping {torr.name}')
                except AttributeError as e:
                    self.log.warning(f'{e}. skipping {torr.name}')
                else:
                    yield torrdir


if __name__ == '__main__':
    tc = Client()
    for torr in tc.done_torrents():
        print(f'{torr.name}')

