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

from pathlib import Path
import time
from typing import Callable
from typing import Optional

from stopit import ThreadingTimeout

from mdbh import environ


def _create_lockfile(file: Path):
    file.with_suffix('.lock').touch()
    return


def _remove_lockfile(file: Path):
    file.with_suffix('.lock').unlink()
    return


def _lockfile_exists(file: Path) -> bool:
    """Check if .lock file exists for current file.
    The suffix of the file is replaced with .lock.

    Returns:
        True if .lock files exist, else False

    """
    return file.with_suffix(".lock").exists()


def _wait_for_lockfile(file: Path, timeout=120):
    """Waits, as long as a .lock file exists for the specified file.
    If no .lock file exists, returns directly.

    Args:
        file:    File to wait for.
        timeout: Number of seconds after which to timeout.

    Raises:
        TimeoutError after timeout seconds.

    """
    if _lockfile_exists(file):
        # Create a context manager for timeout control
        with ThreadingTimeout(seconds=timeout, swallow_exc=True) as mgr:
            assert mgr.state == mgr.EXECUTING
            # Wait, as long as .lock file exists
            while _lockfile_exists(file):
                print(f"Waiting for .lock file {file}.")
                time.sleep(1.0)

        if mgr.state == mgr.TIMED_OUT:
            raise TimeoutError(f"Timeout occurred while waiting for lockfile {file}.")
    return


def _lookup(filename: str) -> Optional[Path]:
    """Check whether file exists in cache folder.
    Files are automatically prefixed with "MDBH_".

    Args:
        filename: Name of file to lookup.

    Returns:
        If present, Path to cached file, else None.
    """
    file_path = Path(environ.get_cache_dir()) / filename
    file_path = file_path.with_name(f"MDBH_{file_path.name}")

    _wait_for_lockfile(file_path)

    if Path.is_file(file_path):
        print(f"Found in cache: {filename}")
        return file_path

    return None


def _save_call(filename: str,
               get_data: Callable[[], bytes],
               force: bool = False) -> Path:
    """Save file to cache from get_data callable.
    Files are automatically prefixed with "MDBH_".

    Args:
        filename: Name of the file to cache.

        get_data: Callable that retrieves binary data.

        force: Whether to force saving even if file exists.

    Raises:
        IOError when file already exists and force=False.
    """
    file_path = Path(environ.get_cache_dir()) / filename
    file_path = file_path.with_name(f"MDBH_{file_path.name}")

    if file_path.is_file() and not force:
        raise IOError(f"Cache file already exists: {file_path}")

    _create_lockfile(file_path)
    try:
        with open(file_path, "wb") as file:
            file.write(get_data())

    except KeyboardInterrupt:
        print("Aborting download. Removing temporary files.")
        file_path.unlink(missing_ok=True)

    except Exception as e:
        print("An exception occured. Removing temporary files.")
        file_path.unlink(missing_ok=True)
        raise e

    except:
        print("An unknown exception occured. Removing temporary files.")
        file_path.unlink(missing_ok=True)

    finally:
        # Always release lockfile
        _remove_lockfile(file_path)

    return file_path


def _save(filename: str,
          data: bytes,
          force: bool = False) -> Path:
    """Save file to cache.
    Files are automatically prefixed with "MDBH_".

    Args:
        filename: Name of the file to cache.

        data: Data bytes to cache.

        force: Whether to force saving even if file exists.

    Raises:
        IOError when file already exists and force=False.
    """
    get_data = lambda: data

    return _save_call(filename, get_data, force)


def get(filename: str,
        get_data: Callable[[], bytes],
        force: bool = False) -> Path:
    """Get filename from cache.
    If it does not yet exist in cache, use get_data to retrieve the data and
    cache the content.

    Args:
        filename: Filename to get.
        get_data: Callable to retrieve file content if file is not yet cached.
        force: Whether to force calling get_data and replacing the possibly cached file.

    Returns:
        Path to cached file.
    """
    cachefile = _lookup(filename)

    if cachefile is None or force:
        cachefile = _save_call(filename, get_data, force=force)

    return cachefile


def empty_cache():
    """Delete all cached files
    """
    cache_dir = Path(environ.get_cache_dir())
    cached_files = list(cache_dir.glob("MDBH_*"))
    print(f"Removing cached files {cached_files}.")
    [f.unlink() for f in cached_files]
    return
