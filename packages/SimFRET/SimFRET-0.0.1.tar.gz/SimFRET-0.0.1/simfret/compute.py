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
from overlap_utils import overlap
from compute_utils import compute

def set_args():
	'''Construct argument parser for compute.py.
	'''

	parser = argparse.ArgumentParser(description="Compute FRET efficiency.", epilog="Output: <prefix>_dist.txt, <prefix>_kappa2.txt, <prefix>_insteff.txt")
	parser.add_argument("-r", "--ref", help="Structure file for reference.", required=True, dest="ref", metavar="REF STRUCTURE")
	parser.add_argument("-rt", "--ref_traj", help="If provided, output will be averaged over trajectory. All frames are used unless --sample is set.", required=False, dest="ref_traj", metavar="REF TRAJ")
	parser.add_argument("-s", "--sample", help="If provided, pick frames from REF TRAJ every N frames.", required=False, dest="sample", type=int, default=1, metavar="N")
	parser.add_argument("-d", "--donor", help="Structure file for donor dye.", required=True, dest="dye1", metavar="DONOR STRUCTURE")
	parser.add_argument("-dt", "--donor_traj", help="Trajectory file for donor dye.", required=True, dest="dye1_traj", metavar="DONOR TRAJ")
	parser.add_argument("-a", "--acceptor", help="Structure file for acceptor dye.", required=True, dest="dye2", metavar="ACCEPTOR STRUCTURE")
	parser.add_argument("-at", "--acceptor_traj", help="Trajectory file for acceptor dye.", required=True, dest="dye2_traj", metavar="ACCEPTOR TRAJ")
	parser.add_argument("-rd", "--residue_donor", help="Residue index to attach donor dye. If this flag is set, --residue_acceptor must also be set.", type=int, required=True, dest="resid1", metavar="DONOR RES")
	parser.add_argument("-ra", "--residue_acceptor", help="Residue index to attach acceptor dye. If this flag is set, --residue_donor must also be set.", type=int, required=True, dest="resid2", metavar="ACCEPTOR RES")
	parser.add_argument("-R0", help="R0 (Å) for the FRET dyes pair.", required=True, type=float, dest="R0", metavar="R0")
	parser.add_argument("-avg", "--averaging_regime", help="Averaging regime. Default 'isotropic'.", default="isotropic", choices={"isotropic", "static", "dynamic"}, required=False, dest="regime")
	parser.add_argument("--burst", help="Turn on burst averaging: 0 = no (default), 1 = yes.", default=0, type=int, choices={0, 1}, required=False, dest="burst_avg")
	parser.add_argument("--burst_threshold", help="Burst size threshold to use with burst averaging (default 30).", default=30, type=int, required=False, dest="burst_threshold")
	parser.add_argument("--burst_decay", help="Burst size decay constant to use with burst averaging (default 3).", default=3, type=int, required=False, dest="burst_decay")	
	parser.add_argument("-p", "--prefix", help="Output files' prefix.", default="PyFRET_compute", required=False, dest="prefix")

	return parser.parse_args()

def main():
	'''Compute FRET efficiency for a given donor-acceptor pair using specific frames from their trajectories.

	The program first aligns the dye molecules to the reference structure and then selects the dye trajectory
	frames where there is no atom overlapping between dyes or with reference structure. These frames are then 
	used to compute FRET efficiency for the provided reference structure. If only one reference structure (and
	no trajectory) is provided, a single FRET efficiency value is produced. However, if a trajectory for the 
	reference molecule is provided, a file containing all the FRET efficiencies is produced. A FRET efficiency
	distribution can be generated from said file.

	For usage instructions run:
		>> $ python path/to/this/script/computation.py -h 

	Output if only a single reference structure is provided: <prefix>_dist.txt, <prefix>_kappa2.txt, <prefix>_insteff.txt.

	Output if a reference trajectory is provided: <prefix>_frame<frame#>_dist.txt, <prefix>_frame<frame#>_kappa2.txt, 
		<prefix>_frame<frame#>_insteff.txt, <prefix>_all_dist.txt, <prefix>_all_kappa2.txt, <prefix>_all_insteff.txt.
	'''

	args = set_args()

	#Load trajectory files

	#Determine mode (fixed or dynamic reference molecule)
	if (args.ref_traj == None):
		ref = Universe(args.ref)
		mode = "fixed"
	else:
		ref = Universe(args.ref, args.ref_traj)
		mode = "dynamic"

	#Compute distance distribution, kappa squared, and FRET Efficiency

	if (mode == "fixed"):
		dye1 = Universe(args.dye1, args.dye1_traj)
		dye2 = Universe(args.dye2, args.dye2_traj)
		frames = overlap_pair(ref, dye1, dye2, args.resid1, args.resid2, prefix=args.prefix)
		distances, kappa2, fret, error = compute(dye1, dye2, args.R0, frames, prefix=args.prefix, regime=args.regime, burst_averaging_on=bool(args.burst_avg), burst_threshold=args.burst_threshold, decay_const=args.burst_decay)

		print("Final FRET:", fret, "±", error)

	elif (mode == "dynamic"):
		all_distances, all_kappa2, all_fret, all_error = [], [], [], []

		total_frames = ref.trajectory.n_frames // args.sample
		
		for idx, _ in enumerate(ref.trajectory[::args.sample]):
			dye1 = Universe(args.dye1, args.dye1_traj)
			dye2 = Universe(args.dye2, args.dye2_traj)
			frames = overlap_pair(ref, dye1, dye2, args.resid1, args.resid2, max_frames=100000, prefix=args.prefix + "_frame" + str(idx))

			if frames:
				distances, kappa2, fret, error = compute(dye1, dye2, args.R0, frames, prefix=args.prefix + "_frame" + str(idx), regime=args.regime, burst_averaging_on=bool(args.burst_avg), burst_threshold=args.burst_threshold, decay_const=args.burst_decay)
				
				all_distances.extend(list(distances))
				all_kappa2.extend(list(kappa2))
				all_fret.append(fret)
				all_error.append(error)

				progress = int(((idx+1)/total_frames)*100)
				empty = 100-progress

				print("\r" + "Progress: |" + "#"*progress + " "*empty + "|", end="")
				
		print("")

		all_distances = np.asarray(all_distances)
		all_kappa2 = np.asarray(all_kappa2)
		all_fret = np.asarray(all_fret)
		all_error = np.asarray(all_error)

		np.savetxt(args.prefix + "_all_dist.txt", all_distances)
		np.savetxt(args.prefix + "_all_kappa2.txt", all_kappa2)
		np.savetxt(args.prefix + "_all_fret.txt", all_fret)
		np.savetxt(args.prefix + "_all_error.txt", all_error)

		print("Final FRET:", np.mean(all_fret), "±", np.mean(all_error))

if __name__ == '__main__':
	main()