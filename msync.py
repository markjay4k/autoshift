#!/usr/bin/env python3

from direntree import DirEntree
from tclient import TClient
import argparse
import clogger
import os
#import __init__


def msync(args):
    dpath = '/store/media' 
    log = clogger.log(args.loglevel)
    #log = clogger.log(os.getenv('LOG_LEVEL'))
    log.info(f'MSYNC: Mork\'s torrent syncing script')
    log.info(f'-------------------------------------')
    log.debug(f'running with the following argument values:')
    for arg, val in vars(args).items():
        log.debug(f'  - {arg:>8s}: {val}')
    client = TClient()
    torrents = client.done_torrents()
    log.info(f'')
    log.info(f'Starting torrent scan')
    log.info(f'')
    for n, torrent in enumerate(torrents):
        if torrent.mediatype!=args.media and args.media!='all':
            log.debug(f'{torrent.mediatype.upper():>6s}: SKIPPING {torrent.name}')
            continue
        newpath = torrent.new_path()
        oldpath = torrent.path
        log.info(f'{torrent.mediatype.upper():>6s} -> {torrent.name}')
        if args.verbose:
            log.info(f'    from: {oldpath.replace(dpath, "")}')
            log.info(f'      to: {newpath.replace(dpath, "")}')
        if args.dryrun:
            continue
        else:
            os.renames(old=oldpath, new=newpath)
            log.info(f'  Removing torrent: {torrent.name}')
            client.remove_torrent(torrent)
    else:
        log.info(f'')
        log.info(f'Torrent scan complete')
        log.info(f'')

    if args.dryrun:
        log.info(f'No torrent(s) files were transferred to Jellyfin library')
        log.info(f'run without "--dryrun" flag to transfer')
    else:
        log.info(f'{n+1} torrent(s) were transferred to Jellyfin library')


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


