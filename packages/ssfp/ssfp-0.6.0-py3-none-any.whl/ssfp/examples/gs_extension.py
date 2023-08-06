'''Extend PLANET recon across harmonics.

Notes
-----
This may be possible due to the fact that spectra/ellipses are very
similar between harmonics (not the same, but might be close enough).

This does not work very well...
'''

import numpy as np
import matplotlib.pyplot as plt
from phantominator import shepp_logan
from tqdm import tqdm

from ssfp import bssfp, planet

if __name__ == '__main__':

    N, npcs = 128, 16
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    M0, T1, T2 = shepp_logan((N, N, 1), MR=True, zlims=(-.25, .25))
    M0, T1, T2 = np.squeeze(M0), np.squeeze(T1), np.squeeze(T2)

    # Linear off resonance
    TR0 = 3e-3
    TR1 = 6e-3
    alpha = np.deg2rad(60)
    TRmax = np.maximum(TR0, TR1)
    TRmin = np.minimum(TR0, TR1)
    df, _ = np.meshgrid(
        np.linspace(-1/TRmax, 1/TRmax, N),
        np.linspace(-1/TRmax, 1/TRmax, N))

    # Simulate acquisition
    data = np.empty((N, N, npcs), dtype=np.complex64)

    data0 = bssfp(
        T1, T2, TR=TR0, alpha=alpha, field_map=df,
        phase_cyc=pcs[0::2], M0=M0, delta_cs=0, phi_rf=0, phi_edd=0,
        phi_drift=0)
    data0 = np.moveaxis(data0, 0, -1)
    data[..., 0::2] = data0

    data1 = bssfp(
        T1, T2, TR=TR1, alpha=alpha, field_map=df,
        phase_cyc=pcs[1::2], M0=M0, delta_cs=0, phi_rf=0, phi_edd=0,
        phi_drift=0)
    data1 = np.moveaxis(data1, 0, -1)
    data[..., 1::2] = data1

    Meff = np.zeros(M0.shape, dtype=np.complex64)
    T1est = np.zeros(T1.shape, dtype=np.complex64)
    T2est = np.zeros(T2.shape, dtype=np.complex64)
    mask = M0 > 0
    for idx in tqdm(
            np.argwhere(mask),
            total=np.sum(mask.flatten()),
            leave=False):
        try:
            Meff[tuple(idx)], T1est[tuple(idx)], T2est[tuple(idx)] = planet(
                data[tuple(idx) + (slice(None),)], alpha, TRmin,
                T1[tuple(idx)])
        except AssertionError:
            pass

    plt.imshow(np.abs(T2est))
    plt.show()



    # # Try recon
    # res = gs_recon(data, pc_axis=-1)

    # plt.imshow(np.abs(res))
    # plt.show()
