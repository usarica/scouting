import numba
import numpy as np

def set_plotting_style():
    from matplotlib import rcParams
    rcParams["font.family"] = "sans-serif"
    rcParams["font.sans-serif"] = ["Helvetica", "Arial", "Liberation Sans", "Bitstream Vera Sans", "DejaVu Sans"]
    rcParams['legend.fontsize'] = 11
    rcParams['legend.labelspacing'] = 0.2
    rcParams['hatch.linewidth'] = 0.5  # https://stackoverflow.com/questions/29549530/how-to-change-the-linewidth-of-hatch-in-matplotlib
    rcParams['axes.xmargin'] = 0.0 # rootlike, no extra padding within x axis
    rcParams['axes.labelsize'] = 'x-large'
    rcParams['axes.formatter.use_mathtext'] = True
    rcParams['legend.framealpha'] = 0.65
    rcParams['axes.labelsize'] = 'x-large'
    rcParams['axes.titlesize'] = 'large'
    rcParams['xtick.labelsize'] = 'large'
    rcParams['ytick.labelsize'] = 'large'
    rcParams['figure.subplot.hspace'] = 0.1
    rcParams['figure.subplot.wspace'] = 0.1
    rcParams['figure.subplot.right'] = 0.96
    rcParams['figure.max_open_warning'] = 0
    rcParams['figure.dpi'] = 100
    rcParams["axes.formatter.limits"] = [-5,4] # scientific notation if log(y) outside this
    
@numba.njit()
def compute_bin_1d_uniform(x, bins, overflow=False):
    n = bins.shape[0] - 1
    b_min = bins[0]
    b_max = bins[-1]
    if overflow:
        if x > b_max: return n-1
        elif x < b_min: return 0
    ibin = int(n * (x - b_min) / (b_max - b_min))
    if x < b_min or x > b_max:
        return -1
    else:
        return ibin
    
@numba.njit()
def numba_histogram(a, bins, weights=None,overflow=False):
    db = np.ediff1d(bins)
    is_uniform_binning = np.all(db-db[0]<1e-6)
    hist = np.zeros((len(bins)-1,), dtype=np.float64)
    a = a.flat
    b_min = bins[0]
    b_max = bins[-1]
    n = bins.shape[0] - 1
    if weights is None:
        weights = np.ones(len(a),dtype=np.float64)
    if is_uniform_binning:
        for i in range(len(a)):
            ibin = compute_bin_1d_uniform(a[i], bins, overflow=overflow)
            if ibin >= 0:
                hist[ibin] += weights[i]
    else:
        ibins = np.searchsorted(bins, a, side='left')
        for i in range(len(a)):
            ibin = ibins[i]
            if overflow:
                if ibin == n+1: ibin = n
                elif ibin == 0: ibin = 1
            if ibin >= 1 and ibin <= n:
                hist[ibin-1] += weights[i]
        pass
    return hist, bins

@numba.njit()
def numba_histogram2d(ax,ay, bins_x, bins_y, weights=None,overflow=False):
    db_x = np.ediff1d(bins_x)
    db_y = np.ediff1d(bins_y)
    is_uniform_binning_x = np.all(db_x-db_x[0]<1e-6)
    is_uniform_binning_y = np.all(db_y-db_y[0]<1e-6)
    hist = np.zeros((len(bins_x)-1,len(bins_y)-1), dtype=np.float64)
    ax = ax.flat
    ay = ay.flat
    b_min_x = bins_x[0]
    b_max_x = bins_x[-1]
    n_x = bins_x.shape[0] - 1
    b_min_y = bins_y[0]
    b_max_y = bins_y[-1]
    n_y = bins_y.shape[0] - 1
    if weights is None:
        weights = np.ones(len(ax),dtype=np.float64)
    if is_uniform_binning_x and is_uniform_binning_y:
        for i in range(len(ax)):
            ibin_x = compute_bin_1d_uniform(ax[i], bins_x, overflow=overflow)
            ibin_y = compute_bin_1d_uniform(ay[i], bins_y, overflow=overflow)
            if ibin_x >= 0 and ibin_y >= 0:
                hist[ibin_x,ibin_y] += weights[i]
    else:
        ibins_x = np.searchsorted(bins_x, ax, side='left')
        ibins_y = np.searchsorted(bins_y, ay, side='left')
        for i in range(len(ax)):
            ibin_x = ibins_x[i]
            ibin_y = ibins_y[i]
            if overflow:
                if ibin_x == n_x+1: ibin_x = n_x
                elif ibin_x == 0: ibin_x = 1
                if ibin_y == n_y+1: ibin_y = n_y
                elif ibin_y == 0: ibin_y = 1
            if ibin_x >= 1 and ibin_y >= 1 and ibin_x <= n_x and ibin_y <= n_y:
                hist[ibin_x-1,ibin_y-1] += weights[i]
    return hist, bins_x, bins_y

def make_profile(tobin,toreduce,edges=None,errors=True):
    from scipy.stats import binned_statistic
    yvals = binned_statistic(tobin,toreduce, 'mean', bins=edges).statistic
    yerr = None
    if errors:
        yerr = binned_statistic(tobin,toreduce, 'std', bins=edges).statistic/binned_statistic(tobin,toreduce, 'count', bins=edges).statistic**0.5
    return yvals, yerr