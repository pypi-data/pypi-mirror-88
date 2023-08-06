"""Test multihistogram module"""

import unittest
import numpy as np
import os

import dlmontepython.htk.sources.dlmonte as dlmonte
import dlmontepython.htk.multihistogram as multihistogram


class TestMultihistogram(unittest.TestCase):

    """Tests for the multihistogram module"""

    def test_reweight_observable_muvt(self):

        """Tests for reweight_observable_muvt. This test also covers functionality in the
        dlmonte module."""

        # List of directories containing muVT simulation data from DL_MONTE
        simdirs = [ os.path.join( os.path.dirname(__file__),"multihistogram_test_data","param_0.03337326996032608","sim_1"),
                    os.path.join( os.path.dirname(__file__),"multihistogram_test_data","param_0.035673993347252395","sim_1"),
                    os.path.join( os.path.dirname(__file__),"multihistogram_test_data","param_0.038133326547045175","sim_1")]

        kT, mu, E, N, rho = ([] for i in range(0,5))

        # Import data from simulation directories
        for simdir in simdirs:
        
            dlminput = dlmonte.DLMonteInput.from_directory(simdir)
            dlmoutput = dlmonte.DLMonteOutput.load(simdir)
            
            kT_sim = dlminput.control.temperature
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
        

        # Reweight the density to a new chemical potential and check the
        # result against a benchmark
        mu_new = -5.2
        rho_new = multihistogram.reweight_observable_muvt(
                        kT, mu, E, N, rho, kT[0], mu_new)
        rho_benchmark = 0.03721273390154083
        np.testing.assert_almost_equal( rho_new, rho_benchmark, decimal=10 )

    


if __name__ == '__main__':

    unittest.main()
