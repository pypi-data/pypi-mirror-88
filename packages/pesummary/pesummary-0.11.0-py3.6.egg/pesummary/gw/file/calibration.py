# Copyright (C) 2020  Charlie Hoy <charlie.hoy@ligo.org>
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

import os
import numpy as np
from pesummary import conf
from pesummary.utils.utils import logger, check_file_exists_and_rename
from pesummary.utils.dict import Dict


class CalibrationDict(Dict):
    """Class to handle a dictionary of calibration data

    Parameters
    ----------
    detectors: list
        list of detectors
    data: nd list
        list of calibration samples for each detector. Each of the columns
        should represent Frequency, Median Mag, Phase (Rad), -1 Sigma Mag,
        -1 Sigma Phase, +1 Sigma Mag, +1 Sigma Phase

    Attributes
    ----------
    detectors: list
        list of detectors stored in the dictionary

    Methods
    -------
    plot:
        Generate a plot based on the calibration samples stored
    """
    def __init__(self, *args):
        _columns = [
            "frequencies", "magnitude", "phase", "magnitude_lower",
            "phase_lower", "magnitude_upper", "phase_upper"
        ]
        super(CalibrationDict, self).__init__(
            *args, value_class=Calibration, value_columns=_columns
        )

    @property
    def detectors(self):
        return list(self.keys())


class Calibration(np.ndarray):
    """Class to handle Calibration data
    """
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        if obj.shape[1] != 7:
            raise ValueError(
                "Invalid input data. See the docs for instructions"
            )
        return obj

    def save_to_file(self, file_name, comments="#", delimiter=conf.delimiter):
        """Save the calibration data to file

        Parameters
        ----------
        file_name: str
            name of the file name that you wish to use
        comments: str, optional
            String that will be prepended to the header and footer strings, to
            mark them as comments. Default is '#'.
        delimiter: str, optional
            String or character separating columns.
        """
        check_file_exists_and_rename(file_name)
        header = [
            "Frequency", "Median Mag", "Phase (Rad)", "-1 Sigma Mag",
            "-1 Sigma Phase", "+1 Sigma Mag", "+1 Sigma Phase"
        ]
        np.savetxt(
            file_name, self, delimiter=delimiter, comments=comments,
            header=delimiter.join(header)
        )

    def __array_finalize__(self, obj):
        if obj is None:
            return
