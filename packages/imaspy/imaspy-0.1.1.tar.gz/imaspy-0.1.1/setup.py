# pylint: disable=wrong-import-position
"""
Packaging settings. Inspired by a minimal setup.py file, the Pandas cython build
and the access-layer setup template.

The reference method of installing is determined by the
[Python Package Authority](https://packaging.python.org/tutorials/installing-packages/)
of which a summary and advanced explanation is on the [IMASPy wiki](https://gitlab.com/imaspy-dev/imaspy/-/wikis/installing)

The installable IMASPy package tries to follow in the following order:
- The style guide for Python code [PEP8](https://www.python.org/dev/peps/pep-0008/)
- The [PyPA guide on packaging projects](https://packaging.python.org/guides/distributing-packages-using-setuptools/#distributing-packages)
- The [PyPA tool recommendations](https://packaging.python.org/guides/tool-recommendations/), specifically:
  * Installing: [pip](https://pip.pypa.io/en/stable/)
  * Environment management: [venv](https://docs.python.org/3/library/venv.html)
  * Dependency management: [pip-tools](https://github.com/jazzband/pip-tools)
  * Packaging source distributions: [setuptools](https://setuptools.readthedocs.io/)
  * Packaging built distributions: [wheels](https://pythonwheels.com/)

On the ITER cluster we handle the environment by using the `IMAS` module load.
So instead, we install packages to the `USER_SITE` there, and do not use
`pip`s `build-isolation`. See [IMAS-584](https://jira.iter.org/browse/IMAS-584)
"""
import argparse
import distutils.sysconfig
import distutils.text_file
import distutils.util
import importlib
import logging
import os
import site
import pkg_resources
import ast

# Allow importing local files, see https://snarky.ca/what-the-heck-is-pyproject-toml/
import sys

# Import other stdlib packages
from distutils.version import LooseVersion as V
from itertools import chain
from pathlib import Path

# Use setuptools to build packages
from setuptools import Extension
from setuptools import __version__ as setuptools_version
from setuptools import find_packages, setup

if sys.version_info < (3, 6):
    sys.exit(
        "Sorry, Python < 3.6 is not supported. Use a different"
        " python e.g. 'module swap python Python/3.6.4-foss-2018a'"
    )


# Check setuptools version before continuing for legacy builds
if V(setuptools_version) < V("42"):
    ee = RuntimeError(
        "Setuptools version outdated. Found"
        f" {V(setuptools_version)} need at least {V('42')}"
    )
    raise ee

# Workaround for https://github.com/pypa/pip/issues/7953
# Cannot install into user site directory with editable source
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]


# Collect env-specific settings
platform = distutils.util.get_platform()  # linux-x86_64
distutils.util.check_environ()

plat_indep_libraries = Path(distutils.sysconfig.get_python_lib())
plat_indep_include = Path(distutils.sysconfig.get_python_inc())

this_file = Path(__file__)
this_dir = this_file.parent.resolve()  # We need to know where we are for many things

package_name = "imaspy"

# Set up 'fancy logging' to display messages to the user
# Import with side-effects, it sets the root logger
loader = importlib.machinery.SourceFileLoader(
    str(this_dir), package_name + "/setup_logging.py"
)
spec = importlib.util.spec_from_loader(loader.name, loader)
setup_logging = importlib.util.module_from_spec(spec)
loader.exec_module(setup_logging)

logger = logging.getLogger("imaspy")

logger.info("pyproject.toml support got added in pip 10. Assuming it is available")

###
# HANDLE USER ENVIRONMENT
###
loader = importlib.machinery.SourceFileLoader(
    str(this_dir), package_name + "/imas_ual_env_parsing.py"
)
spec = importlib.util.spec_from_loader(loader.name, loader)
imas_ual_env_parsing = importlib.util.module_from_spec(spec)
loader.exec_module(imas_ual_env_parsing)

loader = importlib.machinery.SourceFileLoader(str(this_dir), "setup_helpers.py")
spec = importlib.util.spec_from_loader(loader.name, loader)
setup_helpers = importlib.util.module_from_spec(spec)
loader.exec_module(setup_helpers)

# Now that the environment is defined, import the rest of the needed packages

# Prepare DDs if they can be git pulled
setup_helpers.prepare_data_dictionaries()

