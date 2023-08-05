"""
ToFu: A python library for Tomography for Fusion research
=========================================================

Provides
  1. Objects to handle 3D geometry of diagnostics
  2. Built-in methods for computing key quantities, data treatment, inversions...
  3. Visualisation tools

How to use the documentation
----------------------------
Documentation is available in two forms:
  1. Docstrings provided with the code
  2. Online sphinx-generated documentation, available from
`ToFu's homepage <https://tofuproject.github.io/tofu/>`_.


Available subpackages
---------------------
`geom <tofu.geom.html>`_
    Geometry classes to model the 3D geometry (vacuum vessel, structural
    elements, LOS, etc.)
`data <tofu.data.html>`_
    Data-handling classes (storing, processing, plotting, etc.)
`dumpro <tofu.dumpro.html>`_
    Package for dust movie processing
`dust <tofu.dust.html>`_
    Dust module
imas2tofu
    The imas-compatibility module of tofu (optional)
mag
    Magnetic field lines package (optional)

Available modules
-----------------
_plot
    Module providing a basic routine for plotting a shot overview
defaults
    Store most default parameters of tofu
pathfile
    Provide a class for identification of all tofu objects, and functions for path and file handling
utils
    Miscellaneous helper functions

Utilities
---------
tests
    tofu's unit-tests
__version__
    tofu version string
"""

import sys
import warnings
from .version import __version__

# For tests without display with nosetests
if 'matplotlib.pyplot' not in sys.modules.keys():
    import matplotlib
    matplotlib.use('agg')
    del matplotlib

import tofu.pathfile as pathfile
import tofu.utils as utils

from tofu.utils import save, load, load_from_imas, calc_from_imas
import tofu._plot as _plot
import tofu.geom as geom
import tofu.data as data


# -------------------------------------
#   Try importing optional subpackages
# -------------------------------------

msg = None
dsub = dict.fromkeys(['imas2tofu', 'openadas2tofu', 'mag'])
for sub in dsub.keys():
    try:
        exec('import tofu.{0} as {0}'.format(sub))
        dsub[sub] = True
    except Exception as err:
        dsub[sub] = str(err)

# -------------------------------------
# If any error, populate warning and store error message
# -------------------------------------

lsubout = [sub for sub in dsub.keys() if dsub[sub] is not True]
if len(lsubout) > 0:
    lsubout = ['tofu.{0}'.format(ss) for ss in lsubout]
    msg = "\nThe following subpackages are not available:"
    msg += "\n    - " + "\n    - ".join(lsubout)
    msg += "\n  => see print(tofu.dsub[<subpackage>]) for details."
    warnings.warn(msg)

# -------------------------------------
# Add optional subpackages to __all__
# -------------------------------------

__all__ = ['pathfile', 'utils', '_plot', 'geom', 'data']
for sub in dsub.keys():
    if dsub[sub] is True:
        __all__.append(sub)

# clean-up the mess
del sys, warnings, lsubout, sub, msg
