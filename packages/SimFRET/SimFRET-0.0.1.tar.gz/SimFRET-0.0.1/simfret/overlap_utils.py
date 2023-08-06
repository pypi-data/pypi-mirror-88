'''
Copyright (c) 2020, Diego E. Kleiman
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
'''

import numpy as np
from scipy.spatial.distance import cdist
import MDAnalysis as md
from MDAnalysis import Universe
from MDAnalysis.lib.transformations import rotation_matrix
from MDAnalysis.transformations import translate, center_in_box
from MDAnalysis.transformations.rotate import rotateby as rotate

def alignment_selection(ref, resid, verbose=False):
	'''Return selections for three-atom alignment position according to molecule type (protein, DNA or RNA).

	Args:
		ref (MDAnalysis.Universe): Universe instance of reference molecule.
		resid (int): index of residue where dye will be inserted.
		verbose (bool): confirm where dye will be attached.

	Returns:
		MDAnalysis.Universe: reference molecule (might have added atoms to align dye).
		tuple: three-tuple containing atom selections for the atoms that will be used for dye alignment.

	Raises:
		ValueError: The residue type was not recognized. 
	'''
	root = "resid " + str(resid) + " and"
	resname = set(ref.select_atoms("resid " + str(resid)).resnames)
	
	if verbose:
		print(str(resname) + " residue with index " + str(resid) + " will be used for alignment.")
	
	if (resname == {'DT'}):
		atoms = ["C7", "C5", "N3"]
		return ref, tuple([root + " name " + atom for atom in atoms])

	elif (resname == {'U'}):
		ref = add_C7(ref, resid)
		atoms = ["C7", "C5", "N3"]
		return ref, tuple([root + " name " + atom for atom in atoms])

	elif (resname == {'CYS'}):
		atoms = ["SG", "CB", "CA"]
		return ref, tuple([root + " name " + atom for atom in atoms])

	else:
		message = "The residue type selected, " + str(resname) + "is not currently supported or could not be understood."
		raise ValueError(message)

def add_C7(ref, res):
	'''Modify MDAnalysis.Universe instance ref by adding a C7 atom to U residue with resindex res. 

	This results in changing a U residue into the same structure as DT for dye attachment.
	'''
	C7 = Universe.empty(1, n_residues=1, atom_resindex=[0], trajectory=True)
	C7.add_TopologyAttr('name', ['C7'])
	C7.add_TopologyAttr('type', ['C'])
	C7.add_TopologyAttr('elements', ['C'])
	C7.add_TopologyAttr('resname', ['U'])
	C7.add_TopologyAttr('resid', [res])
	C2, C5 = ref.select_atoms('resid ' + str(res) + ' and (name C2 or name C5)').atoms.positions
	vec = C5 - C2
	vec /= np.linalg.norm(vec)
	pos = C5 + 1.5*vec #1.5 is the normal distance between C7 and C5 in a DT residue
	C7.atoms.positions = np.reshape(pos, (1, 3))
	return md.Merge(ref.atoms, C7.atoms)

