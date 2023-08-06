#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2016-2020 Chris Lamb <lamby@debian.org>
# Copyright © 2018 Mattia Rizzolo <mattia@debian.org>
#
# diffoscope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# diffoscope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with diffoscope.  If not, see <https://www.gnu.org/licenses/>.

import os
import logging
import tempfile

_DIRS, _FILES = [], []

logger = logging.getLogger(__name__)


def get_named_temporary_file(*args, **kwargs):
    kwargs["dir"] = kwargs.pop("dir", _get_base_temporary_directory())

    f = tempfile.NamedTemporaryFile(*args, **kwargs)
    _FILES.append(f.name)

    return f


def get_temporary_directory(*args, **kwargs):
    kwargs["dir"] = kwargs.pop("dir", _get_base_temporary_directory())

    d = tempfile.TemporaryDirectory(*args, **kwargs)
    _DIRS.append(d)

    return d


def clean_all_temp_files():
    logger.debug("Cleaning %d temp files", len(_FILES))

    for x in _FILES:
        try:
            os.unlink(x)
        except FileNotFoundError:
            pass
        except:  # noqa
            logger.exception("Unable to delete %s", x)
    _FILES.clear()

    logger.debug("Cleaning %d temporary directories", len(_DIRS))

    # Reverse so we delete the top-level directory last.
    for x in reversed(_DIRS):
        try:
            x.cleanup()
        except PermissionError:
            # Recursively reset the permissions of temporary directories prior
            # to deletion to ensure that non-writable permissions such as 0555
            # are removed and do not cause a traceback. (#891363)
            for dirpath, ys, _ in os.walk(x.name):
                for y in ys:
                    os.chmod(os.path.join(dirpath, y), 0o777)
            # try removing it again now
            x.cleanup()
        except FileNotFoundError:
            pass
        except:  # noqa
            logger.exception("Unable to delete %s", x)
    _DIRS.clear()


def _get_base_temporary_directory():
    if not _DIRS:
        d = tempfile.TemporaryDirectory(
            dir=tempfile.gettempdir(), prefix="diffoscope_"
        )

        logger.debug("Created top-level temporary directory: %s", d.name)

        _DIRS.append(d)

    return _DIRS[0].name


def get_tempdir_free_space():
    """
    unsigned long f_frsize   Fundamental file system block size.
    fsblkcnt_t    f_blocks   Total number of blocks on file system in units of f_frsize.
    fsblkcnt_t    f_bfree    Total number of free blocks.
    fsblkcnt_t    f_bavail   Number of free blocks available to
                             non-privileged process.
    """
    statvfs = os.statvfs(tempfile.gettempdir())

    return statvfs.f_frsize * statvfs.f_bavail
