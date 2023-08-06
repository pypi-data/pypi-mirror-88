#!/usr/bin/env python3

__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import os
import re
from argparse import ArgumentParser, Namespace
from math import log10
from pathlib import Path
from shutil import copy2, SameFileError
from time import time
from typing import List

from media_tools.util import AudaciousTools, find_files


def copy_playlist(
        playlist_id: str, number: int, target: str, verbose: bool=False, renumber: bool=False,
        audacious: AudaciousTools=None
) -> None:
    if not os.path.isdir(target):
        os.mkdir(target)

    if audacious is None:
        audacious = AudaciousTools()

    playlist_id = playlist_id or audacious.get_currently_playing_playlist_id()

    copy_files(audacious.get_files_to_copy(number, playlist_id), target, verbose, renumber)


def strip_leading_numbers(filename: str) -> str:
    return re.sub(r'^\d+\s*[-.]?\s*', '', filename)


def renumber_file(filename: str, number: int, total: int) -> str:
    return "{:0{width}d} - {}".format(
        number, strip_leading_numbers(filename), width=max(int(log10(total)) + 1, 2)
    )


def copy_files(files_to_copy: List[str], target_dir: str, verbose: bool, renumber: bool) -> None:
    for i, file in enumerate(files_to_copy):
        filename = file.split('/')[-1]
        target_filename = renumber_file(filename, i + 1, len(files_to_copy)) if renumber \
            else filename
        if verbose:
            print("{}/{}: {}".format(i + 1, len(files_to_copy), target_filename))
        copy_file(file, os.path.join(target_dir, target_filename))


def copy_file(file: str, target: str) -> None:
    try:
        copy2(file, target)
    except SameFileError as e:
        print(str(e))


def move_files_to_original_places(
        playlist_id: str, music_dir: str='/home/preuss/Music', verbose: bool=False,
        audacious: AudaciousTools=None
) -> None:

    def find(name: str, path: str) -> str:
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
        return ''

    if audacious is None:
        audacious = AudaciousTools()

    playlist_id = playlist_id or audacious.get_currently_playing_playlist_id()
    for file in audacious.files_in_playlist(playlist_id):
        if os.path.isfile(file):
            continue
        filename = file.split('/')[-1]
        target_dir = '/'.join(file.split('/')[:-1])
        original_file = find(filename, music_dir)
        if not original_file:
            continue
        original_file_parent_dir = '/'.join(original_file.split('/')[:-1])
        files_to_move = [
            f for f in os.listdir(original_file_parent_dir)
            if os.path.isfile(original_file_parent_dir + '/' + f)
        ]
        if verbose:
            print('TO MOVE', original_file, target_dir, files_to_move)
        os.makedirs(target_dir, exist_ok=True)
        for f in files_to_move:
            os.rename(original_file_parent_dir + '/' + f, target_dir + '/' + f)
            if verbose:
                print('        MOVING', original_file_parent_dir + '/' + f, target_dir)
        os.rmdir(original_file_parent_dir)


def find_newer_than(base_path: str, seconds: int) -> List[Path]:
    return find_files(Path(base_path), lambda file: time() - os.path.getctime(file) < seconds)


def copy_newest_files(src_dir: str, target_dir: str, max_days: int, verbose: bool=False) -> None:
    to_copy = sorted(find_newer_than(src_dir, max_days * 24 * 60 * 60))
    for i, file in enumerate(to_copy):
        basedir = file.parent
        target_subdir = str(basedir).replace(src_dir, '').split(os.path.sep)
        target_path = Path(target_dir).joinpath(*target_subdir)
        target_path.mkdir(exist_ok=True)
        if verbose:
            print("{}/{} {}".format(i + 1, len(to_copy), str(file).replace(src_dir, '').strip('/')))
        if not file.joinpath(target_path).is_file():
            try:
                copy2(file, target_path)
            except OSError:
                pass


def parse_commandline(args: List[str]) -> Namespace:
    parser = ArgumentParser(
        description="Copy the first N existing files of an audacious playlist to a target folder"
    )
    subparsers = parser.add_subparsers(help='Available subcommands:', dest='subparser')
    # workaround for python issue https://bugs.python.org/issue26510
    subparsers.required = True  # type: ignore

    parser_copy = subparsers.add_parser(
        'copy', help='Copy files on the playlist to a specified target folder'
    )
    parser_copy.add_argument(
        '-p', '--playlist', type=str,
        help='ID of the playlist to copy (default: currently playing)'
    )
    parser_copy.add_argument(
        '-n', '--number', default=0, type=int,
        help='First N files to copy from the playlist (default: all)'
    )
    parser_copy.add_argument(
        '-r', '--renumber', action='store_true',
        help='Rename files to have playlist position prepended to file name'
    )
    parser_copy.add_argument('target', type=str, help='Name of the target folder')

    parser_restore = subparsers.add_parser(
        'restore', help='Move files back to the place in the file system they have on the playlist'
    )
    parser_restore.add_argument(
        '-p', '--playlist', type=str,
        help='ID of the playlist to copy (default: currently playing)'
    )

    parser_copy_newest = subparsers.add_parser(
        'copy_newest', help="Copy the latest files to a specified location"
    )
    parser_copy_newest.add_argument(
        '--max-age', type=int, help='Copy files newer than this many days'
    )
    parser_copy_newest.add_argument(
        '-s', '--source', type=str,
        default=os.path.expanduser('~/Music'),
        help='Source directory. Default: ' + os.path.expanduser('~/Music')
    )
    parser_copy_newest.add_argument('target', type=str, help='Name of the target folder')

    parser.add_argument(
        '-v', '--verbose', action='store_true'
    )

    return parser.parse_args(args)


def main(args: List[str]) -> None:
    opts = parse_commandline(args)
    if opts.subparser == 'copy_newest':
        copy_newest_files(opts.source, opts.target, opts.max_age, verbose=opts.verbose)
    elif opts.subparser == 'restore':
        move_files_to_original_places(opts.playlist, verbose=opts.verbose)
    elif opts.subparser == 'copy':
        copy_playlist(opts.playlist, opts.number, opts.target, opts.verbose, opts.renumber)
    else:
        print("what are you doing?")


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