def pair_fit(reference, mobile, ref_selection, mob_selection, verbose=False):
	'''Align two molecules based on 3-atom selections (in-place function).
	
	Args:
		reference (MDAnalysis.Universe): Universe instance of reference molecule.
		mobile (MDAnalysis.Universe): Universe instance of molecule that will be aligned.
		ref_selection (tuple): three-atom selection for reference molecule.
		mob_selection (tuple): three-atom selection for mobile molecule.
			Structure should be similar to that of ref_selection for proper alignment. 
		verbose (bool): confirm where dye will be attached.

	Returns:
		None: in-place transformation.
	'''
	ref1, ref2, ref3 = reference.select_atoms(*ref_selection).atoms.positions
	mob1, mob2, mob3 = mobile.select_atoms(*mob_selection).atoms.positions

	# Align atoms ref1 and mob1 (using a translation)
	translation = translate(ref1-mob1)

	# Align atoms ref2 and mob2 (using a rotation)
	vec1 = ref2 - ref1
	vec2 = mob2 - mob1
	axis = -np.cross(vec1, vec2)
	norm1 = np.linalg.norm(vec1)
	norm2 = np.linalg.norm(vec2)
	angle = np.degrees(np.arccos(np.dot(vec1, vec2)/(norm1*norm2)))
	rotation1 = rotate(angle, direction=axis, point=ref1)

	# Compute position of mob3 after the first two transformations but before the third one
	matrix = rotation_matrix(np.radians(angle), axis, ref1)
	R = matrix[:3, :3].T
	T = matrix[:3, 3]
	mob3_prime = np.dot(mob3 + (ref1-mob1), R) + T

	# Align atoms ref3 and mob3 with a rotation
	axis2 = -vec1 / norm1
	vec3 = (ref3 - ref2) - np.dot((ref3 - ref2), axis2)*axis2
	vec4 = (mob3_prime - ref2) - np.dot((mob3_prime - ref2), axis2)*axis2
	norm3 = np.linalg.norm(vec3)
	norm4 = np.linalg.norm(vec4)
	angle2 = np.degrees(np.arccos(np.dot(vec3, vec4)/(norm3*norm4)))
	rotation2 = rotate(angle2, direction=axis2, point=ref2)

	# Apply transformations
	workflow = [translation, rotation1, rotation2]
	mobile.trajectory.add_transformations(*workflow)

	resname = str(set(reference.select_atoms(*ref_selection).atoms.resnames))
	dyename = str(set(mobile.select_atoms(*mob_selection).atoms.resnames))
	
	if verbose:
		print("Dye was aligned to residue " + resname + ".")

def get_vdw_radii(molecule):
	'''Return an array with the approximate VDW radii of the atoms in the molecule (MDAnalysis.Universe instance).
	'''
	return np.asarray([md.topology.tables.vdwradii[element] for element in molecule.atoms.types])

def check_frame_overlap(molecule_1, molecule_2, vdw_radii_molecule_1, vdw_radii_molecule_2, verbose=False):
	'''Return True iff atoms in molecule_1 and molecule_2 overlap. 

	Atoms are overlapping when their distance is less than or equal to the sum of the VDW radii.

	Args:
		molecule_1 (MDAnalysis.Universe or AtomGroup): Universe instance of a molecule.
		mobile (MDAnalysis.Universe or AtomGroup): Universe instance of another molecule.
		vdw_radii_molecule_1 (np.ndarray): approximate VDW radii of atoms in molecule_1.
		vdw_radii_molecule_2 (np.ndarray): approximate VDW radii of atoms in molecule_2.
		verbose (bool): print frames with overlapping to stdout.

	Returns:
		bool: True iff atoms in molecule_1 and molecule_2 overlap.
	
	Raises:
		AssertionError: If the number of atoms in molecule_1 or molecule_2 is not the same as the 
			number of elements in vdw_radii_molecule_1 or vdw_radii_molecule_2 respectively.
	'''

	positions_molecule_1 = molecule_1.atoms.positions
	positions_molecule_2 = molecule_2.atoms.positions

	dist_matrix = cdist(positions_molecule_1, positions_molecule_2).flatten()
	min_dist_allowed = np.add.outer(vdw_radii_molecule_1, vdw_radii_molecule_2).flatten()

	assert(dist_matrix.size == min_dist_allowed.size)

	# if verbose:
	# 	frame1 = str(molecule_1.universe.trajectory.frame)
	# 	mol1 = str(molecule_1.universe.filename)
		
	# 	frame2 = str(molecule_2.universe.trajectory.frame)
	# 	mol2 = str(molecule_2.universe.filename)

	# 	print("Frames "+frame1+" and "+frame2+" contain superimposed atoms.")

	return (dist_matrix <= min_dist_allowed).any()

