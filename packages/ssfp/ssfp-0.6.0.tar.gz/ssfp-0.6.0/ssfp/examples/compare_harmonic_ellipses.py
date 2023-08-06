'''Look at ellipses of different harmonics.'''

import numpy as np
import matplotlib.pyplot as plt
from ssfp import bssfp

if __name__ == '__main__':

    npcs = 16
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=True)

    T1, T2, M0 = 1.2, .5, 1
    alpha = np.deg2rad(30)
    TR = 3e-3

    df0 = 3/(2*TR)
    sig0 = bssfp(T1, T2, TR, alpha, field_map=0, phase_cyc=pcs, M0=M0)
    sig1 = bssfp(
        T1, T2, TR, alpha, field_map=df0, phase_cyc=pcs, M0=M0)

    sig0 /= np.linalg.norm(sig0)
    sig1 /= np.linalg.norm(sig1)

    plt.hist([
        np.concatenate((sig0.real, sig0.imag)),
        np.concatenate((sig1.real, sig1.imag))])
    plt.show()
    # plt.hist([sig0.real, sig1.real])
    # plt.show()
    # plt.hist([sig0.imag, sig1.imag])
    # plt.show()

    df = np.linspace(-1/TR, 1/TR, npcs)
    plt.plot(df, np.abs(sig0))
    plt.plot(df, np.roll(np.abs(sig1), 250))
    plt.show()

    plt.plot(sig0.real, sig0.imag)
    plt.plot(sig1.real, sig1.imag)
    plt.axis('square')
    plt.show()

    # Notes:
    #     - Histogram of harmonics should be the same
    #     - ellipses of harmonics appear to be only slightly different
