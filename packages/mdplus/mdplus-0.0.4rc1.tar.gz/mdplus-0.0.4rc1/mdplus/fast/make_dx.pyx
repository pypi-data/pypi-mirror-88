def make_dx(float [:,:] x, float [:] dd, long [:, :] ij):
    """
    Calculate the coordinate shift vector DX.

    Arguments:
        x: [N,3] numpy array of current coordinates.
        dd: [K] numpy array of bond length gradients
        ij: [K, 2] numpy array indexing atom pairs for each bond in dd
    Returns:
        [N, 3] numpy array of shifts (will be further processed in calling
        python function)
    """
    import numpy as np
    
    cdef Py_ssize_t n = x.shape[0]
    cdef Py_ssize_t nk = ij.shape[0]
    cdef Py_ssize_t i, j, k, l
    
    DX = np.zeros((n, 3), dtype = np.float32)
    cdef float [:, :] DX_view = DX
    cdef float dx
    
    for k in range(nk):
        i = ij[k, 0]
        j = ij[k, 1]
        for l in range(3):
            dx = x[j, l] - x[i, l]
            dx = dx * dd[k]
            DX_view[j, l] += dx
            DX_view[i, l] -= dx
    return DX