# Try to grab all necessary environment variables.
# IMAS_PREFIX points to the directory all IMAS components live in
IMAS_PREFIX = os.getenv("IMAS_PREFIX")
if not IMAS_PREFIX or not os.path.isdir(IMAS_PREFIX):
    logger.warning(
        "IMAS_PREFIX is unset or is not a directory. Points to %s. Will not build UAL!",
        IMAS_PREFIX,
    )
    IMAS_PREFIX = "0.0.0"

# Legacy code, we do not need an explicit IMAS_VERSION.
# What is more important, we need the UAL_VERSION we want to link
# to
## Sanity checks, fallback to 0.0.0_0.0.0
# IMAS_VERSION = os.getenv("IMAS_VERSION")
# if not IMAS_VERSION or not len(IMAS_VERSION.split("."))>2:
#    print('IMAS_VERSION is unset or is not formatted as "0.0.0"')
#    IMAS_VERSION = "0.0.0"
# MAJOR = IMAS_VERSION.split(".")[0]
# MINOR = IMAS_VERSION.split(".")[1]

# Grab the UAL_VERSION to build against
UAL_VERSION = os.getenv("UAL_VERSION")
if not UAL_VERSION:
    logger.warning("UAL_VERSION is unset. Will not build UAL!")
    UAL_VERSION = "0.0.0"

(
    ual_symver,
    steps_from_version,
    ual_commit,
) = imas_ual_env_parsing.parse_UAL_version_string(UAL_VERSION)

safe_ual_symver = imas_ual_env_parsing.sanitise_UAL_symver(ual_symver)
ext_module_name = imas_ual_env_parsing.build_UAL_package_name(
    safe_ual_symver, ual_commit
)

# We need source files of the Python HLI UAL library
# to link our build against, the version is grabbed from
# the environment, and they are saved as syubdirectory of
# imaspy
pxd_path = os.path.join(this_dir, "imas")

LANGUAGE = "c"  # Not sure when this is not true
LIBRARIES = "imas"  # We just need the IMAS library
# EXTRALINKARGS = '' # This is machine-specific ignore for now
# EXTRACOMPILEARGS = '' # This is machine-specific ignore for now


###
# Set up Cython build integration
###
### CYTHON COMPILATION ENVIRONMENT

# From https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#multiple-cython-files-in-a-package
REBUILD_LL = False
if REBUILD_LL:
    USE_CYTHON = True
    cython_like_ext = ".pyx" if USE_CYTHON else ".c"

    ###
    # Build extention list
    ###
    extensions = []

    setup_helpers.prepare_ual_sources(ual_symver, ual_commit)
    try:
        import numpy as np
    except ImportError:
        logger.critical("REBUILD_LL is %s, but could not import numpy", REBUILD_LL)
    else:
        extensions = []

    ual_module = Extension(
        name=ext_module_name,
        sources=["imas/_ual_lowlevel.pyx"],  # As these files are copied, easy to find!
        language=LANGUAGE,
        library_dirs=[IMAS_PREFIX + "/lib"],
        libraries=[LIBRARIES],
        # extra_link_args = [ EXTRALINKARGS ],
        # extra_compile_args = [ EXTRACOMPILEARGS ],
        include_dirs=[IMAS_PREFIX + "/include", np.get_include(), pxd_path],
    )
    if "develop" in sys.argv:
        # Make the dir the .so will be put in
        # Somehow not made automatically
        os.makedirs(ext_module_name.split(".")[0], exist_ok=True)
    extensions.append(ual_module)

    ###
    # Set up Cython compilation (or not)
    ###

    if USE_CYTHON:
        try:
            from Cython.Build import cythonize
        except ImportError:
            logger.critical(
                "USE_CYTHON is %s, but could not import Cython",
                USE_CYTHON,
            )
        else:
            extensions = cythonize(extensions)
    else:
        extensions = setup_helpers.no_cythonize(extensions)
else:
    extensions = []


