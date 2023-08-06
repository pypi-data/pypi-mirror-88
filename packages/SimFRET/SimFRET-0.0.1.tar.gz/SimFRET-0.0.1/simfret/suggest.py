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
from suggest_utils import compute_distances, position_to_index

#TODO let the user pick one residue, show other residues in the FRET vecinity, show big distance difference between state A and B

def set_args():
	'''Construct argument parser for suggest.py.
	'''

	parser = argparse.ArgumentParser(description="Suggest residues to place FRET dyes.", epilog="Output: <prefix>_residues.txt")
	parser.add_argument("-r", "--ref", help="Structure file (any format accepted by MDAnalysis).", required=True)
	parser.add_argument("-t", "--traj", help="Trajectory file (any format accepted by MDAnalysis).", required=True)
	parser.add_argument("-c", "--constraint", help="Maximum distance admitted for the dyes (Å).", default=100.0, type=float, required=False)
	parser.add_argument("-p", "--prefix", help="Output files' prefix.", dest="prefix", default="PyFRET_suggest", required=False)

	return parser.parse_args()

def main():
	'''Suggest good residue pairs for dye insertion.

	This program takes a reference molecule and trajectory. It then computes the average and std. dev. of 
	the inter-residue distance for all residue pairs. The residue pairs are then sorted by descending 
	distance std. dev. and the top 100 pairs are saved in residues.txt. A maximum distance constraint 
	can be provided.

	For usage instructions run:
		$ python path/to/this/script/suggest.py -h 

	Outputs residues.txt, containing residue-pairs with high distance variance.
	'''
	
	args = set_args()

	#Load trajectory
	trajectory = Universe(args.ref, args.traj)
	
	#Compute distances between CA and/or C5'/C5* (distance between residues) and store them in array
	n_atoms, resnames, distances = compute_distances(trajectory)

	#Compute mean distances and variance
	var = np.var(distances, axis=0)
	mean = np.mean(distances, axis=0)
	      
	#Get top_k max variances and find their position in the array
	top_k = 100
	indices = np.argpartition(var, -top_k)[-top_k:]
	
	#Sort the indices according to variance value
	indices = indices[np.argsort(var[indices])[::-1]]

	#Translate array position to residue indices
	pos2idx = position_to_index(n_atoms)

	#Write output file
	with open(args.prefix + "_residues.txt", "w") as output:
		output.write("Suggested pair of residues to place the FRET dyes:\n")
		for idx in indices:
			resid1, resid2 = pos2idx[idx]
			resname1, resname2 = resnames[resid1], resnames[resid2]
			if (mean[idx] < args.constraint):
				output.write("Residues " + str(resid1) + " (" + resname1 + ") and " + str(resid2) + " (" + resname2 + "): ")
				output.write(str(mean[idx]) + " ± " + str(np.sqrt(var[idx])) + " Å\n")

	#TODO output nice frames for simulation --> frames where distances between selected residues are high/low
	
if __name__ == '__main__':
	main()