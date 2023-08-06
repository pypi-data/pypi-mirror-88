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


GWlatex_labels = {
    "luminosity_distance": r"$d_{L} [Mpc]$",
    "geocent_time": r"$t_{c} [s]$",
    "dec": r"$\delta [rad]$",
    "ra": r"$\alpha [rad]$",
    "a_1": r"$a_{1}$",
    "a_2": r"$a_{2}$",
    "phi_jl": r"$\phi_{JL} [rad]$",
    "phase": r"$\phi [rad]$",
    "psi": r"$\Psi [rad]$",
    "iota": r"$\iota [rad]$",
    "tilt_1": r"$\theta_{1} [rad]$",
    "tilt_2": r"$\theta_{2} [rad]$",
    "phi_12": r"$\phi_{12} [rad]$",
    "mass_2": r"$m_{2} [M_{\odot}]$",
    "mass_1": r"$m_{1} [M_{\odot}]$",
    "total_mass": r"$M [M_{\odot}]$",
    "chirp_mass": r"$\mathcal{M} [M_{\odot}]$",
    "H1_matched_filter_snr": r"$\rho^{H}_{mf}$",
    "L1_matched_filter_snr": r"$\rho^{L}_{mf}$",
    "network_matched_filter_snr": r"$\rho^{N}_{mf}$",
    "H1_optimal_snr": r"$\rho^{H}_{opt}$",
    "L1_optimal_snr": r"$\rho^{L}_{opt}$",
    "V1_optimal_snr": r"$\rho^{V}_{opt}$",
    "E1_optimal_snr": r"$\rho^{E}_{opt}$",
    "network_optimal_snr": r"$\rho^{N}_{opt}$",
    "H1_matched_filter_snr_abs": r"$\mathrm{abs}(\rho^{H}_{mf})$",
    "L1_matched_filter_snr_abs": r"$\mathrm{abs}(\rho^{L}_{mf})$",
    "V1_matched_filter_snr_abs": r"$\mathrm{abs}(\rho^{V}_{mf})$",
    "E1_matched_filter_snr_abs": r"$\mathrm{abs}(\rho^{E}_{mf})$",
    "H1_matched_filter_snr_angle": r"$\mathrm{arg}(\rho^{H}_{mf})$",
    "L1_matched_filter_snr_angle": r"$\mathrm{arg}(\rho^{L}_{mf})$",
    "V1_matched_filter_snr_angle": r"$\mathrm{arg}(\rho^{V}_{mf})$",
    "E1_matched_filter_snr_angle": r"$\mathrm{arg}(\rho^{E}_{mf})$",
    "H1_time": r"$t_{H} [s]$",
    "L1_time": r"$t_{L} [s]$",
    "V1_time": r"$t_{V} [s]$",
    "E1_time": r"$t_{E} [s]$",
    "spin_1x": r"$S_{1x}$",
    "spin_1y": r"$S_{1y}$",
    "spin_1z": r"$S_{1z}$",
    "spin_1z_evolved": r"$S_{1z}^{evol}$",
    "spin_2x": r"$S_{2x}$",
    "spin_2y": r"$S_{2y}$",
    "spin_2z": r"$S_{2z}$",
    "spin_2z_evolved": r"$S_{2z}^{evol}$",
    "chi_p": r"$\chi_{p}$",
    "chi_eff": r"$\chi_{eff}$",
    "mass_ratio": r"$q$",
    "symmetric_mass_ratio": r"$\eta$",
    "inverted_mass_ratio": r"$1/q$",
    "phi_1": r"$\phi_{1} [rad]$",
    "phi_2": r"$\phi_{2} [rad]$",
    "cos_tilt_1": r"$\cos{\theta_{1}}$",
    "cos_tilt_2": r"$\cos{\theta_{2}}$",
    "redshift": r"$z$",
    "comoving_distance": r"$d_{com} [Mpc]$",
    "mass_1_source": r"$m_{1}^{source} [M_{\odot}]$",
    "mass_2_source": r"$m_{2}^{source} [M_{\odot}]$",
    "chirp_mass_source": r"$\mathcal{M}^{source} [M_{\odot}]$",
    "total_mass_source": r"$M^{source} [M_{\odot}]$",
    "cos_iota": r"$\cos{\iota}$",
    "theta_jn": r"$\theta_{JN} [rad]$",
    "cos_theta_jn": r"$\cos{\theta_{JN}}$",
    "lambda_1": r"$\lambda_{1}$",
    "lambda_2": r"$\lambda_{2}$",
    "lambda_tilde": r"$\tilde{\lambda}$",
    "delta_lambda": r"$\delta\lambda$",
    "peak_luminosity": (
        r"$L_{\mathrm{peak}} [10^{56} \mathrm{ergs\;s^{-1}}]$"
    ),
    "peak_luminosity_non_evolved": (
        r"$L_{\mathrm{peak}}^{\mathrm{nonevol}} [10^{56} "
        "\mathrm{ergs\;s^{-1}}]$"
    ),
    "final_mass": r"$M_{\mathrm{final}} [M_{\odot}]$",
    "final_mass_non_evolved": (
        r"$M_{\mathrm{final}}^{\mathrm{nonevol}} [M_{\odot}]$"
    ),
    "final_mass_source": r"$M_{\mathrm{final}}^{\mathrm{source}} [M_{\odot}]$",
    "final_mass_source_non_evolved": (
        r"$M_{final}^{\mathrm{source, nonevol}} [M_{\odot}]$"
    ),
    "final_spin": r"$a_{\mathrm{final}}$",
    "final_spin_non_evolved": r"$a_{\mathrm{final}}^{\mathrm{nonevol}}$",
    "radiated_energy": r"$E_{\mathrm{rad}} [M_{\odot}]$",
    "radiated_energy_non_evolved": (
        r"$E_{\mathrm{rad}}^{\mathrm{nonevol}} [M_{\odot}]$"
    ),
    "final_kick": r"$v_{\mathrm{final}} [\mathrm{km\;s^{-1}}]$",
    "log_pressure": r"$\log{\mathcal{P}}$",
    "gamma_1": r"$\Gamma_{1}$",
    "gamma_2": r"$\Gamma_{2}$",
    "gamma_3": r"$\Gamma_{3}$",
    "spectral_decomposition_gamma_0": r"$\gamma_{0}$",
    "spectral_decomposition_gamma_1": r"$\gamma_{1}$",
    "spectral_decomposition_gamma_2": r"$\gamma_{2}$",
    "spectral_decomposition_gamma_3": r"$\gamma_{3}$",
    "tidal_disruption_frequency": r"$f_{\mathrm{td}} [\mathrm{Hz}]$",
    "tidal_disruption_frequency_ratio": r"$f_{\mathrm{td}} / f_{220}$",
    "220_quasinormal_mode_frequency": r"$f_{220} [\mathrm{Hz}]$",
    "baryonic_torus_mass": r"$M_{\mathrm{torus}} [M_{\odot}]$",
    "baryonic_torus_mass_source": r"$M^{\mathrm{source}}_{\mathrm{torus}} [M_{\odot}]$",
    "compactness_1": r"$C_{1}$",
    "compactness_2": r"$C_{2}$",
    "baryonic_mass_1": r"$m_{1, \mathrm{baryonic}} [M_{\odot}]$",
    "baryonic_mass_1_source": r"$m^{\mathrm{source}}_{1, \mathrm{baryonic}} [M_{\odot}]$",
    "baryonic_mass_2": r"$m_{2, \mathrm{baryonic}} [M_{\odot}]$",
    "baryonic_mass_2_source": r"$m^{\mathrm{source}}_{2, \mathrm{baryonic}} [M_{\odot}]$"
}

public_GWlatex_labels = {"mass_1": r"$m_{1}^{det} [M_{\odot}]$",
                         "mass_2": r"$m_{2}^{det} [M_{\odot}]$",
                         "mass_1_source": r"$m_{1} [M_{\odot}]$",
                         "mass_2_source": r"$m_{2} [M_{\odot}]$"
                         }
