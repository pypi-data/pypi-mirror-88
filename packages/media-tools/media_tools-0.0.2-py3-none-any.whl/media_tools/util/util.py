__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import os
from pathlib import Path
from typing import Any, Callable, List

Condition = Callable[[Path], bool]


def find_potential_files(base_path: Path, condition: Condition) -> List[Path]:
    return [
        Path(root).joinpath(file)
        for root, _, files in os.walk(str(base_path))
        for file in files
        if condition(Path(root).joinpath(file))
    ]


def find_files(base_path: Path, condition: Condition) -> List[Path]:
    return [file for file in find_potential_files(base_path, condition) if file.exists()]


def find_dirs(base_path: Path, condition: Condition) -> List[Path]:
    return [
        Path(root).joinpath(dir)
        for root, dirs, _ in os.walk(str(base_path))
        for dir in dirs
        if Path(root).joinpath(dir).exists()
        if condition(Path(root).joinpath(dir))
    ]


def print_utf8_safe(*args: Any) -> None:
    try:
        print(*args)
    except UnicodeEncodeError:
        raise ValueError(args)
