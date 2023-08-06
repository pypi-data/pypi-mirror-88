"""Tests for 'analysis' module"""

import unittest
import numpy as np
import numpy.random as random
import sys

import dlmontepython.simtask.analysis as analysis


class AnalysisTestCase(unittest.TestCase):

    """Tests for 'analysis' module"""


    def test_block_averages(self):

        """Tests for 'block_averages' function"""

        data = ( -7.28820535515628000E+01,
                 -3.18863042402020000E+01,
                  2.19403616931461000E+01,
                 -6.40900178434064000E+01,
                 -5.95505218037951000E+01,
                 -7.39927727273677000E+00,
                 -2.02095006700651000E+01,
                 -9.67146259210056000E+01,
                 -4.88034291757944000E+01,
                 -1.34088503173081000E+01  )

        avgs_for_3 = ( -2.76093320328729000E+01,
                       -4.36799389733127000E+01,
                       -5.52425185889550000E+01  )

        avgs_rev_3 = ( -5.29756351380360000E+01,
                       -2.90530999155323000E+01,
                       -2.46786534634874000E+01  )

        np.testing.assert_almost_equal( analysis.block_averages(data,1), data, decimal=10 )
        np.testing.assert_almost_equal( analysis.block_averages(data,3), avgs_for_3, decimal=10 )
        np.testing.assert_almost_equal( analysis.block_averages(data,3,reverse=True), avgs_rev_3, decimal=10 )

        # An empty array should be returned if the block size is larger than the size of the data set
        self.assertEqual( len(analysis.block_averages(data,11)), 0 )




    def test_autocorrelation(self):

        """Tests for 'autocorrelation' function"""

        # Some model data for which the properties can easily be calculated by hand...

        data = (  1.2345678, -1.2345678,
                  1.2345678, -1.2345678,
                  1.2345678, -1.2345678,
                  1.2345678, -1.2345678,
                  1.2345678, -1.2345678  )

        # 'data' yields the following autocorrelation function
        autocorr = ( 1.0, -1.0, 
                     1.0, -1.0, 
                     1.0, -1.0, 
                     1.0, -1.0, 
                     1.0, -1.0  )

        np.testing.assert_almost_equal( analysis.autocorrelation(data), autocorr, decimal=10 )

        # An arbitrary shift to the data should not affect the correlation

        shift = np.ones(len(data)) * 9.01234567

        np.testing.assert_almost_equal( analysis.autocorrelation(data+shift), autocorr, decimal=10 )


        # A single element array with NaN should be returned if the data set has one or zero elements

        np.testing.assert_array_equal( analysis.autocorrelation([5.0]),  np.asarray([ float('NaN') ]) )
        np.testing.assert_array_equal( analysis.autocorrelation([]),  np.asarray([ float('NaN') ]) )


        # Some weakly correlated data I generated in a spreadsheet and calculated the properties of
        # manually...

        data = ( -2.7890565039021,  -2.06649575451978,
                 -1.78184769112837, -1.29594863845756,
                 -0.63966875460567,  0.03057347130564,
                 0.890537757208008,  1.8678791267548,
                 2.40459853350332,   3.37942845384171  )

        autocorr = (  1.0,                0.769579759141887,  
                      0.537686219265065,  0.206782048856929,  
                     -0.159860718357574, -0.542897127624209,
                     -0.967043026224385, -1.39183642673971,
                     -1.76426202271555,  -2.42932654958174   )

        np.testing.assert_almost_equal( analysis.autocorrelation(data), autocorr, decimal=10 )



    def test_inefficiency_autocorrelation_time(self):

        """Tests for 'inefficiency' and 'autocorrelation_time' functions"""


        # Some model data for which the properties can easily be calculated by hand...

        data = (  1.2345678, -1.2345678,
                  1.2345678, -1.2345678,
                  1.2345678, -1.2345678,
                  1.2345678, -1.2345678,
                  1.2345678, -1.2345678  )

        # 'data' yields the following autocorrelation function and inefficiency
        autocorr = ( 1.0, -1.0, 
                     1.0, -1.0, 
                     1.0, -1.0, 
                     1.0, -1.0, 
                     1.0, -1.0  )

        inefficiency = 1.0
        autocorrelation_time = 0.0

        np.testing.assert_almost_equal( analysis.inefficiency(data), inefficiency, decimal=10 )
        assert analysis.autocorrelation_time(data) == 0.0


        # Some weakly correlated data I generated in a spreadsheet and calculated the properties of
        # manually...

        data = ( -2.7890565039021,  -2.06649575451978,
                 -1.78184769112837, -1.29594863845756,
                 -0.63966875460567,  0.03057347130564,
                 0.890537757208008,  1.8678791267548,
                 2.40459853350332,   3.37942845384171  )

        autocorr = (  1.0,                0.769579759141887,  
                      0.537686219265065,  0.206782048856929,  
                     -0.159860718357574, -0.542897127624209,
                     -0.967043026224385, -1.39183642673971,
                     -1.76426202271555,  -2.42932654958174   )

        inefficiency = 4.02809605452776
        autocorrelation_time = 1.97196910093235

        np.testing.assert_almost_equal( analysis.inefficiency(data), inefficiency, decimal=10 )
        np.testing.assert_almost_equal( analysis.autocorrelation_time(data), autocorrelation_time, decimal=10 )


        # A single element array with NaN should be returned by 'inefficiency' if the data
        # set has one or zero elements

        np.testing.assert_array_equal( analysis.inefficiency([5.0]),  np.asarray([ float('NaN') ]) )
        np.testing.assert_array_equal( analysis.inefficiency([]),  np.asarray([ float('NaN') ]) )


        # NaN should be returned by 'autocorrelation_time' if the data set has one or zero
        # elements
        np.testing.assert_equal(analysis.autocorrelation_time([5.0]), float('NaN'))
        np.testing.assert_equal(analysis.autocorrelation_time([]), float('NaN'))



    def test_standard_error(self):

        # Some weakly correlated data I generated in a spreadsheet and calculated the properties of
        # manually...

        data = ( -2.7890565039021,  -2.06649575451978,
                 -1.78184769112837, -1.29594863845756,
                 -0.63966875460567,  0.03057347130564,
                 0.890537757208008,  1.8678791267548,
                 2.40459853350332,   3.37942845384171  )

        autocorr = (  1.0,                0.769579759141887,  
                      0.537686219265065,  0.206782048856929,  
                     -0.159860718357574, -0.542897127624209,
                     -0.967043026224385, -1.39183642673971,
                     -1.76426202271555,  -2.42932654958174   )

        inefficiency = 4.02809605452776

        # Default args: blocksize=1, reverse=False, assume_independent=False
        mean, stderr = analysis.standard_error(data)
        np.testing.assert_almost_equal( mean, np.mean(data), decimal=10 )
        np.testing.assert_almost_equal( stderr, np.sqrt(inefficiency*np.var(data)/len(data)), decimal=10 )

        mean, stderr = analysis.standard_error(data,reverse=False, assume_independent=True)
        np.testing.assert_almost_equal( mean, np.mean(data), decimal=10 )
        np.testing.assert_almost_equal( stderr, np.sqrt(np.var(data)/len(data)), decimal=10 )

        mean, stderr = analysis.standard_error(data,reverse=True, assume_independent=True)
        np.testing.assert_almost_equal( mean, np.mean(data), decimal=10 )
        np.testing.assert_almost_equal( stderr, np.sqrt(np.var(data)/len(data)), decimal=10 )


        # Some data I've calculated block averages for manually using block size of 3...

        data = ( -7.28820535515628000E+01,
                 -3.18863042402020000E+01,
                  2.19403616931461000E+01,
                 -6.40900178434064000E+01,
                 -5.95505218037951000E+01,
                 -7.39927727273677000E+00,
                 -2.02095006700651000E+01,
                 -9.67146259210056000E+01,
                 -4.88034291757944000E+01,
                 -1.34088503173081000E+01  )

        avgs_for_3 = ( -2.76093320328729000E+01,
                       -4.36799389733127000E+01,
                       -5.52425185889550000E+01  )

        avgs_rev_3 = ( -5.29756351380360000E+01,
                       -2.90530999155323000E+01,
                       -2.46786534634874000E+01  )

        mean, stderr = analysis.standard_error(data,blocksize=3,reverse=False, assume_independent=True)
        np.testing.assert_almost_equal( mean, np.mean(avgs_for_3), decimal=10 )
        np.testing.assert_almost_equal( stderr, np.sqrt(np.var(avgs_for_3)/len(avgs_for_3)), decimal=10 )

        mean, stderr = analysis.standard_error(data,blocksize=3,reverse=True, assume_independent=True)
        np.testing.assert_almost_equal( mean, np.mean(avgs_rev_3), decimal=10 )
        np.testing.assert_almost_equal( stderr, np.sqrt(np.var(avgs_rev_3)/len(avgs_for_3)), decimal=10 )

        mean, stderr = analysis.standard_error(data,blocksize=3,reverse=True, assume_independent=False)
        np.testing.assert_almost_equal( mean, np.mean(avgs_rev_3), decimal=10 )
        np.testing.assert_almost_equal( stderr, np.sqrt(analysis.inefficiency(avgs_rev_3)*np.var(avgs_rev_3)/len(avgs_for_3)), decimal=10 )



    def test_equilibration_test(self):
        
        # Initial size of test data sets
        N=1000
        
        # Time array used for some tests.
        t = np.linspace(0,N,N)
        
        
        # Test 0 - Data is a constant 
        y = np.ones(N)*1.234567
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == False
                
        # Test 1 - Flat line with normally distributed noise
        random.seed(0)
        mu=5.0
        sigma=1.0
        y = mu  + random.normal(0.0,sigma,N)
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == True
        
        # Test 2 - Linear increase with normally distributed noise
        random.seed(0)
        A= 0.01
        mu=5.0
        tau=10.0
        sigma=1.0
        y = A*(t-0.5*N) + mu  + random.normal(0.0,sigma,N)
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == False
        
        # Test 3 - Linear decrease with normally distributed noise
        random.seed(0)
        A= -0.01
        mu=5.0
        tau=10.0
        sigma=1.0
        y = A*(t-0.5*N) + mu  + random.normal(0.0,sigma,N)
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == False
        
        # Test 4 - Shallow linear increase with normally distributed noise
        random.seed(0)
        A= 0.001
        mu=5.0
        tau=10.0
        sigma=1.0
        y = A*(t-0.5*N) + mu  + random.normal(0.0,sigma,N)
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == False
        
        # Test 4 - Insignificant shallow linear decrease with normally distributed noise
        random.seed(0)
        A= 0.0001
        mu=5.0
        tau=10.0
        sigma=1.0
        y = A*(t-0.5*N) + mu  + random.normal(0.0,sigma,N)
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == True
        
        # Test 5 - Exponential decay decrease with normally distributed noise
        random.seed(0)
        A= 5.0
        mu=5.0
        tau=100.0
        sigma=1.0
        y = A*np.exp(-t/tau) + mu  + random.normal(0.0,sigma,N)
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == False
        
        
        # Test 6 - Exponential decay increase with normally distributed noise
        random.seed(0)
        A= -5.0
        mu=5.0
        tau=100.0
        sigma=1.0
        y = A*np.exp(-t/tau) + mu  + random.normal(0.0,sigma,N)
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == False
        
        # Test 6 - Shallow exponential decay decrease with normally distributed noise
        random.seed(0)
        A= 1.0
        mu=5.0
        tau=100.0
        sigma=1.0
        y = A*np.exp(-t/tau) + mu  + random.normal(0.0,sigma,N)
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == False
        
        # Test 7 - Insignificant exponential decay increase with normally distributed noise
        random.seed(0)
        A= -0.1
        mu=5.0
        tau=100.0
        sigma=1.0
        y = A*np.exp(-t/tau) + mu  + random.normal(0.0,sigma,N)
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == True
        
        # Test 8 - Bounded random walk
        random.seed(0)
        N=10000
        sigma=1.0
        wall = 10
        y = np.zeros(N)
        for i in range(1,N):
            y[i] = y[i-1] + random.normal(0.0,sigma,1)
            if y[i] > wall:
                y[i] = wall
            if y[i] < -wall:
                y[i] = -wall
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == True
        
        
        # Test 9 - Biased bounded random walk slow equilibration
        random.seed(0)
        N=10000
        sigma=0.1
        bias = 0.1
        wall = 10
        y = np.zeros(N)
        for i in range(1,N):
            y[i] = y[i-1] + random.normal(bias,sigma,1)
            if y[i] > wall:
                y[i] = wall
            if y[i] < -wall:
                y[i] = -wall
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == False
        
        # Test 10 - Biased bounded random walk fast equilibration
        random.seed(0)
        N=10000
        sigma=1.0
        bias = 1.0
        wall = 10
        y = np.zeros(N)
        for i in range(1,N):
            y[i] = y[i-1] + random.normal(bias,sigma,1)
            if y[i] > wall:
                y[i] = wall
            if y[i] < -wall:
                y[i] = -wall
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == True
        
        # Test 11 - Bounded random walk with time-dependent equilibration wall
        random.seed(0)
        N=10000
        sigma=1.0
        A=10.0
        wall = 5.0
        tau=1000.0
        y = np.zeros(N)
        for i in range(1,N):
            wallcentre = A*(1.0-np.exp(-i/tau))
            y[i] = y[i-1] + random.normal(0.0,sigma,1)
            if y[i] > wallcentre + wall:
                y[i] = wallcentre + wall
            if y[i] < wallcentre - wall:
                y[i] = wallcentre - wall
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == False
        
        # Test 12 - Bounded random walk with shallow time-dependent equilibration wall
        random.seed(0)
        N=10000
        sigma=1.0
        A=1.0
        wall = 5.0
        tau=1000.0
        y = np.zeros(N)
        for i in range(1,N):
            wallcentre = A*(1.0-np.exp(-i/tau))
            y[i] = y[i-1] + random.normal(0.0,sigma,1)
            if y[i] > wallcentre + wall:
                y[i] = wallcentre + wall
            if y[i] < wallcentre - wall:
                y[i] = wallcentre - wall
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == False
        
        # Test 13 - Bounded random walk with insignificant time-dependent equilibration wall
        random.seed(0)
        N=10000
        sigma=1.0
        A=0.1
        wall = 5.0
        tau=1000.0
        y = np.zeros(N)
        for i in range(1,N):
            wallcentre = A*(1.0-np.exp(-i/tau))
            y[i] = y[i-1] + random.normal(0.0,sigma,1)
            if y[i] > wallcentre + wall:
                y[i] = wallcentre + wall
            if y[i] < wallcentre - wall:
                y[i] = wallcentre - wall
        flatslice, slicepos = analysis.equilibration_test(y, checktimes=[0.0]) 
        assert flatslice == True



if __name__ == '__main__':

    #unittest.main()
    t = AnalysisTestCase()
    t.test_standard_error()
