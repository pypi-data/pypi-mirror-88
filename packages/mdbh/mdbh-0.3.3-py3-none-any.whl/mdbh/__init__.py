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

try:
    from mdbh._version import __version__
except ImportError:
    __version__ = "local"

__author__ = "Maximilian Schambach"

from .core import get_artifact
from .core import get_artifact_names
from .core import get_conf_databases
from .core import get_dataframe
from .core import get_metric
from .core import get_mongodb
from .core import get_run_names
from .core import get_uri
from .core import resolve_artifacts
from . import environ

environ.set_defaults()
