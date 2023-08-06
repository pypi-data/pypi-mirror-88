""" Evaluation metrics for randomly generated surrogate maps. """

from .base import Base
from .sampled import Sampled
from ..utils.dataio import dataio
import matplotlib.pyplot as plt
import numpy as np

__all__ = ['base_fit', 'sampled_fit']


def base_fit(x, D, nsurr=100, **params):
    """
    Evaluate variogram fits for Base class.

    Parameters
    ----------
    x : (N,) np.ndarray or filename
        Target brain map
    D : (N,N) np.ndarray or filename
        Pairwise distance matrix between regions in `x`
    nsurr : int, default 100
        Number of simulated surrogate maps from which to compute variograms
    params
        Keyword arguments for :class:`brainsmash.mapgen.base.Base`

    Returns
    -------
    None

    Notes
    -----
    Generates and shows a matplotlib plot instance illustrating the fit of
    the surrogates' variograms to the target map's variogram.

    """

    x = dataio(x)
    d = dataio(D)

    # Instantiate surrogate map generator
    generator = Base(x=x, D=d, **params)

    # Simulate surrogate maps
    surrogate_maps = generator(n=nsurr)

    # Compute empirical variogram
    emp_var, u0 = generator.compute_smooth_variogram(x, return_h=True)

    # Compute surrogate map variograms
    surr_var = np.empty((nsurr, generator.nh))
    for i in range(nsurr):
        surr_var[i] = generator.compute_smooth_variogram(surrogate_maps[i])

    # # Create plot for visual comparison

    # Plot empirical variogram
    fig = plt.figure(figsize=(3, 3))
    ax = fig.add_axes([0.12, 0.15, 0.8, 0.77])
    ax.autoscale(axis='y', tight=True)

    ax.scatter(u0, emp_var, s=20, facecolor='none', edgecolor='k',
               marker='o', lw=1, label='Empirical')

    # Plot surrogate maps' variograms
    mu = surr_var.mean(axis=0)
    sigma = surr_var.std(axis=0)
    ax.fill_between(u0, mu-sigma, mu+sigma, facecolor='#377eb8',
                    edgecolor='none', alpha=0.3)
    ax.plot(u0, mu, color='#377eb8', label='SA-preserving', lw=1)

    # Make plot nice
    leg = ax.legend(loc=0)
    leg.get_frame().set_linewidth(0.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.setp(ax.get_yticklabels(), visible=False)
    plt.setp(ax.get_yticklines(), visible=False)
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_xticklines(), visible=False)
    ax.set_xlabel("Spatial separation\ndistance")
    ax.set_ylabel("Variance")

    plt.show()


def sampled_fit(x, D, index, nsurr=10, **params):
    """
    Evaluate variogram fits for Sampled class.

    Parameters
    ----------
    x : (N,) np.ndarray
        Target brain map
    D : (N,N) np.ndarray or np.memmap
        Pairwise distance matrix between elements of `x`
    index : (N,N) np.ndarray or np.memmap
        See :class:`brainsmash.mapgen.sampled.Sampled`
    nsurr : int, default 10
        Number of simulated surrogate maps from which to compute variograms
    params
        Keyword arguments for :class:`brainsmash.mapgen.sampled.Sampled`

    Returns
    -------
    None

    Notes
    -----
    Generates and shows a matplotlib plot instance illustrating the fit of
    the surrogates' variograms to the target map's variogram.

    """

    # Instantiate surrogate map generator
    generator = Sampled(x=x, D=D, index=index, **params)

    # Simulate surrogate maps
    surrogate_maps = generator(n=nsurr)

    # Compute target & surrogate map variograms
    surr_var = np.empty((nsurr, generator.nh))
    emp_var_samples = np.empty((nsurr, generator.nh))
    u0_samples = np.empty((nsurr, generator.nh))
    for i in range(nsurr):
        idx = generator.sample()  # Randomly sample a subset of brain areas
        v = generator.compute_variogram(generator.x, idx)
        u = generator.D[idx, :]
        umax = np.percentile(u, generator.pv)
        uidx = np.where(u < umax)
        emp_var_i, u0i = generator.smooth_variogram(
            u=u[uidx], v=v[uidx], return_h=True)
        emp_var_samples[i], u0_samples[i] = emp_var_i, u0i
        # Surrogate
        v_null = generator.compute_variogram(surrogate_maps[i], idx)
        surr_var[i] = generator.smooth_variogram(
            u=u[uidx], v=v_null[uidx], return_h=False)

    # # Create plot for visual comparison
    u0 = u0_samples.mean(axis=0)
    emp_var = emp_var_samples.mean(axis=0)

    # Plot target variogram
    fig = plt.figure(figsize=(3, 3))
    ax = fig.add_axes([0.12, 0.15, 0.8, 0.77])
    ax.scatter(u0, emp_var, s=20, facecolor='none', edgecolor='k',
               marker='o', lw=1, label='Empirical')

    # Plot surrogate maps' variograms
    mu = surr_var.mean(axis=0)
    sigma = surr_var.std(axis=0)
    ax.fill_between(u0, mu-sigma, mu+sigma, facecolor='#377eb8',
                    edgecolor='none', alpha=0.3)
    ax.plot(u0, mu, color='#377eb8', label='SA-preserving', lw=1)

    # Make plot nice
    leg = ax.legend(loc=0)
    leg.get_frame().set_linewidth(0.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.setp(ax.get_yticklabels(), visible=False)
    plt.setp(ax.get_yticklines(), visible=False)
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_xticklines(), visible=False)
    ax.set_xlabel("Spatial separation\ndistance")
    ax.set_ylabel("Variance")
    plt.show()
