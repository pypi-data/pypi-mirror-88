__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List

from util.mixcloud import Mix


def parse_commandline(args: List[str]) -> Namespace:
    parser = ArgumentParser(
        description="Creates a mix from audio files and uploads it to Mixcloud"
    )
    parser.add_argument(
        '-d', '--directory', type=str, required=True, help='Directory containing the mix'
    )
    parser.add_argument(
        '-e', '--extensions', nargs='+', default=['flac', 'MP3', 'mp3', 'ogg'],
        help='List of extensions considered for the mix'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true'
    )
    parser.add_argument(
        '-s', '--strict', action='store_true', help='Fail if any required data are missing'
    )
    return parser.parse_args(args)


def main() -> None:
    args: List[str] = sys.argv[1:]
    opts = parse_commandline(args)
    mix = Mix.create(
        Path(opts.directory), tuple(f'?? - *.{ext}' for ext in opts.extensions),
        verbose=opts.verbose, strict=opts.strict
    )
    mix.export()
    mix.upload()


if __name__ == '__main__':
    main()
