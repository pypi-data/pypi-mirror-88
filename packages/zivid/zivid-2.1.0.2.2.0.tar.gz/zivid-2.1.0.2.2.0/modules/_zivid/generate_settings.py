"""This file imports used classes, modules and packages."""
"""This file imports used classes, modules and packages."""
import inspect
from collections import namedtuple
from dataclasses import dataclass
from typing import Tuple
import subprocess
from common import (
    _create_class,
    _imports,
    _recursion,
    common_class_generation,
)


def start_traverse():
    from _zivid._zivid import Settings

    common_class_generation(
        internal_class=Settings,
        settings_type="Settings",
        converter_import="_settings_converter",
    )


# def start_traverse():

#     import tempfile
#     from pathlib import Path
#
#     data_model = _recursion(Settings, indentation_level=0)
#     with tempfile.NamedTemporaryFile(suffix=".py") as temp_file:
#         temp_file = Path(temp_file.name)
#         raw_text = _imports(
#             internal=True,
#             settings=True,
#             additional_imports=("zivid._settings_converter",),
#         )
#         raw_text += _create_settings_py(data_model)
#
#         new_lines = []
#         for line in raw_text.splitlines():
#             new_lines.append(line[4:])
#
#         temp_file.write_text("\n".join(new_lines))
#         print(temp_file.read_text())
#         subprocess.check_output((f"black {temp_file}"), shell=True)
#         print(temp_file.read_text())
#         path_to_settings = (
#             Path(__file__).resolve() / ".." / ".." / "zivid" / "settings__3d.py"
#         ).resolve()
#         path_to_settings.write_text(temp_file.read_text())
#
#
# def _create_settings_py(data_model):
#     return _create_class(data_model, settings_type="Settings")
#