# long_description
# By default, an upload's description will render with reStructuredText. If the description is in an alternate format like Markdown, a package may set the long_description_content_type in setup.py to the alternate format.
with open(os.path.join(this_dir, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

optional_reqs = {}
for req in ["backends_al", "backends_xarray", "core", "examples", "test", "docs"]:
    optional_reqs[req] = distutils.text_file.TextFile(
        this_dir / f"requirements_{req}.txt"
    ).readlines()
install_requires = optional_reqs.pop("core")
# collect all optional dependencies in a "all" target
optional_reqs["all"] = list(chain(*optional_reqs.values()))

if __name__ == "__main__":
    # Legacy setuptools support, e.g. `python setup.py something`
    # See [PEP-0517](https://www.python.org/dev/peps/pep-0517/) and
    # [setuptools docs](https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html#basic-use)
    pyproject: list = distutils.text_file.TextFile("pyproject.toml").readlines()
    requires_line: str = [line for line in pyproject if "requires =" in line][0]
    requires: str = requires_line.split("=", 1)[1]
    setup_requires: list = ast.literal_eval(requires.strip())
    # Rough logic setuptools_scm
    # See https://pypi.org/project/setuptools-scm/
    # or Git projects, the version relies on git describe
    # no distance and clean:
    #     {tag}
    # distance and clean:
    #     {next_version}.dev{distance}+{scm letter}{revision hash}
    # no distance and not clean:
    #     {tag}+dYYYYMMDD
    # distance and not clean:
    #     {next_version}.dev{distance}+{scm letter}{revision hash}.dYYYYMMDD

    # version_scheme: Configures how the local version number is constructed; either an entrypoint name or a callable.
    # version_scheme options:
    # guess-next-dev:
    #   Automatically guesses the next development version (default). Guesses the upcoming release
    #   by incrementing the pre-release segment if present, otherwise by incrementing the micro
    #   segment. Then appends .devN. In case the tag ends with .dev0 the version is not bumped and
    #   custom .devN versions will trigger a error.
    # post-release:
    #   generates post release versions (adds .postN)
    # python-simplified-semver:
    #   Basic semantic versioning. Guesses the upcoming release by incrementing the minor segment
    #   and setting the micro segment to zero if the current branch contains the string 'feature',
    #   otherwise by incrementing the micro version. Then appends .devN. Not compatible with
    #   pre-releases.
    # release-branch-semver:
    #   Semantic versioning for projects with release branches. The same as guess-next-dev
    #   (incrementing the pre-release or micro segment) if on a release branch: a branch whose
    #   name (ignoring namespace) parses as a version that matches the most recent tag up to the
    #   minor segment. Otherwise if on a non-release branch, increments the minor segment and
    #   sets the micro segment to zero, then appends .devN.
    # no-guess-dev:
    #   Does no next version guessing, just adds .post1.devN

    # local_scheme: Configures how the local version number is constructed; either an entrypoint name or a callable.
    # local_scheme options:
    # node-and-date:
    #   adds the node on dev versions and the date on dirty workdir (default)
    # node-and-timestamp:
    #   like node-and-date but with a timestamp of the form {:%Y%m%d%H%M%S} instead
    # dirty-tag:
    #   adds +dirty if the current workdir has changes
    # no-local-version:
    #   omits local version, useful e.g. because pypi does not support it

    # See https://packaging.python.org/specifications/core-metadata/ for allow version strings
    # Example PEP 440 string:
    # Version: 1.0a2

    setup(
        name=package_name,
        description="Pythonic wrappers for the IMAS Access Layer",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://gitlab.com/klimex/imaspy",
        author="Karel van de Plassche",
        author_email="k.l.vandeplassche@differ.nl",
        classifiers=[
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
            "Natural Language :: English",
            "Programming Language :: Python :: 3",
            "Topic :: Utilities",
        ],
        packages=find_packages(),
        # Include files specified by MANIFEST.in
        include_package_data=True,
        # No pyproject.toml for --no-build-installation. Use setup.py instead
        use_scm_version={
            "write_to": package_name + "/version.py",
            'write_to_template': '"{version}"',
            "relative_to": this_file,
            # For tarball installs without metadata (e.g. .git repository)
            "version_scheme": "guess-next-dev",
            "local_scheme": "no-local-version",
            "fallback_version": os.getenv("IMASPY_VERSION", "0.0.0"),
        },
        python_requires=">3.6",
        # Duplicate from pyproject.toml for older setuptools
        setup_requires=setup_requires,
        install_requires=install_requires,
        extras_require=optional_reqs,
        ext_modules=extensions,
    )
