# SimFRET
 A Python package to simulate FRET experiments.
 
## Installation
The easiest way is through conda:
```
$ conda create --name SimFRET --file simfret.yml
```
## Usage 
 There are four modules (`simulate.py`, `suggest.py`, `overlap.py`, `compute.py`). <br>
 - `simulate.py` runs a quick simulation using the SMOG potential. Input files for this module can be obtained through the [SMOG Webtool](http://smog-server.org/cgi-bin/GenTopGro.pl). <br>
 - `suggest.py` suggests pairs of residues for FRET dye attachment. <br>
 - `overlap.py` overlaps the dyes to the macromolecule (some dye molecules are already available under the folder dyes). <br>
 - `compute.py` computes the FRET efficiency (ignoring frames where dye atoms are superimposed with the macromolecule). <br>
 Note: `simulate.py` and `suggest.py` are not necessary if the molecule under study has already been simulated and the places where FRET dyes are attached are known. <br>
### simulate.py
```
usage: simulate.py [-h] -ref REF -top TOP [-p PREFIX] [-dt TIMESTEP]
                   [--nsteps NSTEPS] [--nstxout NSTXOUT] [--nstlog NSTLOG]
                   [--nstdcdout NSTDCDOUT] [--gamma GAMMA] [-t TEMP]
                   [--rcutoff RCUTOFF]

Run fast simulations with the SMOG potential.

optional arguments:
  -h, --help            show this help message and exit
  -ref REF              Structure file (.gro) from SMOG/SOMG2.
  -top TOP              Topology file (.top) from SMOG/SOMG2.
  -p PREFIX, --prefix PREFIX
                        Output files' prefix (default SMOG).
  -dt TIMESTEP, --timestep TIMESTEP
                        Simulation timestep in ps (default 2 fs).
  --nsteps NSTEPS       Number of simulation steps (defaul 50000).
  --nstxout NSTXOUT     Interval to save checkpoint (default 10000 steps).
  --nstlog NSTLOG       Interval to save energy information (default 1000
                        steps).
  --nstdcdout NSTDCDOUT
                        Interval to save simulation frames (default 1000
                        steps).
  --gamma GAMMA         Friction factor for Langeving integrator in ps^-1
                        (default 1/ps).
  -t TEMP, --temperature TEMP
                        Simulation temperature. Not physical temperature
                        (default 75 K).
  --rcutoff RCUTOFF     Cutoff for nonbonded interactions in nm (default 1.5
                        nm).

Output: <prefix>_settings.txt, <prefix>_traj.dcd, <prefix>_checkpoint.chk,
<prefix>_energy.log
```
### suggest.py
```
usage: suggest.py [-h] -r REF -t TRAJ [-c CONSTRAINT] [-p PREFIX]

Suggest residues to place FRET dyes.

optional arguments:
  -h, --help            show this help message and exit
  -r REF, --ref REF     Structure file (any format accepted by MDAnalysis).
  -t TRAJ, --traj TRAJ  Trajectory file (any format accepted by MDAnalysis).
  -c CONSTRAINT, --constraint CONSTRAINT
                        Maximum distance admitted for the dyes (Å).
  -p PREFIX, --prefix PREFIX
                        Output files' prefix.

Output: <prefix>_residues.txt
```
### overlap.py
```
usage: overlap.py [-h] -r REFERENCE -d DONOR STRUCTURE -dt DONOR TRAJ -a
                  ACCEPTOR STRUCTURE -at ACCEPTOR TRAJ [-rd DONOR RES]
                  [-ra ACCEPTOR RES] [-p PREFIX]

Anchor FRET dyes to reference molecule. (This script is intended to visualize
dye docking only.)

optional arguments:
  -h, --help            show this help message and exit
  -r REFERENCE, --ref REFERENCE
                        Structure file for reference molecule.
  -d DONOR STRUCTURE, --donor DONOR STRUCTURE
                        Structure file for donor dye.
  -dt DONOR TRAJ, --donor_traj DONOR TRAJ
                        Trajectory file for donor dye.
  -a ACCEPTOR STRUCTURE, --acceptor ACCEPTOR STRUCTURE
                        Structure file for acceptor dye.
  -at ACCEPTOR TRAJ, --acceptor_traj ACCEPTOR TRAJ
                        Trajectory file for acceptor dye.
  -rd DONOR RES, --residue_donor DONOR RES
                        Residue index to attach donor dye. If this flag is
                        set, --residue_acceptor must also be set.
  -ra ACCEPTOR RES, --residue_acceptor ACCEPTOR RES
                        Residue index to attach acceptor dye. If this flag is
                        set, --residue_donor must also be set.
  -p PREFIX, --prefix PREFIX
                        Output files' prefix.

Output: <prefix>_donor_fitted.pdb, <prefix>_acceptor_fitted.pdb,
<prefix>_alignment_donor.dcd, <prefix>_alignment_acceptor.dcd
```
### compute.py
```
usage: compute.py [-h] -r REF STRUCTURE [-rt REF TRAJ] [-s N] -d DONOR
                  STRUCTURE -dt DONOR TRAJ -a ACCEPTOR STRUCTURE -at ACCEPTOR
                  TRAJ -rd DONOR RES -ra ACCEPTOR RES -R0 R0
                  [-avg {static,isotropic,dynamic}] [--burst {0,1}]
                  [--burst_threshold BURST_THRESHOLD]
                  [--burst_decay BURST_DECAY] [-p PREFIX]

Compute FRET efficiency.

optional arguments:
  -h, --help            show this help message and exit
  -r REF STRUCTURE, --ref REF STRUCTURE
                        Structure file for reference.
  -rt REF TRAJ, --ref_traj REF TRAJ
                        If provided, output will be averaged over trajectory.
                        All frames are used unless --sample is set.
  -s N, --sample N      If provided, pick frames from REF TRAJ every N frames.
  -d DONOR STRUCTURE, --donor DONOR STRUCTURE
                        Structure file for donor dye.
  -dt DONOR TRAJ, --donor_traj DONOR TRAJ
                        Trajectory file for donor dye.
  -a ACCEPTOR STRUCTURE, --acceptor ACCEPTOR STRUCTURE
                        Structure file for acceptor dye.
  -at ACCEPTOR TRAJ, --acceptor_traj ACCEPTOR TRAJ
                        Trajectory file for acceptor dye.
  -rd DONOR RES, --residue_donor DONOR RES
                        Residue index to attach donor dye. If this flag is
                        set, --residue_acceptor must also be set.
  -ra ACCEPTOR RES, --residue_acceptor ACCEPTOR RES
                        Residue index to attach acceptor dye. If this flag is
                        set, --residue_donor must also be set.
  -R0 R0                R0 (Å) for the FRET dyes pair.
  -avg {static,isotropic,dynamic}, --averaging_regime {static,isotropic,dynamic}
                        Averaging regime. Default 'isotropic'.
  --burst {0,1}         Turn on burst averaging: 0 = no (default), 1 = yes.
  --burst_threshold BURST_THRESHOLD
                        Burst size threshold to use with burst averaging
                        (default 30).
  --burst_decay BURST_DECAY
                        Burst size decay constant to use with burst averaging
                        (default 3).
  -p PREFIX, --prefix PREFIX
                        Output files' prefix.

Output: <prefix>_dist.txt, <prefix>_kappa2.txt, <prefix>_insteff.txt
```
