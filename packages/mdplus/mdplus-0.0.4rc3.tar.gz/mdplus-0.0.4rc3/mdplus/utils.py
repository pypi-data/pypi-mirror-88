# utils.py 
import mdtraj as mdt
import numpy as np

def rmsd(traj, xref):
    """
    Calculate rmsd between coordinates in traj and xref)

    Args:
        traj: [n_atoms, 3] or [n_frames_n_atoms, 3] array
        xref: [n_atoms, 3] or [n_frames_n_atoms, 3] array

    Returns:
        float or vector or array depending on dhapes of traj and xref
    """
    traj = check_dimensions(traj)
    xref = check_dimensions(xref)
    t_traj = mdt.Trajectory(traj, None)
    t_ref = mdt.Trajectory(xref, None)
    rmsd = np.zeros((len(t_traj), len(t_ref)))
    for i, r in enumerate(t_ref):
        rmsd[:, i] = mdt.rmsd(t_traj, r)
    if rmsd.shape[1] == 1:
        rmsd = rmsd.flatten()
    if len(rmsd) == 1:
        rmsd = rmsd[0]
    return rmsd

def fit(traj, xref):
    """
    Least squares fit a trajectory to a reference structure

    Args:
        traj: [n_atoms, 3] or [n_frames_n_atoms, 3] array
        xref: [n_atoms, 3] or [n_frames_n_atoms, 3] array. if the latter,
              the first coordinate set is used for the fit.

    Returns:
        [n_frames, n_atoms, 3] array of fitted coordinates.f
    """
    traj = check_dimensions(traj)
    xref = check_dimensions(xref)
    t_traj = mdt.Trajectory(traj, None)
    t_ref = mdt.Trajectory(xref, None)
    t_traj.superpose(t_ref)
    return t_traj.xyz
    
def check_dimensions(traj):
    """
    Check and regularize a trajectory array
    """
    if not isinstance(traj, np.ndarray):
        traj = np.array(traj)
    if len(traj.shape) < 2 or len(traj.shape) > 3 or traj.shape[-1] != 3:
        raise ValueError('Error: traj must be an [n_atoms, 3] or [n_frames, n_atoms, 3] array')
    if len(traj.shape) == 2:
        traj = traj.reshape((1, -1, 3))
    return traj

class Procrustes(object):

    def __init__(self, max_its=10, drmsd=0.01):
        """
        Initialise a procrustes least-squares fitter.

        Args:
            max_its: int, maximum number of iterations
            drmsd: float, target rmsd between successive means for convergence
        """
        self.max_its = max_its
        self.drmsd = drmsd

    def fit(self, X):
        """
        Train the fitter.

        Args:
            X: [n_frames, n_atoms, 3] numpy array
        """
        X = check_dimensions(X)
        x_mean = X[0]
        t = mdt.Trajectory(X, None)
        t_oldmean = mdt.Trajectory(x_mean, None)
        t_newmean = mdt.Trajectory(x_mean, None)
        err = self.drmsd + 1.0
        it = 0
        while err > self.drmsd and it < self.max_its:
            it += 1
            t.superpose(t_oldmean)
            t_newmean.xyz = t.xyz.mean(axis=0)
            err = mdt.rmsd(t_oldmean, t_newmean)[0]
            t_oldmean.xyz = t_newmean.xyz

        self.converged = err <= self.drmsd
        self.mean = t_oldmean.xyz
            
    def transform(self, X):
        """
        Least-squares fit the coordinates in X.

        Args:
            X: [n_frames, n_atoms, 3] numpy array
        Returns:
            [n_frames, n_atoms, 3] numpy array of fitted coordinates
        """
        X = check_dimensions(X)
        return fit(X, self.mean)
    
    def fit_transform(self, X):
        """
        Train the fitter, and apply to X.

        Args:
            X: [n_frames, n_atoms, 3] numpy array
        Returns:
            [n_frames, n_atoms, 3] numpy array of fitted coordinates
        """
        self.fit(X)
        return self.transform(X)