def overlap_dye(ref, dye, resid, sel_mode="indices", max_frames=100000, prefix="", verbose=False):
	'''Perform in-place dye alignment to ref molecule and return frames of trajectory with no atom overlapping.

	A subset of the atoms belonging to the dyes are selected to check for overlap given that some overlap with the
	reference system is expected given that the dye is inserted by alignemnt with reference atoms.

	Args:
		ref (MDAnalysis.Universe): Universe instance of reference system.
		dye (MDAnalysis.Universe): Universe instance of dye.
		resid (int): residue index from ref where dye will be attached.
		sel_mode (str): selection mode (only option implemented is by residue index).
		max_frames (int): maximum number of frames from dye trajectories that will be taken into account.
			Default 100000.
		prefix (str): prefix for output files.
		verbose (bool): whether to print debugging information.

	Returns:
		np.ndarray: frame indices from dye trajectories that don't show overlapping between atoms.
			If no appropriate frames are found, None is returned and no error is thrown.
	'''
	if (sel_mode == 'indices'):
		ref, dye_anchor_sel = alignment_selection(ref, resid)
	# elif (sel_mode == 'custom'):
	# 	dye1_anchor_sel = (resid1)
	else:
		raise NotImplementedError("Only selection by indices allowed.")
	
	# TODO make alignment selection more general for the dye (especially nucleic acids)
	alingment_zone_dye = ("name SG", "name CB", "name CA")

	# Transformations (in-place)
	pair_fit(ref, dye, dye_anchor_sel, alingment_zone_dye)

	# Save initial fitted structures
	dye.atoms.write(prefix + "_dye_fitted.pdb")
	
	# Get frame number
	n_frames = min(dye.trajectory.n_frames, max_frames)

	# Constrain atom selection to check overlap
	include_ref = "around 30 resid " + str(resid)

	# TODO: expand insertion residue options
	include_dye = "not ((resname CYS) or (around 10 resname CYS))"

	ref_subset = ref.select_atoms(include_ref)
	dye_subset = dye.select_atoms(include_dye)

	vdwradii_ref_subset = get_vdw_radii(ref_subset)
	vdwradii_dye_subset = get_vdw_radii(dye_subset)

	frames = []
	
	for i in range(n_frames):
		dye.trajectory[i]

		check = check_frame_overlap(ref_subset, dye_subset, vdwradii_ref_subset, vdwradii_dye_subset, verbose=verbose)
		
		if check:
			continue

		frames.append(i)

	if (len(frames)==0 and verbose):
		print("\nWarning: no allowed dye conformations found.")
		print("Check file: " + prefix + "_dye_fitted.pdb")

	return frames



