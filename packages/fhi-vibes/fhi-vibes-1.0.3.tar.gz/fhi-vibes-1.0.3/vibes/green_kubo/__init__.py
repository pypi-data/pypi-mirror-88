"""ab initio Green-Kubo post processing"""
from collections import namedtuple

import numpy as np
import xarray as xr
from ase import units
from scipy import signal as sl

from vibes import defaults
from vibes import dimensions as dims
from vibes import keys
from vibes.correlation import get_autocorrelationNd
from vibes.fourier import get_fourier_transformed
from vibes.helpers import Timer, talk, warn
from vibes.integrate import get_cumtrapz


_prefix = "GreenKubo"

Timer.prefix = _prefix


def _talk(msg, **kw):
    """wrapper for `utils.talk` with prefix"""
    return talk(msg, prefix=_prefix, **kw)


def gk_prefactor(
    volume: float, temperature: float, fs_factor: float = 1, verbose: bool = False
) -> float:
    """convert eV/AA^2/fs to W/mK

    Args:
        volume (float): volume of the supercell in AA^3
        temperature (float): avg. temp. in K (trajectory.temperatures.mean())
        fs_factor (float): time * fs_factor = time in fs

    Returns:
        V / (k_B * T^2) * 1602
    """
    V = float(volume)
    T = float(temperature)
    prefactor = 1 / units.kB / T ** 2 * 1.602 * V / fs_factor  # / 1000
    msg = [
        f"Compute Prefactor:",
        f".. Volume:        {V:10.2f}  AA^3",
        f".. Temperature:   {T:10.2f}  K",
        f".. factor to fs.: {fs_factor:10.5f}",
        f"-> Prefactor:     {prefactor:10.2f}  W/mK / (eV/AA^/fs)",
    ]
    _talk(msg, verbose=verbose)
    return float(prefactor)


def get_gk_prefactor_from_dataset(dataset: xr.Dataset, verbose: bool = True) -> float:
    """get the GK prefactor for the dataset, wraps `gk_prefactor`"""
    volume = dataset.attrs[keys.volume]
    temperature = dataset[keys.temperature].mean()
    return gk_prefactor(volume=volume, temperature=temperature, verbose=verbose)


def get_hf_data(flux: xr.DataArray, dropna_dim=keys.time) -> namedtuple:
    """Compute heat flux autocorrelation and integrated kappa from heat flux

    Args:
        flux [N_t, 3]: the heat flux in an xr.DataArray
        dropna_dim: drop nan values along this dimension (default: `time`)

    Returns:
        namedtuple: (heat flux autocorrelation function, integrated kappa)

    """
    # dropna
    flux = flux.dropna(dropna_dim)

    # compute the time mean flux of flux <J>
    flux_avg = flux.mean(axis=0)

    # compute heat flux autocorrelation function (HFACF) <J(t)J>
    flux_corr = get_autocorrelationNd(flux - flux_avg, off_diagonal=True, verbose=False)

    # get integrated kappa
    kappa = get_cumtrapz(flux_corr)

    # return namedtuple w/ HFACF and integrated kappa
    cls = namedtuple(
        "gk_raw_data", (keys.heat_flux_autocorrelation, keys.kappa_cumulative)
    )

    return cls(flux_corr, kappa)


def get_lowest_vibrational_frequency(
    velocities: xr.DataArray,
    threshold: float = defaults.filter_threshold,
    freq_key: str = keys.omega,
    verbose: bool = False,
) -> float:
    """get the lowest significant vibrational density from VDOS

    Args:
        velocities [N_t, N_a, 3]: DataArray with atomic velocites
        threshold: fraction of the max. density used to determine lowest significant
        freq_key: name of the frequency axis (default: `omega`)
        verbose: print additional information

    Returns:
        float: the lowest significant vibrational frequency in THz

    """
    # get VDOS (= fourier transform of velocity autocorrelation)
    velocties_corr = get_autocorrelationNd(velocities, verbose=verbose).sum(axis=(1, 2))

    vdos = get_fourier_transformed(velocties_corr, npad=10000, verbose=verbose).real

    # normalize
    vdos /= vdos.max()

    # pick and return the lowest significant frequency
    freq = float(vdos[freq_key][vdos > threshold].min())

    return freq


def get_filtered(
    array: xr.DataArray,
    window_fs: float = None,
    window: int = None,
    antisymmetric: bool = False,
    polyorder: int = 1,
    verbose: bool = True,
) -> xr.DataArray:
    """apply Savitzky-Golay filter to array to remove noise

    See: https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter

    Args:
        array [N_t, ...]: the array to be filtered with time axis in the front
        window_fs: the filter window in fs (we assume array has time axis given in fs)
        window: the filter window in time steps
        antisymmetric: use antisymmetric boundary condition to correctly interpolate t=0
        polyorder: order used for filter (default: 1)
        verbose: be verbose

    Returns:
        xr.DataArray [N_t, ...]: array with filter applied to time axis

    """
    # get the window from time axis:
    if window_fs is not None:
        time = array[keys.time]
        window = len(time[time < window_fs])

    if window is None:
        warn("Either `window_fs` or `window` have to be specified.", level=2)

    # make sure window is odd
    window = window // 2 * 2 + 1

    # if antisymmetric, use f(-t) = -f(t) to extend data
    if antisymmetric:
        data = np.concatenate((-array[::-1], array))
    else:
        data = np.asarray(array)

    # prepare array for the filtered data
    data_filtered = np.zeros_like(data)

    # move time axis to back
    data = np.moveaxis(data, 0, -1)
    data_filtered = np.moveaxis(data_filtered, 0, -1)

    # filter the data
    kw = {"window_length": window, "polyorder": polyorder}
    _talk(f"Apply Savitzky-Golay filter with {kw}", verbose=verbose)
    for ij in np.ndindex(data.shape[:-1]):
        data_filtered[ij] = sl.savgol_filter(data[ij], **kw)

    # move time axis back to front
    data = np.moveaxis(data, -1, 0)
    data_filtered = np.moveaxis(data_filtered, -1, 0)

    # create DataArray with filtered data
    new_array = array.copy()
    if antisymmetric:
        new_array.data = data_filtered[len(array) :]
    else:
        new_array.data = data_filtered

    return new_array


