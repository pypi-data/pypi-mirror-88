# This file is part of IMASPy.
#
# IMASPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IMASPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with IMASPy.  If not, see <https://www.gnu.org/licenses/>.

import pkg_resources
from distutils.version import LooseVersion as V
try:
    __version__ = pkg_resources.get_distribution("imaspy").version
except Exception:
    # Try local wrongly install copy
    try:
        from version import __version__
    except Exception:
        # Local copy or not installed with setuptools.
        # Disable minimum version checks on downstream libraries.
        __version__ = "0.0.0"

import logging
root_logger = logging.getLogger("imaspy")
if V(__version__) < V("0.2"):
    root_logger.critical("You are using the FOSS version of IMASPy. Please use the ITER version"
                         " instead! See `https://git.iter.org/projects/IMAS/repos/imaspy`")
from imaspy import (
    setup_logging,
    imas_ual_env_parsing,
    ids_classes,
)

from imaspy.backends import (
    file_manager,
    xarray_core_indexing,
    xarray_core_utils,
    common,
    ual,
)
