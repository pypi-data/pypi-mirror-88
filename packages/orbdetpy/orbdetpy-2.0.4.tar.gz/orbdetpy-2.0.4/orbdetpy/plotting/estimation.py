# estimation.py - Plot orbit determination results.
# Copyright (C) 2018-2020 University of Texas
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy
from typing import List
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from orbdetpy import Constant, EstimationType, MeasurementType
from orbdetpy.conversion import get_lvlh_rotation
from orbdetpy.rpc.messages_pb2 import Settings

def plot(cfg: Settings, measurements, orbit_fit, interactive: bool=False,
         output_file_path: str=None, estim_param: bool=True)->List[str]:
    """Plot orbit determination residuals, covariances, and estimated parameters.

    Parameters
    ----------
    cfg : Settings object.
    measurements : List of measurements.
    orbit_fit : Return value from determine_orbit().
    interactive : Show interactive plots if True.
    output_file_path : File path and name prefixes if plots are to be saved.
    estim_param : Plot estimated parameters if True.

    Returns
    -------
    List of plot files if they were saved to disk.
    """

    key = list(cfg.measurements.keys())
    key.sort()
    meas_names = {0: "Azimuth", 1: "Elevation", 2: "Range", 3: "Range Rate", 4: "Right Ascension", 5: "Declination"}
    inp = [m for m in measurements if (len(m.station) > 0 or len(m.values) >= 3)]
    out = [f for f in orbit_fit if (len(f.pre_fit)*len(f.post_fit) > 0)]
    dmcidx, dmcrun = 6, (cfg.estm_DMC_corr_time > 0.0 and cfg.estm_DMC_sigma_pert > 0.0)

    cd, cr = cfg.drag_coefficient.estimation, cfg.rp_coeff_reflection.estimation
    if (cd == EstimationType.ESTIMATE):
        dmcidx += 1
    if (cr == EstimationType.ESTIMATE):
        dmcidx += 1

    parnames = []
    if (cd == EstimationType.ESTIMATE or (cd == EstimationType.CONSIDER and cr == EstimationType.CONSIDER)):
        parnames.extend([r"$C_D$", r"$C_R$"])
    else:
        parnames.extend([r"$C_R$", r"$C_D$"])

    cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    idx, patches, cmap = 0, [], {None: cycle[0]}
    for sk, sv in cfg.stations.items():
        if (sk not in cmap):
            cmap[sk] = cycle[idx]
            patches.append(patch.Patch(color=cycle[idx], label=sk))
            idx = (idx + 1)%len(cycle)
        if (sv.bias_estimation in [EstimationType.ESTIMATE, EstimationType.CONSIDER]):
            for m in key:
                parnames.append(f"{sk}-{meas_names[m]}")

    tstamp, prefit, posfit, inocov, params, estmacc, estmcov, colors = [], [], [], [], [], [], [], []
    for i, o in zip(inp, out):
        tstamp.append(i.time)
        colors.append(cmap[o.station if len(o.station) else None])
        prefit.append([ix - ox for ix, ox in zip(i.values, o.pre_fit)])
        posfit.append([ix - ox for ix, ox in zip(i.values, o.post_fit)])

        p = []
        for m in range(len(o.innovation_covariance)):
            if (m in [0, 2, 5, 9, 14, 20]):
                p.append(3.0*numpy.sqrt(o.innovation_covariance[m]))
        if (len(p) > 0):
            inocov.append(p)
        else:
            inocov.append([0.0]*len(prefit[0]))

        if (estim_param and len(o.estimated_state) > 6):
            if (dmcrun):
                params.append(o.estimated_state[6:dmcidx] + o.estimated_state[dmcidx+3:])
                estmacc.append(get_lvlh_rotation(o.estimated_state).dot(o.estimated_state[dmcidx:dmcidx+3]))
            else:
                params.append(o.estimated_state[6:])

    pre = numpy.array(prefit)
    pos = numpy.array(posfit)
    cov = numpy.array(inocov)
    if (estim_param):
        par = numpy.array(params)
        estmacc = numpy.array(estmacc)

    if (len(tstamp) > 0):
        start = tstamp[0] if (tstamp[0] < tstamp[-1]) else tstamp[-1]
        tim = [(t - start)/3600 for t in tstamp]
    else:
        tim = []

    angles = [MeasurementType.AZIMUTH, MeasurementType.ELEVATION, MeasurementType.RIGHT_ASCENSION, MeasurementType.DECLINATION]
    if (MeasurementType.POSITION in key):
        order = [1, 2, 3]
        units = ["m", "m", "m"]
        ylabs = [r"$\Delta x$", r"$\Delta y$", r"$\Delta z$"]
    elif (MeasurementType.POSITION_VELOCITY in key):
        order = [1, 3, 5, 2, 4, 6]
        units = ["m", "m", "m", "m/s", "m/s", "m/s"]
        ylabs = [r"$\Delta x$", r"$\Delta y$", r"$\Delta z$", r"$\Delta v_x$", r"$\Delta v_y$", r"$\Delta v_z$"]
    else:
        ylabs = [meas_names[k] for k in key]
        if (key[0] in angles and key[1] in angles):
            pre /= Constant.ARC_SECOND_TO_RAD
            pos /= Constant.ARC_SECOND_TO_RAD
            cov /= Constant.ARC_SECOND_TO_RAD
            units = ["arcsec", "arcsec"]
        else:
            units = ["m", "m/s"] if (key[0] == MeasurementType.RANGE) else ["m/s"]

    outfiles = []
    plt.figure(0)
    plt.suptitle("Pre-Fit Residuals")
    for i in range(pre.shape[-1]):
        if (MeasurementType.POSITION in key):
            plt.subplot(3, 1, order[i])
        elif (MeasurementType.POSITION_VELOCITY in key):
            plt.subplot(3, 2, order[i])
        else:
            plt.subplot(pre.shape[-1], 1, i + 1)
        plt.scatter(tim, pre[:,i], color=colors, marker="o", s=7)
        plt.legend(handles=patches, loc="best")
        plt.xlabel("Time [hr]")
        plt.ylabel(f"{ylabs[i]} [{units[i]}]")
        plt.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    if (output_file_path):
        outfiles.append(output_file_path + "_prefit.png")
        plt.savefig(outfiles[-1], format="png")

    plt.figure(1)
    plt.suptitle("Post-Fit Residuals")
    for i in range(pre.shape[-1]):
        if (MeasurementType.POSITION in key):
            plt.subplot(3, 1, order[i])
        elif (MeasurementType.POSITION_VELOCITY in key):
            plt.subplot(3, 2, order[i])
        else:
            plt.subplot(pre.shape[-1], 1, i + 1)
        plt.scatter(tim, pos[:,i], color=colors, marker="o", s=7)
        plt.legend(handles=patches, loc="best")
        plt.plot(tim, -cov[:,i], "-r")
        plt.plot(tim,  cov[:,i], "-r")
        plt.xlabel("Time [hr]")
        plt.ylabel(f"{ylabs[i]} [{units[i]}]")
        plt.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    if (output_file_path):
        outfiles.append(output_file_path + "_postfit.png")
        plt.savefig(outfiles[-1], format="png")

    if (estim_param):
        for i in range(par.shape[-1]):
            if (i == 0):
                plt.figure(2)
                plt.suptitle("Estimated Parameters")
            plt.subplot(par.shape[1], 1, i + 1)
            plt.scatter(tim, par[:,i], marker="o", s=7)
            plt.xlabel("Time [hr]")
            plt.ylabel(parnames[i])
            plt.grid(True)

        plt.tight_layout(rect = [0, 0.03, 1, 0.95])
        if (output_file_path):
            outfiles.append(output_file_path + "_estpar.png")
            plt.savefig(outfiles[-1], format="png")

        if (dmcrun):
            lab = [r"Radial [$\frac{m}{s^2}$]", r"In-Track [$\frac{m}{s^2}$]", r"Cross-Track [$\frac{m}{s^2}$]"]
            plt.figure(3)
            plt.suptitle("Estimated DMC Accelerations")
            for i in range(3):
                plt.subplot(3, 1, i+1)
                if (len(estmacc) > 0):
                    plt.plot(tim, estmacc[:,i])
                plt.xlabel("Time [hr]")
                plt.ylabel(lab[i])
                plt.grid(True)

            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            if (output_file_path):
                outfiles.append(output_file_path + "_estacc.png")
                plt.savefig(outfiles[-1], format="png")

    if (interactive):
        plt.show()
    plt.close("all")
    return(outfiles)

if (__name__ != '__main__'):
    __pdoc__ = {m: False for m in ("Settings", )}
