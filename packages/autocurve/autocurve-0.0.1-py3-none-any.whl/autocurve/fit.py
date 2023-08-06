import imageio
import numpy as np
import matplotlib.pyplot as plt


def read(fpath):
    """ Read image

    Parameters
    ----------
    fpath: path-like object
        Path to file

    Returns
    -------
    np.array
        Image in numpy array form

    """
    f = imageio.imread(fpath)
    f = np.array(f)
    return f


def parameterize(f):
    """ Parameterize

    """
    # CONTRAST
    f = (f > np.median(f.flatten())) * 1

    # GET VALUES
    XY = np.dstack(np.where(f.T == 1))
    X, Y = XY.T[0][:, 0], XY.T[1][:, 0]

    # ONE VALUE PER X
    f = np.bincount(X, Y) / np.bincount(X, np.ones(len(X)))

    return f


def plot(f):
    """ Plot

    """
    plt.plot(f)
    plt.show()


def pipe(fpath):
    f = read(fpath)
    f = parameterize(f)
    plot(f)
