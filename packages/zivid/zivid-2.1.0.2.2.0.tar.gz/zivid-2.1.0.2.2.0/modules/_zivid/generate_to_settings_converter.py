"""This file imports used classes, modules and packages."""
import inspect
from collections import namedtuple
from dataclasses import dataclass
from typing import Tuple
import subprocess
from _zivid.common import (
    _create_class,
    _imports,
    _recursion,
    common_to_normal_generation,
)
import tempfile
from pathlib import Path
import inflection
from _zivid._zivid import Settings


def start_traverse():
    common_to_normal_generation(
        internal_class=Settings, settings_type="Settings",
    )
