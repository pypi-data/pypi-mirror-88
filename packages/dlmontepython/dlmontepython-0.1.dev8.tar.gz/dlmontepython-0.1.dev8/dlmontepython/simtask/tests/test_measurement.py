"""Tests for Measurement class"""

import unittest
import os
import shutil

import numpy as np

import dlmontepython.simtask.dlmonteinterface as dlmonteinterface
import dlmontepython.simtask.measurement as measurement
import dlmontepython.simtask.analysis as analysis
import dlmontepython.simtask.task as task


class MeasurementTestCase(unittest.TestCase):

    """Tests for Measurement class"""

    def test_measurement_sweep(self):

        """Tests for MeasurementSweep class using DL_MONTE as the simulation
        engine. Note that this test requires DL_MONTE to be installed on the
        local system, and the PATH environment variable to be set to include 
        the path to the serial DL_MONTE executable 'DLMONTE-SRL.X'. 
        WARNING: This overwrites the 'measurement_test_data_output' directory
        if it exists."""

        # This test runs GCMC simulations for the Lennard-Jones system in
        # a sweep over various thermodynamic activities to obtain the number
        # of molecules in the system, nmol, vs. activity, and compare the 
        # results to benchmark.

        # Link to serial DL_MONTE executable, which must be visible via the
        # PATH environment variable.
        interface = dlmonteinterface.DLMonteInterface("DLMONTE-SRL.X")

        nmol_obs = task.Observable( ("nmol",0) )
        observables = [ nmol_obs ]
        
        # System volume used in the GCMC simulations (used to calculate nmol precision threshold)
        volume=8.0**3
        # Threshold density precision at which to stop simulations at a given activity
        density_prec = 0.02
        
        # ... corresponding threshold nmol precision 
        precisions= { nmol_obs : density_prec*volume }
        
        # Use the subdirectory 'measurement_test_data' relative to the directory
        # containing this script as the directory containing the input files
        inputdir = os.path.join( os.path.dirname(__file__), "measurement_test_data")
        measurement_template = measurement.Measurement(interface, observables, precisions=precisions,
                                                       inputdir=inputdir)
        
        # Thermodynamic activities to consider in sweep
        activities = np.logspace(-3.0, 1.3333333333, 5)  
        
        # Set the name of the directory for the output files, and delete any old
        # versions of it before running the measurement sweep
        # Use the subdirectory 'measurement_test_data_output.tmp' relative to the directory
        # containing this script as the directory.
        outputdir = os.path.join( os.path.dirname(__file__), "measurement_test_data_output.tmp")
        if os.path.isdir(outputdir):
            shutil.rmtree(outputdir)


        # Run the calculations
        sweep = measurement.MeasurementSweep(param="molchempot", paramvalues=activities, 
                                             measurement_template=measurement_template, 
                                             outputdir=outputdir)        
        sweep.run()

        # Compare the results to a benchmark
        nmoldata_benchmark = np.array([[0.001,                0.518796992481203, 0.05214123250998071],
                                       [0.012115276586053412, 6.167919799498747, 0.17776376455383364],
                                       [0.146779926756574,    63.725,            0.5257691508637607 ],
                                       [1.778279409936555,    248.2284946236559, 2.5626209993127773 ],
                                       [21.544346898665243,   366.7758620689655, 9.621020162479562  ]])


        nmoldata = np.loadtxt( os.path.join(outputdir,"nmol_0_sweep.dat"))

        np.testing.assert_almost_equal( nmoldata, nmoldata_benchmark, decimal=10 )        


if __name__ == '__main__':

    unittest.main()
