# Distributed under the terms of the MIT License.

"""
Module containing helper functions for dealing with band structures.
"""

import numpy as np
import itertools as it
from copy import deepcopy

from collections import defaultdict

from pymatgen.electronic_structure.core import Spin
from pymatgen.electronic_structure.bandstructure import (BandStructure,
                                                         BandStructureSymmLine)

