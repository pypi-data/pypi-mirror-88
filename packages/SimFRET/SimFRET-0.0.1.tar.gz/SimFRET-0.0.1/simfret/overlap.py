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
from MDAnalysis.coordinates.DCD import DCDWriter
from overlap_utils import overlap

def set_args():
	'''Construct argument parser for overlap.py.
	'''

	parser = argparse.ArgumentParser(description="Anchor FRET dyes to reference molecule. (This script is intended to visualize dye docking only.)", epilog="Output: <prefix>_donor_fitted.pdb, <prefix>_acceptor_fitted.pdb, <prefix>_alignment_donor.dcd, <prefix>_alignment_acceptor.dcd")
	parser.add_argument("-r", "--ref", help="Structure file for reference molecule.", required=True, dest="ref", metavar="REFERENCE")
	parser.add_argument("-d", "--donor", help="Structure file for donor dye.", required=True, dest="dye1", metavar="DONOR STRUCTURE")
	parser.add_argument("-dt", "--donor_traj", help="Trajectory file for donor dye.", required=True, dest="dye1_traj", metavar="DONOR TRAJ")
	parser.add_argument("-a", "--acceptor", help="Structure file for acceptor dye.", required=True, dest="dye2", metavar="ACCEPTOR STRUCTURE")
	parser.add_argument("-at", "--acceptor_traj", help="Trajectory file for acceptor dye.", required=True, dest="dye2_traj", metavar="ACCEPTOR TRAJ")
	parser.add_argument("-rd", "--residue_donor", help="Residue index to attach donor dye. If this flag is set, --residue_acceptor must also be set.", type=int, required=False, dest="resid1", metavar="DONOR RES")
	parser.add_argument("-ra", "--residue_acceptor", help="Residue index to attach acceptor dye. If this flag is set, --residue_donor must also be set.", type=int, required=False, dest="resid2", metavar="ACCEPTOR RES")
	# parser.add_argument("-da", "--donor_align", help="Three-atom group to attach donor dye. If this flag is set, --acceptor_align must also be set.", required=False, dest="don_align", metavar="SELECTION")
	# parser.add_argument("-aa", "--acceptor_align", help="Three-atom group to attach acceptor dye. If this flag is set, --donor_align must also be set.", required=False, dest="acc_align", metavar="SELECTION")
	parser.add_argument("-p", "--prefix", help="Output files' prefix.", default="PyFRET_overlap", required=False, dest="prefix")

	return parser.parse_args()

# def check_sel_mode(args):
# 	'''Check if user provided consistent selections for dye alignment and determine which mode was used.
# 	'''
# 	indices = (args.resid1 is not None) and (args.resid2 is not None)
# 	custom = (args.don_align is not None) and (args.acc_align is not None)

# 	if indices and custom:
# 		print("Both indices and a custom selection were provided.")
# 		print("Use only one method to select where the dyes will be inserted.")
# 		exit(1)
# 	elif indices:
# 		return "indices"
# 	elif custom:
# 		return "custom"
# 	else:
# 		print("Consistent selections to decide where to insert the dyes were not provided.")
# 		print("Select the appropriate residues (by index) setting the flags --residue_donor and --residue_acceptor or provide a custom selection through the flags --donor_align and --acceptor_align.")
# 		exit(1)	

def main():
	'''Overlaps dye trajectories to reference structure and saves them for verification.

	The program first aligns the dye molecules to the reference structure and then selects the dye trajectory
	frames where there is no atom overlapping between dyes or with reference structure. The frames are saved
	to output files. 

	For usage instructions run:
		>> $ python path/to/this/script/overlap.py -h 

	Outputs dye structures (<prefix>_donor_fitted.pdb, <prefix>_acceptor_fitted.pdb) and trajectory files with 
	allowed frames (<prefix>_alignment_donor.dcd, <prefix>_alignment_acceptor.dcd).
	'''
	
	args = set_args()

	#Load files
	ref  = Universe(args.ref)
	dye1 = Universe(args.dye1, args.dye1_traj)
	dye2 = Universe(args.dye2, args.dye2_traj)

	#Select anchoring places for the dyes
	#Check type of molecule and select atoms for alignment accordingly
	#TODO: expand selection mode options for dye alignment.
	sel_mode = 'indices' # check_sel_mode(args)
	
	frames = overlap(ref, dye1, dye2, args.resid1, args.resid2, sel_mode=sel_mode, max_frames=10000, prefix=args.prefix, verbose=False)
	frame_num = len(frames)
	
	with DCDWriter(args.prefix + "_alignment_donor.dcd", dye1.trajectory.n_atoms) as writer_donor, DCDWriter(args.prefix + "_alignment_acceptor.dcd", dye2.trajectory.n_atoms) as writer_acceptor:

		for f1, f2 in frames:
			dye1.trajectory[f1]
			dye2.trajectory[f2]

			writer_donor.write(dye1)
			writer_acceptor.write(dye2)

		print("Wrote %.d frames" % frame_num)

	if (frame_num==0):
		print("Warning: no allowed dye conformations found. Try placing the dyes in a different site.")
		

if __name__ == '__main__':
	main()