def overlap_pair(ref, dye1, dye2, resid1, resid2, sel_mode="indices", max_frames=100000, prefix="", verbose=False):
	'''Perform in-place dye alignment to ref molecule and return frames of trajectory with no atom overlapping.

	A subset of the atoms belonging to the dyes are selected to check for overlap given that some overlap with the
	reference system is expected given that the dyes are inserted by alignemnt with reference atoms.

	Args:
		ref (MDAnalysis.Universe): Universe instance of reference system.
		dye1 (MDAnalysis.Universe): Universe instance of donor dye.
		dye2 (MDAnalysis.Universe): Universe instance of acceptor dye.
		resid1 (int): residue index from ref where dye1 will be attached.
		resid2 (int): residue index from ref where dye2 will be attached.
		sel_mode (str): selection mode (only option implemented is by residue index).
		max_frames (int): maximum number of frames from dye trajectories that will be taken into account.
			Default 100000.
		prefix (str): prefix for output files.
		verbose (bool): whether to print accesory information to stdout.

	Returns:
		np.ndarray: frame indices from dye trajectories that don't show overlapping between atoms.
			If no appropriate frames are found, None is returned and no error is thrown.
	'''
	# Select anchoring places for the dyes
	
	if (sel_mode == 'indices'):
		ref, dye1_anchor_sel = alignment_selection(ref, resid1)
		ref, dye2_anchor_sel = alignment_selection(ref, resid2)
	# elif (sel_mode == 'custom'):
	# 	dye1_anchor_sel = (resid1)
	# 	dye2_anchor_sel = (resid2)
	else:
		raise NotImplementedError("Only selection by indices allowed.")
	
	# TODO make alignment selection more general for the dye (especially nucleic acids)
	alingment_zone_dye = ("name SG", "name CB", "name CA")

	# Transformations (in-place)
	pair_fit(ref, dye1, dye1_anchor_sel, alingment_zone_dye)
	pair_fit(ref, dye2, dye2_anchor_sel, alingment_zone_dye)

	# Save initial fitted structures
	dye1.atoms.write(prefix + '_donor_fitted.pdb')
	dye2.atoms.write(prefix + '_acceptor_fitted.pdb')
	
	# Get frame number
	n_frames = min(dye1.trajectory.n_frames, dye2.trajectory.n_frames, max_frames)

	# Constrain atom selection to check overlap
	include_1 = "around 30 resid " + str(resid1)
	include_2 = "around 30 resid " + str(resid2)

	# TODO: expand insertion residue options
	include = "not ((resname CYS) or (around 10 resname CYS))"

	ref_subset_1 = ref.select_atoms(include_1)
	ref_subset_2 = ref.select_atoms(include_2)
	dye1_subset = dye1.select_atoms(include)
	dye2_subset = dye2.select_atoms(include)

	vdwradii_ref_subset_1 = get_vdw_radii(ref_subset_1)
	vdwradii_ref_subset_2 = get_vdw_radii(ref_subset_2)
	vdwradii_dye1_subset = get_vdw_radii(dye1_subset)
	vdwradii_dye2_subset = get_vdw_radii(dye2_subset)

	frames = []
	for i in range(n_frames):
		dye1.trajectory[i]
		dye2.trajectory[i]

		check1 = check_frame_overlap(
			ref_subset_1, 
			dye1_subset, 
			vdwradii_ref_subset_1, 
			vdwradii_dye1_subset, 
			verbose=verbose)
		
		if check1:
			continue

		check2 = check_frame_overlap(
			ref_subset_2, 
			dye2_subset, 
			vdwradii_ref_subset_2, 
			vdwradii_dye2_subset, 
			verbose=verbose)

		if check2:
			continue

		check3 = check_frame_overlap(
			dye1_subset, 
			dye2_subset, 
			vdwradii_dye1_subset, 
			vdwradii_dye2_subset, 
			verbose=verbose)

		if check3:
			continue

		frames.append(i)

	if (len(frames)==0):
		print("\nWarning: no allowed dye conformations found.")
		print("Check files: " + prefix + "_donor_fitted.pdb and " + prefix +  "_acceptor_fitted.pdb")

	return frames

def position_variance(dye, dipole, frames):
	'''Compute the distance variance of a dye dipole w.r.t. a point.
	
	The variance is computed as the distance variance w.r.t. to the center of mass of the first frame.

	Args:
		dye (MDAnalysis.Universe): Universe instance of dye.
		dipole: atom selection in MDAnalysis syntax for dipole atoms.
		frames: frames from dye trajectory to be used.

	Output:
		float: distance variance.
	'''
	atoms = dye.select_atoms(*dipole)
	
	positions = []
	for f in frames:
		dye.trajectory[f]
		position = np.mean(atoms.positions, axis=1)
		positions.append(position)

	pos = np.asarray(positions)
	ref = np.asarray([positions[0]])
	distances = cdist(pos, ref).flatten()

	return np.std(distances)

def direction_variance(dye, dipole, frames):
	'''Compute the direction variance of a dye dipole w.r.t. initial direction.

	The direction variance is defined as the variance in the angle formed by the dipole vectors
	across all frames.

	Args:
		dye (MDAnalysis.Universe): Universe instance of dye.
		dipole: atom selection in MDAnalysis syntax for dipole atoms.
		frames: frames from dye trajectory to be used.
	
	Output:
		float: direction variance.
	'''
	atoms = dye.select_atoms(*dipole)
	
	directions = []
	for f in frames:
		dye.trajectory[f]
		direction = atoms.positions[1] - atoms.positions[0]
		directions.append(direction)

	directions = np.asarray(directions)
	directions /= np.linalg.norm(directions, axis=1)[:,None]
	ref = np.asarray([directions[0]])
	products = np.einsum('ij,ij->i', directions, ref)
	products = np.clip(products, -1, 1)
	angles = np.arccos(products)

	return np.std(angles)
