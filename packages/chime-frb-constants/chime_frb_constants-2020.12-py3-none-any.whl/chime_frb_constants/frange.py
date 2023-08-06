#!/usr/bin/env python
"""Python range modified for floats."""
# Retrieved from https://github.com/nisanharamati/franges/blob/master/franges/frange.py
# Copyright (C) 2012  POF.com
#
# This file is part of franges.
#
# franges is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# franges is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with franges.  If not, see <http://www.gnu.org/licenses/>.

from math import ceil


def _frange(start, stop=None, step=1):
    """Generate a set of floating point values.

    The task is performed over the range [start, stop)
    with step size step frange([start,] stop [, step ])
    """
    if stop is None:  # pragma: no cover
        yield from range(int(ceil(start)))
    else:
        # create a generator expression for the index values
        indices = (i for i in range(0, int((stop - start) / step)))
        # yield results
        for i in indices:
            yield start + step * i
