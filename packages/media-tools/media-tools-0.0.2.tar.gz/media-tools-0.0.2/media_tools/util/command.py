from pathlib import Path
from shutil import move
from typing import Any, List, NamedTuple

from .util import print_utf8_safe


class Command(NamedTuple):
    src: Path = None
    dest: Path = None
    info: List[Any] = []

    @property
    def source(self) -> str:
        return str(self.src.resolve())

    @property
    def destination(self) -> str:
        return str(self.dest.resolve())

    def execute(self, verbose: bool, force: bool) -> None:
        if force:
            self.do_execute(verbose)
        self.print(verbose)

    def print(self, verbose: bool) -> None:
        raise NotImplementedError()

    def do_execute(self, verbose: bool) -> None:
        raise NotImplementedError()


class Nothing(Command):
    def do_execute(self, verbose: bool) -> None:
        pass

    def print(self, verbose: bool) -> None:
        pass


class Move(Command):
    def do_execute(self, verbose: bool) -> None:
        try:
            move(self.source, self.destination)
        except FileNotFoundError:
            if verbose:
                print_utf8_safe('FAIL:', self.source, '->', self.destination)

    def print(self, verbose: bool) -> None:
        if verbose:
            print(f'mv {self.source} {self.destination} # {self.info}')


class Relink(Command):
    @property
    def new_symlink(self) -> Path:
        return self.src.parent.joinpath(self.dest.name)

    def do_execute(self, verbose: bool) -> None:
        self.src.unlink()
        self.new_symlink.symlink_to(self.dest)

    def print(self, verbose: bool) -> None:
        if verbose:
            print(f'rm -f {self.source}')
            print(f'ln -s {self.destination} {str(self.new_symlink)}')


Commands = List[Command]
