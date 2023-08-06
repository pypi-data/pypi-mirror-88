__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path
from sys import argv
from typing import List

from media_tools.util.buying.track import Track, TrackDB
from media_tools.util.buying.distributor import Beatport, Amazon
from media_tools.util.buying.last_fm import LastFM

DEFAULT_TRACK_DB = 'bought.pickle'


def read_datetime(args: str) -> datetime:
    try:
        return datetime.strptime(args, '%Y-%m-%d')
    except ValueError:
        print('Accepted date format: YYYY-MM-DD')
        raise


def parse_commandline(args: List[str]) -> Namespace:
    parser = ArgumentParser(
        description="..."
    )
    parser.add_argument(
        '-u', '--user', required=True, help='Last.FM username'
    )
    parser.add_argument(
        '-k', '--api-key', required=True, help='Last.FM API key'
    )
    parser.add_argument(
        '-l', '--limit', type=int, default=10, help='Maximum number of tracks to display'
    )
    parser.add_argument(
        '-m', '--min-plays', type=int, default=1, help='Minimum number of plays per track'
    )
    parser.add_argument(
        '--buy-up-to', type=int, default=None,
        help='When specified, repeat until this may tracks have been bought'
    )
    period_group = parser.add_mutually_exclusive_group()
    period_group.add_argument(
        '-p', '--period', choices=('overall', '7day', '1month', '3month', '6month', '12month'),
        default='overall', help='Period from which to choose favorite tracks'
    )
    period_group.add_argument(
        '-f', '--from-date', type=read_datetime,
        help='...'
    )
    parser.add_argument(
        '-t', '--to-date', type=read_datetime, default=datetime.now(),
        help='...'
    )
    parser.add_argument(
        '-d', '--track-db', type=str, default=DEFAULT_TRACK_DB,
        help='Name of the file storing already bought tracks'
    )

    return parser.parse_args(args)


def main(opts: Namespace) -> None:
    api = LastFM(opts.user, opts.api_key)

    with TrackDB(Path(opts.track_db)) as trackdb:
        Track.setup((Beatport(), Amazon()), trackdb)
        bought = buy_exactly(api, opts)
    print(bought, 'bought')


def buy_exactly(api: LastFM, opts: Namespace, verbose: bool = False) -> int:
    bought = 0
    while bought < (opts.buy_up_to or 1):
        for track in get_tracks_chunk(api, opts):
            if verbose:
                print(track, track.buy_url())
            track.buy()
            if track.buy_url():
                bought += 1
                if opts.buy_up_to and bought >= opts.buy_up_to:
                    break
    return bought


def get_tracks_chunk(api: LastFM, opts: Namespace, page: int = 1) -> List[Track]:
    return api.get_tracks_by_period(
        from_date=opts.from_date, to_date=opts.to_date, limit=opts.limit, page=page,
        min_plays=opts.min_plays
    ) if opts.from_date else api.get_top_tracks(
        period=opts.period, limit=opts.limit, page=page, min_plays=opts.min_plays
    )


if __name__ == '__main__':
    main(parse_commandline(argv[1:]))