def get_gk_dataset(
    dataset: xr.Dataset,
    window_factor: int = defaults.window_factor,
    filter_threshold: float = defaults.filter_threshold,
    total: bool = False,
    verbose: bool = True,
) -> xr.Dataset:
    """get Green-Kubo data from trajectory dataset

    Args:
        dataset: a dataset containing `heat_flux` and describing attributes
        window_factor: factor for filter width estimated from VDOS (default: 1)
        filter_threshold: threshold for choosing vibr. freq. for filtering (default: 0.1)

    Returns:
        xr.Dataset: the processed data

    Workflow:
        1. get heat flux autocorrelation function (HFACF) and the integrated kappa
        2. get lowest significant vibrational frequency and get its time period
        3. filter integrated kappa with this period
        4. get HFACF by time derivative of this filtered kappa
        5. filter the HFACF with the same filter
        6. estimate cutoff time from the decay of the filtered HFACF

    """
    # 1. get HFACF and integrated kappa
    heat_flux = dataset[keys.heat_flux]

    if total:  # add non-gauge-invariant contribution
        heat_flux += dataset[keys.heat_flux_aux]

    hfacf, kappa = get_hf_data(heat_flux)

    # convert to W/mK
    pref = get_gk_prefactor_from_dataset(dataset, verbose=True)
    hfacf *= pref
    kappa *= pref

    # 2. get lowest significant frequency (from VDOS) in THz
    kw = {"threshold": filter_threshold}
    freq = get_lowest_vibrational_frequency(dataset[keys.velocities], **kw)

    if abs(freq) < 0.001:
        warn(f"Lowest significant vib. freq is {freq} THz, CHECK VDOS!", level=2)

    # window in fs from freq.:
    window_fs = window_factor / freq * 1000

    kw_talk = {"verbose": verbose}
    _talk(f"Estimate filter window size", **kw_talk)
    _talk(f".. lowest vibrational frequency: {freq:.4f} THz", **kw_talk)
    _talk(f".. corresponding window size:    {window_fs:.4f} fs", **kw_talk)
    _talk(f".. window multiplicator used:    {window_factor:.4f} fs", **kw_talk)

    # 3. filter integrated HFACF (kappa) with this window respecting antisymmetry in time
    k_filtered = get_filtered(kappa, window_fs=window_fs, antisymmetric=True)

    # 4. get the respective HFACF by differentiating w.r.t. time and filtering again
    k_gradient = kappa.copy()

    # compute derivative with j = dk/dt = dk/dn * dn/dt = dk/dn / dt
    dt = float(kappa.time[1] - kappa.time[0])
    k_gradient.data = np.gradient(k_filtered, axis=0) / dt

    j_filtered = get_filtered(k_gradient, window_fs=window_fs, verbose=False)

    # 5. get cutoff times from j_filtered and save respective kappas
    ts = np.zeros([3, 3])
    ks = np.zeros([3, 3])

    for (ii, jj) in np.ndindex(3, 3):
        j = j_filtered[:, ii, jj]
        times = j.time[j < 0]
        if len(times) > 1:
            ta = times.min()
        else:
            warn(f"no cutoff time found", level=1)
            ta = 0
        ks[ii, jj] = k_filtered[:, ii, jj].sel(time=ta)
        ts[ii, jj] = ta

    # report
    if verbose:
        k_diag = np.diag(ks)
        _talk(["Cutoff times (fs):", *np.array2string(ts, precision=3).split("\n")])
        _talk(f"Kappa is:       {np.mean(k_diag):.3f} +/- {np.std(k_diag) / 3**.5:.3f}")
        _talk(["Kappa^ab is: ", *np.array2string(ks, precision=3).split("\n")])

    # 6. compile new dataset
    attrs = dataset.attrs.copy()
    attrs.update({"gk_window_fs": window_fs})

    _filtered = "_filtered"
    data = {
        keys.hf_acf: hfacf,
        keys.hf_acf + _filtered: j_filtered,
        keys.kappa_cumulative: kappa,
        keys.kappa_cumulative + _filtered: k_filtered,
        keys.kappa: (dims.tensor, ks),
        keys.time_cutoff: (dims.tensor, ts),
    }

    return xr.Dataset(data, coords=kappa.coords, attrs=attrs)
