from pathlib import Path
from typing import Dict

from .base_filename_cleaner import BaseFilenameCleaner
from .command import Commands, Move


class UndoCommands(BaseFilenameCleaner):

    def fix_commands(self, undo_info: Dict[str, str]) -> Commands:
        path = self._base_directory.resolve()
        fix_commands: Commands = []
        for source, destination in [
                (dest, src) for src, dest in undo_info.items() if dest.startswith(str(path))
        ]:
            if Path(source).is_file():
                fix_commands.append(Move(Path(source), Path(destination)))
            elif self._verbose:
                print('FAIL', source)
        return fix_commands
