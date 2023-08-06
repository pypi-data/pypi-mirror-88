import numpy as np
from MDAnalysis import Universe
from fretraj import FRETraj
import pickle

def save_results(results, fname):
	with open(fname + ".pickle", 'wb') as handle:
		pickle.dump(results, handle)

ref = Universe("/Users/diegoeduardo/Desktop/GitHub/PyFRET/test/1yls/1yls.25912.pdb.gro", "/Users/diegoeduardo/Desktop/GitHub/PyFRET/test/1yls/testing_traj.dcd")
donor = Universe("/Users/diegoeduardo/Desktop/GitHub/PyFRET/dyes/structure/CY3.pdb", "/Users/diegoeduardo/Desktop/GitHub/PyFRET/dyes/traj/CY3_fixed.dcd")
acceptor = Universe("/Users/diegoeduardo/Desktop/GitHub/PyFRET/dyes/structure/CY5.pdb", "/Users/diegoeduardo/Desktop/GitHub/PyFRET/dyes/traj/CY5.dcd") 

fret = FRETraj(ref, donor, acceptor)

#print(list(set(fret.ref.select_atoms("resname U").resids)))
print("Creating object...")
ref_frames = np.arange(0, fret.ref.trajectory.n_frames, fret.ref.trajectory.n_frames//100)
print("Done creating object.")
# total_frames = fret.overlap_dyes(6, 42, "donor", "acceptor", ref_frames=ref_frames, prefix="src/more_tests/testing")

# for allowed_frames in total_frames:
# 	if allowed_frames:
# 		print(len(allowed_frames))

# print("Starting computation...")
# print("Computing results_iso...")
# results_iso = fret.compute_efficiency(6, 42, 52., regime='isotropic', burst_averaging_on=False, ref_frames=ref_frames, verbose=True, prefix="src/more_tests/testing")
# save_results(results_iso, "results_iso")
# print("Done.")
# print("Computing results_dynamic...")
# results_dynamic = fret.compute_efficiency(6, 42, 52., regime='dynamic', burst_averaging_on=False, ref_frames=ref_frames, verbose=True, prefix="src/more_tests/testing")
# save_results(results_dynamic, "results_dynamic")
# print("Done.")
# print("Computing results_static...")
# results_static = fret.compute_efficiency(6, 42, 52., regime='static', burst_averaging_on=False, ref_frames=ref_frames, verbose=True, prefix="src/more_tests/testing")
# save_results(results_static, "results_static")
# print("Done.")
# print("Computing results_iso_burst...")
# results_iso_burst = fret.compute_efficiency(6, 42, 52., regime='isotropic', burst_averaging_on=True, ref_frames=ref_frames, verbose=True, prefix="src/more_tests/testing")
# save_results(results_iso_burst, "results_iso_burst")
# print("Done.")
# print("Computing results_dynamic_burst...")
# results_dynamic_burst = fret.compute_efficiency(6, 42, 52., regime='dynamic', burst_averaging_on=True, ref_frames=ref_frames, verbose=True, prefix="src/more_tests/testing")
# save_results(results_dynamic_burst, "results_dynamic_burst")
# print("Done.")
# print("Computing results_static_burst...")
# results_static_burst = fret.compute_efficiency(6, 42, 52., regime='static', burst_averaging_on=True, ref_frames=ref_frames, verbose=True, prefix="src/more_tests/testing")
# save_results(results_static_burst, "results_static_burst")
# print("Done with computation.")

print("Starting computation...")
# print("Computing results_iso...")
# results_iso = fret.compute_efficiency(6, 42, 52., regime='isotropic', burst_averaging_on=False, ref_frames=ref_frames, verbose=True, prefix="src/more_tests/testing")
# save_results(results_iso, "results_iso")
# print("Done.")
print("Computing results_dynamic...")
results_dynamic = fret.compute_efficiency(865, 353, 52., regime='dynamic', burst_averaging_on=False, ref_frames=ref_frames, verbose=True, prefix="../test/")
save_results(results_dynamic, "results_dynamic")
print("Done.")
# print("Computing results_static...")
# results_static = fret.compute_efficiency(6, 42, 52., regime='static', burst_averaging_on=False, ref_frames=ref_frames, verbose=True, prefix="src/more_tests/testing")
# save_results(results_static, "results_static")
# print("Done.")
# print("Computing results_iso_burst...")
# results_iso_burst = fret.compute_efficiency(6, 42, 52., regime='isotropic', burst_averaging_on=True, ref_frames=ref_frames, verbose=True, prefix="src/more_tests/testing")
# save_results(results_iso_burst, "results_iso_burst")
# print("Done.")
print("Computing results_dynamic_burst...")
results_dynamic_burst = fret.compute_efficiency(6, 42, 52., regime='dynamic', burst_averaging_on=True, ref_frames=ref_frames, verbose=True, prefix="src/more_tests/testing")
save_results(results_dynamic_burst, "results_dynamic_burst")
print("Done.")
# print("Computing results_static_burst...")
# results_static_burst = fret.compute_efficiency(6, 42, 52., regime='static', burst_averaging_on=True, ref_frames=ref_frames, verbose=True, prefix="src/more_tests/testing")
# save_results(results_static_burst, "results_static_burst")
# print("Done with computation.")







