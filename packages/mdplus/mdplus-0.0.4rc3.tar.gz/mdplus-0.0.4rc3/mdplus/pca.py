# pca.py - PCA routines for MD trajectory data.

import mdtraj as mdt
from mdplus.utils import Procrustes, check_dimensions
from sklearn.decomposition import PCA as skPCA
import numpy as np

class PCA(object):
    """
    PCA for MD trajectory data, with an API like scikit-learn PCA

    With a [n_frames, n_atoms, 3] array of coordinates:

        pca = PCA()
        pca.fit(X)
        scores = pca.transform(X)

    Attributes:
        n_atoms: int, number of atoms
        n_components: int, number of PCA components
        mean: [n_atoms, 3] array, mean structure
        eigenvalues: [n_components] array
        
    """
    def __init__(self, n_components=None):
        self.n_components = n_components
        self._pca = skPCA(n_components=self.n_components)

    def fit(self, traj):
        """
        Build the PCA model.

        Args:
            traj: [n_frames, n_atoms, 3] numpy array of coordinates.
        """
        traj = check_dimensions(traj)
        n_frames = traj.shape[0]
        self.n_atoms = traj.shape[1]

        if self.n_components is not None:
            if self.n_components > 1 and self.n_components > min(n_frames, 3 * self.n_atoms):
                raise ValueError('Error: cannot find {} principal components from a trajectory of {} frames of {} atoms'.format(self.n_components, n_frames, self.n_atoms))
          
        self._fitter = Procrustes()
        fitted_traj = self._fitter.fit_transform(traj)
        self._pca.fit(fitted_traj.reshape((n_frames, -1)))
        self.n_components = self._pca.n_components_
        self.eigenvalues = self._pca.explained_variance_
        self.mean = self._pca.mean_.reshape((self.n_atoms, 3))

    def transform(self, traj):
        """
        Transform the trajectory frames into the PCA space.

        Args:
            traj: [n_frames, n_atoms, 3] numpy array of coordinates.

        Returns:
            An [n_frames, n_components)
        """
        traj = check_dimensions(traj)
        n_atoms = traj.shape[1]
        if n_atoms != self.n_atoms:
            raise ValueError('Error: trajectory has {} atoms but the model requires {}'.format(n_atoms, self.n_atoms))
        traj = self._fitter.transform(traj)
        n_frames = traj.shape[0]
        return self._pca.transform(traj.reshape((n_frames, -1)))

    def inverse_transform(self, traj):
        """
        Transform frames back from PCA space to Cartesian space

        Args:
            traj: an [n_components] or [n_frames, n_components] array

        Returns:
            an [n_frames, n_atoms, 3] array
        """
        traj = np.array(traj)
        if len(traj.shape) > 2 or traj.shape[-1] != self.n_components:
            raise ValueError('Error: traj must be a vector of length {} or an array of shape [any,{}]'.format(self.n_components, self.n_components))
        if len(traj.shape) == 1:
            traj = traj.reshape((1, -1) )
        n_frames = len(traj)
        crds = self._pca.inverse_transform(traj)
        return crds.reshape((n_frames, self.n_atoms, 3))
        
    def fit_transform(self, traj):
        """
        Fit the PCA model and return the transformed data

        Args:
            traj: [n_frames, n_atoms, 3] numpy array of coordinates.

        Returns:
            An [n_frames, n_components] array
        """
        traj = check_dimensions(traj)
        self.fit(traj)
        return self.transform(traj)
        
