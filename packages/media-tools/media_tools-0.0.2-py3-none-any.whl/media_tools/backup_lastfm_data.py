__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

from argparse import ArgumentParser
from calendar import timegm
from datetime import date, datetime
from glob import glob
from pickle import dump, load
from os import environ
from sys import exit
from typing import Dict, Optional

from pylast import LastFMNetwork, User

"""
export PYLAST_USERNAME=ENTER_YOURS_HERE
export PYLAST_API_KEY=ENTER_YOURS_HERE
export PYLAST_API_SECRET=ENTER_YOURS_HERE
"""


def from_datetime(convert_datetime: datetime) -> int:
    return timegm(convert_datetime.utctimetuple())


def year_range(year: int) -> Dict[str, int]:
    start = datetime(year, 1, 1, 0, 0, 0)
    end = datetime(year, 12, 31, 23, 59, 59, 999999)
    return dict(time_from=from_datetime(start), time_to=from_datetime(end))


def start_year(user: User) -> int:
    return date.fromtimestamp(user.get_unixtime_registered()).year


def get_data(user: User, year: Optional[int], limit: Optional[int]) -> Dict:
    year_dates = year_range(year)
    return dict(
        time=datetime.now(),
        play_count=user.get_playcount(),
        tracks=user.get_recent_tracks(limit=limit, **year_dates),
        loved=user.get_loved_tracks(limit=limit),
        top_tracks=user.get_top_tracks(limit=limit),
        top_artists=user.get_top_artists(limit=limit),
        top_albums=user.get_top_albums(limit=limit),
        top_tags=user.get_top_tags(limit=limit),
    )


def combine_data() -> None:
    separate_user_data = {}
    user_data = {}
    for filename in glob('backup_lastfm_20??.pickle'):
        with open(filename, 'rb') as file:
            separate_user_data[filename] = load(file)
        user_data = separate_user_data[filename]
    user_data['tracks'] = sum([data['tracks'] for data in separate_user_data.values()], [])
    with open('backup_lastfm_all.pickle', 'wb') as backup_file:
        dump(user_data, backup_file)


parser = ArgumentParser(
    description="Creates a pickle file from a last.fm user's data"
)
parser.add_argument(
    '-l', '--limit', type=int, default=None,
    help='Max. number of entries to request'
)
parser.add_argument(
    '-y', '--year', type=int, default=None,
    help='Year the data is requested for'
)
parser.add_argument(
    '-c', '--combine', action='store_true',
    help='Combine data sets present in current folder'
)

args = parser.parse_args()
if args.combine:
    combine_data()
    exit(0)

network = LastFMNetwork(
    api_key=environ['PYLAST_API_KEY'], api_secret=environ['PYLAST_API_SECRET']
)

user = network.get_user(environ['PYLAST_USERNAME'])
years = [args.year] if args.year else range(start_year(user), datetime.now().year)

for year in years:
    user_data = get_data(user, year, args.limit)
    with open(f'backup_lastfm_{year}.pickle', 'wb') as backup_file:
        dump(user_data, backup_file)
