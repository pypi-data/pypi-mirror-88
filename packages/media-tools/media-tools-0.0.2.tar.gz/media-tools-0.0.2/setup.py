# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['media_tools', 'media_tools.util', 'media_tools.util.buying']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.2,<5.0.0',
 'pydub>=0.24.1,<0.25.0',
 'pylast>=4.0.0,<5.0.0',
 'requests>=2.25.0,<3.0.0',
 'tinytag>=1.5.0,<2.0.0']

entry_points = \
{'console_scripts': ['backup_lastfm_data = media_tools.backup_lastfm_data:main',
                     'buy_most_played = media_tools.buy_most_played:main',
                     'clean_filenames = media_tools.clean_filenames:main',
                     'copy_from_playlist = media_tools.copy_from_playlist:main',
                     'mixcloud_upload = media_tools.mixcloud_upload:main']}

setup_kwargs = {
    'name': 'media-tools',
    'version': '0.0.2',
    'description': 'Creating and managing playlists, and managing the filenames and directory structure for large numbers of music files.',
    'long_description': 'Toolbox for helping creating and managing playlists, and managing the filenames and directory\nstructure for large numbers of music files. \n\nThis is mostly tailored to my own usage patterns, although it may be useful to others. \n\nUsage\n=====\n\nMusic file library management\n-----------------------------\nIn general: run a script with the `-v` option first to see what it would change. If \nsatisfied, then re-run it with the `-f` option to effect those changes.\n\nRemoving useless duplicate strings from filenames:\n```bash\n$ clean_filenames.py -v clean-filenames --recurse .\n$ clean_filenames.py -v -f clean-filenames --recurse .\n```\nChanging filenames from different numbering schemes to the scheme `01 - filename.ext`:\n```bash\n$ clean_filenames.py -v clean-numbering .\n$ clean_filenames.py -v -f clean-numbering .\n``` \nRemoving stray junk, such as underscores, stray dashes, and stray `[]` and `()` from\nfilenames:\n```bash\n$ clean_filenames.py -v clean-junk .\n$ clean_filenames.py -v -f clean-junk .\n```\nUndoing renamings done with this script, limited to a specified directory and its subfolders,\nor a single file name:\n```bash\n$ clean_filenames.py -v undo .\n$ clean_filenames.py -v -f undo .\n# OR\n$ clean_filenames.py -v -f undo ./subdir/file_name.mp3\n```\nFixing symlinks to files which have been renamed by any of the previous commands:\n```bash\n$ clean_filenames.py -v fix-symlinks .\n$ clean_filenames.py -v -f fix-symlinks .\n```\n\n### Checking results\n\nFinding mp3 files which do not conform to the numbering scheme in general:\n```bash\n$ find . -name \\*.mp3 | grep -vE \'[[:digit:]]+ - .+\\.mp3\'\n```\nFinding mp3 files which have a number in their filename but do not conform to the numbering scheme,\nexcluding some more common use cases:\n```bash\n$ find . -name \\*.mp3 | \\\n    grep -E \'[[:digit:]]+[^/]+\\.mp3\' | \\\n    grep -vE \'[[:digit:]]+ - .+\\.mp3\' | \\\n    grep -vE \'[[:digit:]]{2}\\.mp3\'\n```\n\nAudacious playlist tools\n------------------------\n\nTools for making and repairing playlists containing physical music files from audacious playlists\nand the latest music files. The argument to `--playlist` defaults to the playlist currently playing \nin audacious.\n\nCopying files from the current or specified playlist (as its name in the `playlists` subdir in the \naudacious configuration folder) to a specified target folder, optionally limiting the number of \nfiles to copy to the first NUM, and optionally renaming the files to reflect the position of the\nsong in the playlist:\n```bash\n$ copy_from_playlist.py [-v] copy \\\n    [--playlist PLAYLIST_ID] \\\n    [--number NUM] \\\n    [--renumber] \\\n    TARGET_DIR\n```\nTry to find files in the current playlist which are unavailable because they have been moved, and\nmove them back to the place in the filesystem which is noted on the playlist (does not appear to \nwork currently):\n```bash\n$ copy_from_playlist.py [-v] restore \\\n    [--playlist PLAYLIST_ID]\n```\nCopy the newest files to a specified target:\n```bash\n$ copy_from_playlist.py [-v] copy-newest \\\n    --max-age NUM_DAYS \\\n    --source SOURCE_DIR \\\n    --target TARGET_DIR\n```\n\nTO DO\n=====\n* fix broken symlinks\n  * finding broken symlinks: `$ find DIR -type l -follow -exec readlink -f "{}" \\;`\n* fix audacious playlists which contain moved songs\n* fix filenames with common encoder suffixes\n* make extensions all lowercase\n* migrate undo database to JSON (backup old db first :-/)\n\nTest suite\n==========\n```bash\n$ nosetests --with-coverage --cover-package=util tests/unit ; and mypy .; and flake8 .; and nosetests tests/integration\n```',
    'author': 'Lene Preuss',
    'author_email': 'lene.preuss@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/lilacashes/music-library-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
