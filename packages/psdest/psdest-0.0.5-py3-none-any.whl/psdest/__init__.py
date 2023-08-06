import numpy as np

from .pypsder import PyPSDer

try:
    from .cpsder import CPSDer
except ModuleNotFoundError:
    CPSDer = None


def PSDer(
        Nft=None, 
        rbw=None, 
        rate=1., 
        window='hann', 
        step=0.5, 
        threads=1,
        dtype=np.float64):

    # automatically select PSDer
    if np.dtype(dtype).char in np.typecodes['Complex'] or CPSDer is None:
        return PyPSDer(Nft=Nft, rbw=rbw, rate=rate, window=window, step=step, threads=threads, dtype=dtype)
    else:
        return CPSDer(Nft=Nft, rbw=rbw, rate=rate, window=window, step=step, threads=threads, dtype=dtype)


