import os
import sys
from pathlib import Path
from typing import Union

import flywheel

# Typing shortcut
Container = Union[
    flywheel.Project,
    flywheel.Subject,
    flywheel.Session,
    flywheel.Acquisition,
    flywheel.FileEntry,
    flywheel.AnalysisOutput,
]

PathLike = Union[str, os.PathLike, Path]
