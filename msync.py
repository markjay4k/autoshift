#!/usr/bin/env python3

from direntree import DirEntree
from tclient import TClient
import argparse
import clogger
import os


def msync(args):
    dpath = '/store/media' 
    mod = clogger.mods()
    log = clogger.log(args.loglevel)
    log.info(mod.aqua(f'MSYNC: Mork\'s torrent syncing script'))
    log.info(f'-------------------------------------')
    log.debug(f'running with the following argument values:')
    for arg, val in vars(args).items():
        log.debug(f'  - {arg:>8s}: {val}')
    client = TClient()
    torrents = client.done_torrents()
    log.info(f'Starting torrent scan')

    n = None
    for n, torrent in enumerate(torrents):
        if torrent.torr.mediatype!=args.media and args.media!='all':
            log.debug(f'{mod.aqua(torrent.torr.mediatype.upper()):>6s}SKIPPING {torrent.name}')
            continue
        newpath = torrent.new_path()
        oldpath = torrent.path
        log.info(f'{mod.bold(torrent.torr.mediatype.upper()):>6s} -> {torrent.name}')
        if args.verbose:
            log.info(f'   {mod.bold("from")}: {oldpath.replace(dpath, "")}')
            log.info(f'     {mod.bold("to")}:{"":9s}{newpath.replace(dpath, "")}')
        if args.dryrun:
            continue
        else:
            os.renames(old=oldpath, new=newpath)
            log.info(f'  Removing torrent: {torrent.name}')
            client.remove_torrent(torrent)
    else:
        log.info(mod.green(f'Torrent scan complete'))

    if n is None:
        log.info(f'No torrent(s) ready to transfer')
    else:
        if args.dryrun:
            log.info(f'{n+1} torrent(s) ready to transfer to Jellyfin')
            log.info(f'None were transferred because (--dryrun=True)')
            log.info(f'run script without "--dryrun" flag to transfer')
        else:
            log.info(f'{n+1} torrent(s) transferred to Jellyfin library')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dryrun',
        help='run without moving any files (default: False)',
        action='store_true',
    )
    parser.add_argument(
        '-m', '--media',
        help='select mediatype to find and transfer',
        type=str, choices=('movie', 'show', 'season', 'all'),
        default='all'
    )
    parser.add_argument(
        '-v', '--verbose',
        help='display more info (default: False)',
        action='store_true',
    )
    parser.add_argument(
        '-l', '--loglevel',
        help='set log level (default: INFO)',
        type=str, choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
        default='INFO',
    )
    args = parser.parse_args()
    msync(args)


