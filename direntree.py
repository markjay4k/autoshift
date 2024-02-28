#!/usr/bin/env python3

from transmission_rpc import torrent
import clogger
import os


class DirEntree:
    loglevel = os.getenv('LOG_LEVEL')
    jf_movies = os.getenv('JF_MOVIES')
    jf_shows = os.getenv('JF_SHOWS')
    tr_dir = os.getenv('TR_PATH')

    def __init__(self, torr: torrent.Torrent) -> None:
        self.log = clogger.log(self.loglevel)
        self.mod = clogger.mods()
        self.torr = torr
        self.id = self.torr.id
        self.path = os.path.join(self.tr_dir, torr.name)
        self.name = os.path.basename(self.path)
        self.mediatype = self.torr.mediatype 
        if not torr.download_done:
            error = f'Download incomplete: {torrent.name=}'
            self.log.warning(error)
            raise FileNotFoundError(error)

        if not torr.download_done:
            error = f'Seeding incomplete: {torrent.name=}'
            self.log.warning(error)
            raise AttributeError(error)

        if self.mediatype == 'UNDEFINED':
            error = f'torrent mediatype is undefined'
            self.log.warning(self.mod.bold(error))
            raise ValueError(error)

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
        chars = (' ', '(', ')', '[', ']', *[x for x in args])
        if name is None:
            name = self.name
        for char in chars:
            if char in name:
                name = name.replace(char, spacer)
        if '\'' in name:
            name = name.replace('\'', '')
        name = spacer.join([x for x in name.split(spacer) if x])
        return name

