# -*- coding: utf-8 -*-1.3
# Copyright (C) 2020  The MDBH Authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from pathlib import Path


def get():
    """Get the MDBH environment variables and values."""
    return {k: val for k, val in os.environ.items() if k[:5] == "MDBH_"}


def set_defaults():
    """Set the default MDBH environment variables and values.

    TODO: Use MDBH config file to define defaults.
    """
    from tempfile import gettempdir
    tmpdir = gettempdir()
    set_cache_dir(tmpdir)


def get_cache_dir() -> str:
    """Set the MDBH cache directory environment variable."""
    return os.environ['MDBH_CACHE_DIR']


def set_cache_dir(cache_dir: str):
    """Set the MDBH cache directory environment variable."""
    os.environ['MDBH_CACHE_DIR'] = cache_dir
    # Create directory and parents, if non-existent
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
