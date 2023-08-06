'''Try to evaluate some line integrals.'''

import numpy as np
import matplotlib.pyplot as plt
# from skimage.feature import canny
# from scipy.integrate import quad
# from tqdm import tqdm

if __name__ == '__main__':

    fft = lambda x0: np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(
        x0)))
    ifft = lambda x0: np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(
        x0)))

    a, b = 1, 2
    N = 75
    X, Y = np.meshgrid(
        np.linspace(-3, 3, N),
        np.linspace(-3, 3, N))
    Z = X**2/a**2 + Y**2/b**2 <= 1
    # Z = canny(Z)
    FZ = fft(Z)

    # Try line integral
    npcs = 500
    t = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    x = a*np.cos(t)
    y = b*np.sin(t)

    def f(t, a, b, u, v):
        return np.exp(
            -1j*(u*a*np.cos(t) + v*b*np.sin(t)))*np.sqrt(
                a**2*np.sin(t)**2 + b**2*np.cos(t)**2)
    def fr(t, a, b, u, v):
        return np.real(f(t, a, b, u, v))
    def fi(t, a, b, u, v):
        return np.imag(f(t, a, b, u, v))

    u = X[..., None]*2*np.pi
    v = Y[..., None]*2*np.pi
    t = t[None, None, :]
    lFZ = np.sum(np.exp(-1j*(u*a*np.cos(t) + v*b*np.sin(t)))*np.sqrt(a**2*np.sin(t)**2 + b**2*np.cos(t)**2), axis=-1)

    # lFZ = np.zeros((N, N), dtype=FZ.dtype)
    # for idx in tqdm(np.ndindex((N, N)), total=N**2, leave=False):
    #     ii, jj = idx[:]
    #     re = quad(fr, 0, 2*np.pi, args=(
    #         a, b, X[ii, jj]*2*np.pi, Y[ii, jj]*2*np.pi))
    #     im = quad(fi, 0, 2*np.pi, args=(
    #         a, b, X[ii, jj]*2*np.pi, Y[ii, jj]*2*np.pi))
    #     lFZ[ii, jj] = re[0] + 1j*im[0]
    #
    plt.subplot(1, 2, 1)
    plt.imshow(np.abs(FZ))
    plt.subplot(1, 2, 2)
    plt.imshow(np.abs(lFZ))
    plt.show()

    plt.subplot(1, 2, 1)
    plt.imshow(Z)
    plt.subplot(1, 2, 2)
    plt.imshow(np.abs(ifft(lFZ)))
    plt.show()
