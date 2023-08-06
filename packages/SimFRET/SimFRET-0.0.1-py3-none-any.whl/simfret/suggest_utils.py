'''
Copyright (c) 2020, Diego E. Kleiman
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
'''

import sys
import argparse
import numpy as np
from MDAnalysis import Universe
from MDAnalysis.analysis.distances import self_distance_array 

def compute_distances(trajectory):
	'''Computes inter-residue distances (using CA or C5' positions for residue positions).

	Args:
		trajectory (MDAnalysis.Universe): Universe instance of molecule.

	Returns:
		tuple: (n_atoms, resnames, distances).
			n_atoms (int): number of atoms (one per residue) in Universe.
			resnames (list[str]): list of residue names.
			distances (np.ndarray): 1-dimensional array with inter-residue distances.
				position_to_index() can be used to map indices in distances array to residues indices.
	'''
	selection = trajectory.select_atoms("name CA or name C5' or (name C5* and not name C5)")
	n_atoms = selection.n_atoms
	resnames = selection.resnames
	n_frames = trajectory.trajectory.n_frames
	distances = np.empty((n_frames, n_atoms*(n_atoms-1)//2), dtype=np.float64)
	dist = np.empty((n_atoms*(n_atoms-1)//2, ), dtype=np.float64)
	for i in range(n_frames-1):
		self_distance_array(selection.positions, result=dist)
		distances[i,:] = dist
		trajectory.trajectory.next()

	return n_atoms, resnames, distances


def position_to_index(n_atoms):
	'''Map (i, j) indices from a 2D array to a 1D index of corresponding flattened array.
	
	Returns a dictionary that maps (i, j) indices from a self-distance matrix to the corresponding index
	of a flat 1D array of size n_atoms*(n_atoms-1)//2. This function is meant to be used with the output 
	of compute_distances().

	Example:
		>>> n_atoms, resnames, distances = compute_distances(traj)
		>>> pos2idx = position_to_index(n_atoms)
		>>> idx = pos2idx[0, 1] # 0 --> first residue, 1 --> second residue
		>>> print("Per-frame distances between first and second residues are:", distances[idx])

	Args:
		n_atoms (int): number of atoms whose pair-wise distances were computed in compute_distances().

	Returns:
		dict: map of 2D indices to 1D index of corresponding flattened array.

	'''
	pos2idx = {}
	k = 0
	for i in range(n_atoms):
	    for j in range(i + 1, n_atoms):
	        pos2idx[k] = (i, j)
	        k += 1
	return pos2idx