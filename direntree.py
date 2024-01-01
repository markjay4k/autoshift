#!/usr/bin/env python3

from transmission_rpc import torrent
import os


class DirEntree:
    jf_movies = os.getenv('JF_MOVIES')
    jf_shows = os.getenv('JF_SHOWS')
    tr_dir = os.getenv('TR_PATH')

    def __init__(self, torr: torrent.Torrent) -> None:
        self.torr = torr
        self.id = self.torr.id
        self.path = os.path.join(self.tr_dir, torr.name)
        self.name = os.path.basename(self.path)
        self.mediatype = self.torr.mediatype 
        if not torr.download_done:
            raise FileNotFoundError(f'Download incomplete: {torrent.name=}')
        if not torr.download_done:
            raise AttributeError(f'Seeding incomplete: {torrent.name=}')
        if self.mediatype == 'UNDEFINED':
            raise ValueError(f'torrent mediatype is undefined')

    def is_dir(self) -> bool:
        return os.path.isdir(self.path)

    def is_file(self) -> bool:
        return os.path.isfile(self.path)

    def clean_wrapped(self) -> str:
        if self.is_file():
            ext = os.path.splitext(self.name)[-1]
            wrapdir = self.clean_name(ext)
            torrname = self.clean_name()
            return os.path.join(wrapdir, torrname)
        else:
            return self.clean_name() 

    def clean_show_path(self) -> str:
        seriesdir = self.clean_name(name=self.torr.info['title'])
        seasondir = f'{seriesdir}.S{self.torr.info["season"]:02d}'
        if self.mediatype == 'show':
            episodedir = self.clean_wrapped()
        elif self.mediatype == 'season':
            episodedir = ''
        return os.path.join(seriesdir, seasondir, episodedir)

    def new_path(self) -> str:
        if self.mediatype == 'movie':
            cleanpath = self.clean_wrapped()
            return os.path.join(self.jf_movies, cleanpath)
        else:
            cleanpath = self.clean_show_path()
            return os.path.join(self.jf_shows, cleanpath)

    def clean_name(self, *args: str, name: str=None, spacer: str='.') -> str:
        self.chars = (' ', '(', ')', '[', ']', *[x for x in args])
        if name is None:
            name = self.name
        for char in self.chars:
            if char in name:
                name = name.replace(char, spacer)
        if '\'' in name:
            name = name.replace('\'', '')
        name = spacer.join([x for x in name.split(spacer) if x])
        return name
