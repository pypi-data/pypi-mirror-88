'''
Copyright (c) 2020, Diego E. Kleiman
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
'''

import numpy as np
import pandas as pd
import os
from MDAnalysis import Universe
from MDAnalysis.coordinates.DCD import DCDWriter
from suggest_utils import compute_distances, position_to_index
from overlap_utils import overlap_dye, overlap_pair, position_variance, direction_variance
from compute_utils import compute, define_dipole_sel

# TODO:
# 	Short term:
# 		1. Add dye displacement information to know about dye movement [DONE]
# 		2. Add rotation autocorrelation constant [CANCELLED]
# 		3. Add ability to test only one dye [DONE]
# 		4. Make Python interface more flexible
# 		5. Make CLI more interactive
#		6. Implement suggest for Python interface [DONE]
# 	Long term:
# 		1. Implement energy assessment for frame weighing [CANCELLED]
# 		2. Implement web server features (Django) [DONE]



class FRETraj:
	'''The FRETraj class is the core interface of the FRETraj package.

	A FRETraj object must be instantiated by providing three MDAnalysis.Universe objects.
	The first one corresponds to the reference macromolecule or system which will be labeled 
	with fluorescent dyes. The second and third Universe instances correspond to the donor and 
	acceptor dyes respectively. The trajectories should be preloaded in the Universe instances.

	Example:
		>>> ref = MDAnalysis.Universe("ref_structure.pdb", "ref_traj.dcd") #ref_traj.dcd optional
		>>> donor = MDAnalysis.Universe("CY3.pdb", "CY3.dcd")
		>>> acceptor = MDAnalysis.Universe("CY5.pdb", "CY5.dcd")
		>>> system = FRETraj(ref=ref, donor=donor, acceptor=acceptor)

	Attributes:

	Methods:

	'''

	def __init__(self, ref, donor=None, acceptor=None):
		self.ref = ref
		self.donor = donor
		self.acceptor = acceptor

	def _rewind_dyes(self):
		if (self.donor is not None):
			self.donor.trajectory[0]
		if (self.acceptor is not None):
			self.acceptor.trajectory[0]

	def _rewind_all(self):
		self._rewind_dyes()
		self.ref.trajectory[0]

	def _write_trajectory(self, dye_copy, fname, frames, prefix):
		with DCDWriter(prefix + fname + ".dcd", dye_copy.trajectory.n_atoms) as writer:

			for f1 in frames:
				dye_copy.trajectory[f1]
				writer.write(dye_copy)

	# def define_physical_atoms(donor_sel=None, acceptor_sel=None):
	# 	raise NotImplementedError

	# def define_overlap_constrain():
	# 	raise NotImplementedError

	def suggest(self, k=None, min_dist=None, max_dist=None, fixed_res=None, fname=None):
		'''Suggest good residue pairs for dye insertion.

		Using the trajectory file, it computes the average and st. dev. of the inter-residue distance 
		for all residue pairs. The residue pairs are then sorted by descending distance variance and 
		the top k pairs are saved in residues.txt. A maximum and minimum distance constraint can be 
		provided. If a residue is already determined to contain a dye, the `fixed_res` keyword can be
		set to that residue index and suggest will only return residue pairs containing that residue.

		Writes a file `fname` containing residue-pairs with high distance variance.
		'''

		self._rewind_all()

		# Compute distances between CA and/or C5'/C5* (distance between residues) and store them in array
		n_atoms, resnames, distances = compute_distances(self.ref)

		# Compute mean distances and variance
		var = np.std(distances, axis=0)
		mean = np.mean(distances, axis=0)

		# Get sorted indices by variance in descending order
		indices = var.argsort()[::-1]

		# Translate array position to residue indices
		pos2idx = position_to_index(n_atoms)

		# Filter by fixed residue
		if fixed_res is not None:
			filtered_indices = []

			for idx in indices:
				resid1, resid2 = pos2idx[idx]
				if (resid1==fixed_res) or (resid2==fixed_res):
					filtered_indices.append(idx)

			indices = np.asarray(filtered_indices)

		# Filter by minimum distance
		if min_dist is not None:
			filtered_indices = []

			for idx in indices:
				m = mean[idx]
				if m > min_dist:
					filtered_indices.append(idx)

			indices = np.asarray(filtered_indices)

		# Filter by minimum distance
		if max_dist is not None:
			filtered_indices = []

			for idx in indices:
				m = mean[idx]
				if m < max_dist:
					filtered_indices.append(idx)

			indices = np.asarray(filtered_indices)

		# Set k
		if k is None:
			k = len(indices)

		# Write output file

		tmp_list = []

		if fname is not None:
			with open(fname + '.txt', 'w') as output:
				output.write("Suggested pair of residues to insert the FRET dyes (mean ± std. dev.):\n")
				count = 0
				for idx in indices:
					count += 1
					resid1, resid2 = pos2idx[idx]
					resname1, resname2 = resnames[resid1], resnames[resid2]
					m = "{:.2f}".format(mean[idx])
					v = "{:.2f}".format(var[idx])
					output.write("Residues " + str(resid1) + " (" + resname1 + ") and " + str(resid2) + " (" + resname2 + "): ")
					output.write(m + " ± " + v + " Å\n")
					tmp_list.append([resid1, resid2, resname1, resname2, mean[idx], var[idx]])
					if count > k:
						break
		else:
			count = 0
			for idx in indices:
				count += 1
				resid1, resid2 = pos2idx[idx]
				resname1, resname2 = resnames[resid1], resnames[resid2]
				m = "{:.2f}".format(mean[idx])
				v = "{:.2f}".format(var[idx])
				tmp_list.append([resid1, resid2, resname1, resname2, mean[idx], var[idx]])
				if count > k:
					break

		# Save as csv and return pandas DataFrame
		df = pd.DataFrame(tmp_list, columns=['Residue 1 index', 'Residue 2 index', 'Residue 1 name', 'Residue 2 name', 'Mean distance (Å)', 'Std. dev. (Å)'])
		if fname is not None:	
			df.to_csv(fname + '.csv')

		self._rewind_all()
		
		return df

	def overlap_dye(self, dye, resid, dye_traj_fname, ref_frames=None, verbose=False, prefix=""):
		'''Attach a dye to the reference molecule at the selected residue and output relevant information.

		The dye is aligned to the indicated residue and valid frames from the dye trajectory are selected from
		the dye trajectory based on steric clashes. Using the valid frames, the freedom of rotation is quantified
		as the distance variance of the center of mass of the dipole and its direction variance w.r.t. the first
		allowed frame.

		Args:
			dye (str): "donor" or "acceptor".
			resid (int): residue index where dye will be aligned.
			dye_traj_fname (str): the name of the trajectory file that will be saved.

		Optional args:
			ref_frames (iterable): frame indices from reference molecule trajectory to be considered.
				Defaults to all frames provided.
			verbose (bool): print debugging info.
			prefix (str): prefix for files to be stored.

		Returns:
			dict: contains "pos_var" and "dir_var".
				These keys map to arrays containing the position variance and direction variance for each frame
				in ref_frames.

		Raises:
			ValueError: if dye option different from 'donor' or 'acceptor'.
			AssertionError: if ref_frames provided are out of range for ref trajectory frames.
		'''
		self._rewind_all()

		if (ref_frames is None):
			ref_frames = range(self.ref.trajectory.n_frames)

		assert(max(ref_frames) <= self.ref.trajectory.n_frames)

		if (dye == 'donor'):
			dye = self.donor
		elif (dye == 'acceptor'):
			dye = self.acceptor
		else:
			message = "Dye option not understood, enter 'donor' or 'acceptor'."
			raise ValueError(message)

		pos_var = []
		dir_var = []
		total_frames = []
		dipole = define_dipole_sel(dye)
		for frame in ref_frames:
			
			self.ref.trajectory[frame]

			dye_copy = dye.copy()

			allowed_frames = overlap_dye(
				self.ref.copy(), 
				dye_copy, resid, 
				prefix= prefix + "_frame_" + str(frame), 
				verbose=verbose)

			total_frames.append(allowed_frames)
			
			if allowed_frames:
				self._write_trajectory(dye_copy, 
					dye_traj_fname, 
					allowed_frames, 
					prefix + "_frame_" + str(frame) + "_")
				p_var = position_variance(dye_copy, dipole, allowed_frames)
				d_var = direction_variance(dye_copy, dipole, allowed_frames)
				pos_var.append(p_var)
				dir_var.append(d_var)

		pos_var = np.asarray(pos_var)
		dir_var = np.asarray(dir_var)

		self._rewind_all()

		return {
		'pos_var_donor': pos_var, 
		'dir_var_donor': dir_var, 
		'pos_var_acceptor': None, 
		'dir_var_acceptor': None, 
		'frames': total_frames
		}

	def overlap_pair(self, resid_donor, resid_acceptor, donor_traj_fname, acceptor_traj_fname, ref_frames=None, verbose=False, prefix=""):
		'''Attach dyes to the reference molecule at the selected residues and output relevant information.

		The dyes are aligned to the indicated residues and valid frames from the dye trajectories are selected based on 
		steric clashes. Using the valid frames, the freedom of rotation is quantified using the position variance of the 
		center of mass of the dipole and its direction variance.

		Args:
			dye (str): "donor" or "acceptor".
			resid (int): residue index where dye will be aligned.
			dye_traj_fname (str): the name of the trajectory file that will be saved.

		Optional args:
			ref_frames (iterable): frame indices from reference molecule trajectory to be considered.
				Defaults to all frames provided.
			verbose (bool): print debugging info.
			prefix (str): prefix for files to be stored.

		Returns:
				dict: contains keys "pos_var_donor", "dir_var_donor", "pos_var_acceptor", "dir_var_acceptor".
					These keys map to arrays containing the position variance and direction variance for each frame
					in ref_frames.

		Raises:
			AssertionError: if ref_frames provided are out of range for ref trajectory frames.
			AssertionError: if one of the dyes was not provided.
		'''
		self._rewind_all()

		if (ref_frames is None):
			ref_frames = range(self.ref.trajectory.n_frames)

		assert(max(ref_frames) <= self.ref.trajectory.n_frames)

		assert((self.donor is not None) and (self.acceptor is not None))
		
		pos_var_donor, dir_var_donor = [], []
		pos_var_acceptor, dir_var_acceptor = [], []
		total_frames = []
		dipole_donor = define_dipole_sel(self.donor)
		dipole_acceptor = define_dipole_sel(self.acceptor)
		
		for frame in ref_frames:
			
			self.ref.trajectory[frame]

			donor_copy = self.donor.copy()
			acceptor_copy = self.acceptor.copy()

			allowed_frames = overlap_pair(
				self.ref.copy(), 
				donor_copy, 
				acceptor_copy, 
				resid_donor, 
				resid_acceptor, 
				prefix= prefix + "_frame_" + str(frame), 
				verbose=verbose)

			total_frames.append([allowed_frames])
			
			if allowed_frames:
				self._write_trajectory(
					donor_copy, 
					donor_traj_fname, 
					allowed_frames, 
					prefix + "_frame_" + str(frame) + "_")

				self._write_trajectory(
					acceptor_copy, 
					acceptor_traj_fname, 
					allowed_frames, 
					prefix + "_frame_" + str(frame) + "_")
				
				p_var_donor = position_variance(donor_copy, dipole_donor, allowed_frames)
				d_var_donor = direction_variance(donor_copy, dipole_donor, allowed_frames)
				pos_var_donor.append(p_var_donor)
				dir_var_donor.append(d_var_donor)

				p_var_acceptor = position_variance(acceptor_copy, dipole_acceptor, allowed_frames)
				d_var_acceptor = direction_variance(acceptor_copy, dipole_acceptor, allowed_frames)
				pos_var_acceptor.append(p_var_acceptor)
				dir_var_acceptor.append(d_var_acceptor)
		
		self._rewind_all()

		pos_var_donor = np.asarray(pos_var_donor)
		dir_var_donor = np.asarray(dir_var_donor)
		pos_var_acceptor = np.asarray(pos_var_acceptor)
		dir_var_acceptor = np.asarray(dir_var_acceptor)

		return {
		'pos_var_donor': pos_var_donor, 
		'dir_var_donor': dir_var_donor, 
		'pos_var_acceptor': pos_var_acceptor, 
		'dir_var_acceptor': dir_var_acceptor, 
		'frames': total_frames
		}

	def compute_efficiency(self, resid_donor, resid_acceptor, R0, regime='isotropic', burst_averaging_on=False, burst_threshold=30, decay_const=3, ref_frames=None, verbose=False, prefix=""):
		'''Compute FRET efficiency for a given donor-acceptor pair using specific frames from their trajectories.

		Args:
			resid_donor (int): residue index where donor dye will be aligned.
			resid_acceptor (int): residue index where acceptor dye will be aligned.
			R0 (float): Förster radius for the donor-acceptor pair.
			regime (str): averaging regime (one of 'isotropic', 'dynamic', 'static').
				Default 'isotropic'.
			burst_averaging_on (bool): whether to use burst averaging or not.
			burst_threshold (int): minimum number of photons in a burst.
			decay_const (int): exponential decay scale for burst size distribution.
			ref_frames (iterable): frame indices from reference molecule trajectory to be considered.
				Defaults to all frames provided.
			verbose (bool): print debugging info.
			prefix (str): prefix for files to be stored.

		Returns:
			dict: contains keys "dist", "kappa2", "fret", "fret_error".
				dist (np.ndarray): distances between donor and acceptor for each ref frame.
				kappa2 (np.ndarray): kappa squared factor for each ref frame.
				fret (np.ndarray): FRET efficiency for each ref frame.
				fret_error (np.ndarray): standard error for FRET efficiency. 
		'''
		self._rewind_all()
		
		if (ref_frames is None):
			ref_frames = range(self.ref.trajectory.n_frames)

		assert(max(ref_frames) <= self.ref.trajectory.n_frames)

		all_distances, all_kappa2, all_fret, all_error = [], [], [], []
		# dipole_donor = define_dipole_sel(self.donor)

		for frame in ref_frames:
			
			self.ref.trajectory[frame]

			donor_copy = self.donor.copy()
			acceptor_copy = self.acceptor.copy()

			allowed_frames = overlap_pair(
				self.ref.copy(), 
				donor_copy, 
				acceptor_copy, 
				resid_donor, 
				resid_acceptor, 
				prefix= prefix + "_frame_" + str(frame), 
				verbose=verbose)

			if allowed_frames:
				distances, kappa2, fret, error = compute(
					donor_copy, 
					acceptor_copy, 
					R0, 
					allowed_frames, 
					prefix=prefix + "_frame_" + str(frame), 
					regime=regime, 
					burst_averaging_on=burst_averaging_on, 
					burst_threshold=burst_threshold, 
					decay_const=decay_const)
				
				all_distances.extend(list(distances))
				all_kappa2.extend(list(kappa2))
				all_fret.append(fret)
				all_error.append(error)

				if verbose:
					print("Finished processing frame " + str(frame))

		all_distances = np.asarray(all_distances)
		all_kappa2 = np.asarray(all_kappa2)
		all_fret = np.asarray(all_fret)
		all_error = np.asarray(all_error)

		self._rewind_all()

		return {
		'dist': all_distances, 
		'kappa2': all_kappa2, 
		'fret': all_fret, 
		'fret_error': all_error
		}


