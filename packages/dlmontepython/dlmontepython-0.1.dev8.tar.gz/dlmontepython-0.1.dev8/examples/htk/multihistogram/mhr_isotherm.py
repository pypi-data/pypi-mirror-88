import dlmontepython.htk.sources.dlmonte as dlmonte
import dlmontepython.htk.multihistogram as multihistogram
import numpy as np

# List of directories containing DL_MONTE simulation data
# at different chemical potentials or activities. (These
# may be in a tar archive in the current directory which
# should be extracted before invoking this script).
simdirs = [ "param_0.03337326996032608",
            "param_0.035673993347252395",
            "param_0.038133326547045175" ]

# List of chemical potentials to calculate density at using
# reweighting
mu_target = np.linspace(-5.3,-4.8,20)

# Data and thermodynamic parameters for all simulations.
# kT[n] will be the temperature of simulation 'n' , and
# similarly for mu. E[n][i] will be the energy of
# simulation 'n' at timestep 'i', and similarly for N
# and rho.
kT, mu, E, N, rho = ([] for i in range(0,5))

# Import data from simulation directories, using classes in
# htk package to make importing easier.
for simdir in simdirs:

    dlminput = dlmonte.DLMonteInput.from_directory(simdir)
    dlmoutput = dlmonte.DLMonteOutput.load(simdir)
    
    kT_sim = dlminput.control.get_temperature()
    V_sim = dlminput.config.volume()
    activity_sim = dlminput.control.get_molecule_gcmc_potential('lj')
    mu_sim =  np.log(activity_sim)*kT_sim

    kT.append(kT_sim)
    mu.append(mu_sim)

    E_sim = dlmoutput.yamldata.time_series("energy")
    N_sim = dlmoutput.yamldata.time_series("nmol")
    N_sim = np.reshape(N_sim,len(N_sim))
    rho_sim = N_sim / V_sim

    E.append(E_sim)
    N.append(N_sim)
    rho.append(rho_sim)


# Perform the reweighting and output
for mu_new in  np.linspace(-5.2,-4.8,20):
    
    rho_new = multihistogram.reweight_observable_muvt(
                kT, mu, E, N, rho, kT[0], mu_new)

    print(mu_new, rho_new)
    
