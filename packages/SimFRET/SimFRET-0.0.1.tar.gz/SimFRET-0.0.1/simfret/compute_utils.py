'''
Copyright (c) 2020, Diego E. Kleiman
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
'''

import sys
import argparse
import numpy as np
import MDAnalysis as md
from MDAnalysis import Universe
import scipy.stats as st

def define_dipole_sel(dye):
	'''Return atom name selections whose positions will be used as a proxy for the dye dipole.

	Returns hard-coded atom names for those atoms at the extrema of the dye molecule.
	Currently available dyes are CY3, CY5, AX4 (Alexa488), and AM5 (Alexa594).
	More dyes will be added in future releases.

	Args:
		dye (MDAnalysis.Universe): Universe instance of dye molecule. 
			Resname must be one of 'CY3', 'CY5', 'AX4', 'AM5'.

	Returns:
		tuple: tuple of size two with atom names corresponding to dipole.
		If dye name is 'CY3' or 'CY5' returns ('name C7B', 'name C7A').
		If dye name is 'AX4' or 'AM5' returns ('name N2', 'name N11').

	Raises:
		ValueError: The dye name was not recognized.
	'''

	dye_name = dye.residues.resnames[1]

	#TODO: add more dye options
	if dye_name in ['CY3', 'CY5']:
		return ("name C7B", "name C7A")
	elif dye_name in ['AX4', 'AM5']:
		return ("name N2", "name N11")
	else:
		message = "Dye " + dye_name + " not recognized."
		raise ValueError(message)

def compute_kappa(donor, acceptor, dipole_donor, dipole_acceptor, frames):
	'''Computes kappa squared factor from donor and acceptor trajectories.

	Computes kappa squared (orientation) factor from dipole positions provided through donor and 
	acceptor trajectories.
	For information on the mathematical expression used see Eq. 3.1 in http://www.fretresearch.org/kappasquaredchapter.pdf

	Args:
		donor (MDAnalysis.Universe): Universe instance of donor dye molecule.
		acceptor (MDAnalysis.Universe): Universe instance of acceptor dye molecule.
		dipole_donor (tuple): two-tuple containing selections for donor dipole atoms.
			Obtained from define_dipole_sel().
		dipole_acceptor (tuple): two-tuple containing selections for acceptor dipole atoms.
			Obtained from define_dipole_sel().
		frames (iterable): contains indices of frames of donor and acceptor trajectories that 
			will be used to compute kappa squared. 

	Returns:
		np.ndarray: array containing kappa squared for each frame in frames.
	'''

	dipole1 = donor.select_atoms(*dipole_donor)
	dipole2 = acceptor.select_atoms(*dipole_acceptor)

	kappa2 = []

	for f in frames:
		
		donor.trajectory[f]
		acceptor.trajectory[f]

		p1, p2 = dipole1.atoms.positions
		p3, p4 = dipole2.atoms.positions

		donvec = p2 - p1
		donvec /= np.linalg.norm(donvec)
		accvec = p4 - p3
		accvec /= np.linalg.norm(accvec)
		distnorm = p3 - p1
		distnorm /= np.linalg.norm(distnorm)

		k = (np.dot(donvec, accvec) - 3*(np.dot(donvec, distnorm) * np.dot(distnorm, accvec)))**2
		kappa2.append(k)

	return np.asarray(kappa2)

def compute_distances(donor, acceptor, dipole_donor, dipole_acceptor, frames):
	'''Computes donor-acceptor distance from donor and acceptor trajectories.

	Computes distances from dipole positions provided through donor and acceptor trajectories.
	The distance is computed between gemetric centers of dipole atoms for donor and acceptor.

	Args:
		donor (MDAnalysis.Universe): Universe instance of donor dye molecule.
		acceptor (MDAnalysis.Universe): Universe instance of acceptor dye molecule.
		dipole_donor (tuple): two-tuple containing selections for donor dipole atoms.
			Obtained from define_dipole_sel().
		dipole_acceptor (tuple): two-tuple containing selections for acceptor dipole atoms.
			Obtained from define_dipole_sel().
		frames (iterable): contains indices of frames of donor and acceptor trajectories that 
			will be used to compute distance. 

	Returns:
		np.ndarray: array containing distance measured for each frame in frames.
	'''
	
	dipole1 = donor.select_atoms(*dipole_donor)
	dipole2 = acceptor.select_atoms(*dipole_acceptor)

	distances = []
	
	for f in frames:
		
		donor.trajectory[f]
		acceptor.trajectory[f]

		p1, p2 = dipole1.atoms.positions
		p3, p4 = dipole2.atoms.positions

		com_donor = (p1 + p2)/2
		com_acceptor = (p3 + p4)/2
		distance = np.linalg.norm(com_donor - com_acceptor)
		
		distances.append(distance)

	return np.asarray(distances)

class BSD_gen(st.rv_discrete):
    '''Generator class for burst size distribution. Inherits from scipy.stats.rv_discrete.

    For more details read the scipy documentation.
    '''
    
    # Overwrite probability mass function from parent class
    def _pmf(self, x, t, s):
        return 1/s*np.exp(-(x-t)/s)

