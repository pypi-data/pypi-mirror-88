# Copyright (C) 2018  Charlie Hoy <charlie.hoy@ligo.org>
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import numpy as np
from pesummary import conf
from pesummary.utils.utils import logger, check_filename


def read_dat(path, delimiter=None):
    """Grab the parameters and samples in a .dat file

    Parameters
    ----------
    path: str
        path to the result file you wish to read in
    """
    from .numpy import genfromtxt
    return genfromtxt(path, delimiter=delimiter, names=True)


def _write_dat(
    parameters, samples, outdir="./", label=None, filename=None, overwrite=False,
    delimiter=conf.delimiter, default_filename="pesummary_{}.dat", **kwargs
):
    """Write a set of samples to a dat file

    Parameters
    ----------
    parameters: list
        list of parameters
    samples: 2d list
        list of samples. Columns correspond to a given parameter
    outdir: str, optional
        directory to write the dat file
    label: str, optional
        The label of the analysis. This is used in the filename if a filename
        if not specified
    filename: str, optional
        The name of the file that you wish to write
    overwrite: Bool, optional
        If True, an existing file of the same name will be overwritten
    delimiter: str, optional
        The delimiter you wish to use for the dat file
    """
    filename = check_filename(
        default_filename=default_filename, outdir=outdir, label=label,
        filename=filename, overwrite=overwrite
    )
    np.savetxt(
        filename, samples, delimiter=delimiter, header=delimiter.join(parameters),
        comments=''
    )


def write_dat(
    parameters, samples, outdir="./", label=None, filename=None, overwrite=False,
    delimiter=conf.delimiter, **kwargs
):
    """Write a set of samples to a dat file

    Parameters
    ----------
    parameters: nd list
        list of parameters
    samples: nd list
        list of samples. Columns correspond to a given parameter
    outdir: str, optional
        directory to write the dat file
    label: str, optional
        The label of the analysis. This is used in the filename if a filename
        if not specified
    filename: str, optional
        The name of the file that you wish to write
    overwrite: Bool, optional
        If True, an existing file of the same name will be overwritten
    delimiter: str, optional
        The delimiter you wish to use for the dat file
    """
    from pesummary.io.write import _multi_analysis_write

    _multi_analysis_write(
        _write_dat, parameters, samples, outdir=outdir, label=label,
        filename=filename, overwrite=overwrite, delimiter=delimiter,
        file_format="dat", **kwargs
    )
