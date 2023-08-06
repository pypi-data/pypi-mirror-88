'''
Copyright (c) 2020, Diego E. Kleiman
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
'''

import sys
import argparse
from simtk.unit import nanometer, picosecond, kelvin
from simtk.openmm.app import *
from simtk.openmm import *

# Define simulation hyperparameters

def set_args():
	'''Construct argument parser for simulate.py.
	'''

	parser = argparse.ArgumentParser(description="Run fast simulations with the SMOG potential.", epilog="Output: <prefix>_settings.txt, <prefix>_traj.dcd, <prefix>_checkpoint.chk, <prefix>_energy.log")
	parser.add_argument("-ref", help="Structure file (.gro) from SMOG/SOMG2.", dest="ref", required=True)
	parser.add_argument("-top", help="Topology file (.top) from SMOG/SOMG2.", dest="top", required=True)
	parser.add_argument("-p", "--prefix", help="Output files' prefix (default SMOG).", dest="prefix", default="SMOG", required=False)
	parser.add_argument("-dt", "--timestep", help="Simulation timestep in ps (default 2 fs).", dest="dt", default=0.002, type=float, metavar="TIMESTEP", required=False)
	parser.add_argument("--nsteps", help="Number of simulation steps (defaul 50000).", dest="nsteps", default=50000, type=int, required=False)
	parser.add_argument("--nstxout", help="Interval to save checkpoint (default 10000 steps).", dest="nstxout", default=10000, type=int, required=False)
	parser.add_argument("--nstlog", help="Interval to save energy information (default 1000 steps).", dest="nstlog", default=1000, type=int, required=False)
	parser.add_argument("--nstdcdout", help="Interval to save simulation frames (default 1000 steps).", dest="nstdcdout", default=1000, type=int, required=False)
	parser.add_argument("--gamma", help="Friction factor for Langeving integrator in ps^-1 (default 1/ps).", dest="gamma", default=1.0, type=float, required=False)
	parser.add_argument("-t", "--temperature", help="Simulation temperature. Not physical temperature (default 75 K).", dest="temp", default=75.0, type=float, required=False)
	parser.add_argument("--rcutoff", help="Cutoff for nonbonded interactions in nm (default 1.5 nm).", dest="rcutoff", default=1.5, type=float, required=False)

	return parser.parse_args()

def main():
	'''Compute fast simulations using the SMOG potential.

	For instruction on how to preprocess input files see http://smog-server.org/
	For usage instructions run:
		$ python path/to/this/script/simulate.py -h 

	Outputs system trajectory, settings employed in the run, and log files.
	'''
	
	args = set_args()

	#Get parameters
	with open(args.prefix + "_settings.txt", "w") as output:
		output.write("Settings used with SMOG potential for simulation of " + args.ref + " with topology " + args.top + "\n")
		output.write("timestep 	= " + str(args.dt) + "\n")
		output.write("nsteps 	= " + str(args.nsteps) + "\n")
		output.write("nstxout 	= " + str(args.nstxout) + "\n")
		output.write("nstdcdout = " + str(args.nstdcdout) + "\n")
		output.write("gamma 	= " + str(args.gamma) + "\n")
		output.write("temp 		= " + str(args.temp) + "\n")

	#Load gro and top files from input
	gro = GromacsGroFile(args.ref)
	top = GromacsTopFile(args.top)

	#Create system
	system = top.createSystem(nonbondedMethod=CutoffNonPeriodic, nonbondedCutoff=args.rcutoff * nanometer)

	# Check and fix exclusions/exceptions problems for heterogenous systems (amino acid + nulceic acids).
	# This issue arises because OpenMM does not automatically add exclusions form .top file to the 
	# CustomNonbondedForce instance belonging to system (but it does add them to NonbondedForce). The number 
	# (and atom indices) of exclusions from CustomNonbondedForce must match the number of exceptions in 
	# NonbondedForce. If the problem goes unfixed, an error is thrown.

	#system.getForce(0) is NonbondedForce and system.getForce(1) is CustomNonbondedForce
	if (system.getForce(0).getNumExceptions() != system.getForce(1).getNumExclusions()):
		exceptions = system.getForce(0).getNumExceptions()
		exclusions = system.getForce(1).getNumExclusions()
		
		#Fill up exclusions until matching number of exceptions
		for idx in range(exclusions, exceptions):
			atom1, atom2 = system.getForce(0).getExceptionParameters(idx)[:2] #First two elements are atom indices
			system.getForce(1).addExclusion(atom1, atom2)

	#Check if numbers match
	assert(system.getForce(0).getNumExceptions() == system.getForce(1).getNumExclusions()) 

	#Define integrator
	integrator = LangevinIntegrator(args.temp * kelvin, args.gamma / picosecond, args.dt * picosecond)

	#Set initial variables
	simulation = Simulation(top.topology, system, integrator)
	simulation.context.setPositions(gro.positions)
	simulation.context.setVelocitiesToTemperature(args.temp * kelvin)

	#Set reporters
	simulation.reporters.append(DCDReporter(args.prefix + "_traj.dcd", args.nstdcdout))
	#TODO: add support for continuing simulation from checkpoint
	simulation.reporters.append(CheckpointReporter(args.prefix + "_checkpoint.chk", args.nstxout))
	simulation.reporters.append(StateDataReporter(args.prefix + "_energy.log", args.nstlog,
		step=True, potentialEnergy=True, temperature=True))

	#Run simulation
	simulation.step(args.nsteps)

	

if __name__ == '__main__':
	main()