def burst_average(insteff, variate_generator, burst_threshold, decay_const):
	'''Performs burst-averaging on a collection of FRET measurements. 

	To account for photon statistics, burst averages can be computed from individual FRET measurements.
	The burst size distribution is samlped from a discrete exponential decay with a minimum set threshold
	burst_threshold. The variable decay_const determines the rate in the exponential decay of the burst size 
	distribution.
	Followingly, the number of acceptor photons is sampled from a binomial distribution with probability of 
	success equal to the FRET efficiency value.
	The final, corrected FRET efficiency is computed as the sum of acceptor photons divided by the total number 
	of photons from the bursts.

	Args:
		insteff (np.ndarray): individual values of FRET efficiency.
		variate_generator (BSD_gen): instance of BSD_gen (burst size distribution generator).
		burst_threshold (int): minimum number of photons in a single burst.
		decay_const (int): decay scale of burst size distribution.

	Returns:
		float: burst-averaged FRET efficiency.
	'''
	A = []
	BS = []
	size = insteff.shape[0]

	for Ei in insteff: 
	    BSi = variate_generator.rvs(burst_threshold, decay_const) #burst size from distribution
	    BS.append(BSi)
	    Ai = np.random.binomial(BSi, Ei) #acceptor photons
	    A.append(Ai)

	A = np.asarray(A)
	BS = np.asarray(BS)

	return np.mean(A/BS), np.std(A/BS)/np.sqrt(size)

def average(distances, kappa2, R0, prefix, regime, burst_averaging_on, burst_threshold, decay_const):
	'''Returns FRET efficiency value based on the selected averaging regime.

	Computes FRET efficiency based on selected averaging regime.
	For more details on the selecting an averaging regime and how each one is computed
	see www.pnas.org/content/105/47/18337

	Args:
		distances (np.ndarray): distances between donor and acceptor for each frame.
		kappa2 (np.ndarray): kappa squared factor for each frame.
		R0 (float): Förster radius for the donor-acceptor pair.
		prefix (str): prefix of output files (per-frame FRET efficiency).
		regime (str): averaging regime (one of 'isotropic', 'dynamic', 'static').
		burst_averaging_on (bool): whether to use burst averaging or not.
		burst_threshold (int): minimum number of photons in a burst.
		decay_const (int): exponential decay scale for burst size distribution.

	Returns:
		tuple: (FRET efficiency, standard error).
			FRET efficiency (float): average FRET efficiency.
			standard error (float): standard error for FRET efficiency measurement.
		Also saves output files for instant FRET efficiencies -- <prefix>_insteff.txt

	Raises:
		ValueError: The averaging regime was not recognized.
	'''

	BSD = BSD_gen(a=burst_threshold, name="BSD")

	if (regime == 'static'):
		numerator = kappa2*(3/2)*(R0**6)
		denominator = kappa2*(3/2)*(R0**6) + distances**6
		insteff = numerator/denominator
		np.savetxt(prefix + "_insteff.txt", insteff)
		if burst_averaging_on:
			fret, error = burst_average(insteff, BSD, burst_threshold, decay_const) 
		else:
			fret = np.mean(insteff)
			error = np.std(insteff)/np.sqrt(insteff.shape[0])

	elif (regime == 'dynamic'):
		
		ratio = kappa2/(distances**6)
		insteff = ratio*(3/2)*(R0**6)/(ratio*(3/2)*(R0**6) + 1)
		np.savetxt(prefix + "_insteff.txt", insteff)
		
		if burst_averaging_on:
			fret, error = burst_average(insteff, BSD, burst_threshold, decay_const)
		else:
			ratio = np.mean(ratio)
			fret = ratio*(3/2)*(R0**6)/(ratio*(3/2)*(R0**6) + 1)
			ratio_error = np.std(kappa2/(distances**6))/np.sqrt(distances.shape[0])
			error = 2*ratio_error/((ratio+1)**3) #propagated error


	elif (regime == 'isotropic'):
		insteff = (R0**6)/(R0**6 + distances**6)
		np.savetxt(prefix + "_insteff.txt", insteff)
		if burst_averaging_on:
			fret, error = burst_average(insteff, BSD, burst_threshold, decay_const) 
		else:
			fret = np.mean(insteff)
			error = np.std(insteff)/np.sqrt(distances.shape[0])
		
	else:
		message = "Averaging regime not understood. Available options: 'static', 'dynamic', 'isotropic'."
		raise ValueError(message)

	return fret, error

def compute(dye1, dye2, R0, frames, prefix='', regime='isotropic', burst_averaging_on=False, burst_threshold=30, decay_const=3):
	'''Compute FRET efficiency for a given donor-acceptor pair using specific frames from their trajectories.

	Args:
		dye1 (MDAnalysis.Universe): Universe instance of donor dye molecule.
		dye2 (MDAnalysis.Universe): Universe instance of acceptor dye molecule.
		R0 (float): Förster radius for the donor-acceptor pair.
		frames (iterable): contains indices of frames of donor and acceptor trajectories that 
			will be used to compute FRET efficiency.
		prefix (str): prefix of output files.
		regime (str): averaging regime (one of 'isotropic' --> default, 'dynamic', 'static').
		burst_averaging_on (bool): whether to use burst averaging or not.
		burst_threshold (int): minimum number of photons in a burst.
		decay_const (int): exponential decay scale for burst size distribution.

	Returns:
		tuple: (distances, kappa2, FRET efficiency, standard error).
			distances (np.ndarray): distances between donor and acceptor for each frame.
			kappa2 (np.ndarray): kappa squared factor for each frame.
			FRET efficiency (float): average FRET efficiency.
			standard error (float): standard error for FRET efficiency measurement. 
	'''
	
	dipole1 = define_dipole_sel(dye1)
	dipole2 = define_dipole_sel(dye2)

	distances = compute_distances(dye1, dye2, dipole1, dipole2, frames)
	kappa2 = compute_kappa(dye1, dye2, dipole1, dipole2, frames)
	np.savetxt(prefix + "_dist.txt", distances)
	np.savetxt(prefix + "_kappa2.txt", kappa2)
	fret, error = average(distances, kappa2, R0, prefix, regime, burst_averaging_on, burst_threshold, decay_const)

	return distances, kappa2, fret, error
