r"""
.. moduleauthor:: Tom L. Underwood

This module contains functions for performing multiple histogram reweighting (MHR).
We consider probability distributions of the form

:math:`p_i=\frac{1}{Z}\exp(\mathbf{b}\cdot\mathbf{X}_i)`,

where :math:`p_i` is the probability of the system being in state :math:`i`;
:math:`X_i` is a vector containing the relevant thermodynamic generalised displacements
(e.g. energy, volume) for state :math:`i`; :math:`\mathbf{b}` is a vector
containing the relevant generalised forces (e.g. beta and pressure if the
displacements are energy and volume); and 

:math:`Z = \sum_i\exp(\mathbf{b}\cdot\mathbf{X}_i)`

is the partition function for the system. MHR can be used to pool data sampled
from multiple systems with different :math:`\mathbf{b}` and biasings and use the
data  make predictions about another :math:`\mathbf{b}`. We assume that there 
is data from :math:`R` different :math:`\mathbf{b}`, where the probability
distribution for the :math:`n` th :math:`\mathbf{b}`, :math:`\mathbf{b}^{(n)}`,
is 

:math:`p^{(n)}_i = \frac{1}{Z^{(n)}}\exp(\mathbf{b}^{(n)}\cdot\mathbf{X}_i)`

The expected value of an observable at a 'new' math:`\mathbf{b}`, :math:`\mathbf{b}'`, 
using the data from :math:`\mathbf{b}^{(1)},\mathbf{b}^{(2)},\dotsc`, can be obtained via

:math:`\langle O'\rangle = \frac{ \sum_{n=1}^{R}\sum_{i=1}^{N_n}O_{ni}\exp( (\mathbf{b}'-\mathbf{b}^{(n)})\cdot\mathbf{X}_{ni}-F^{(n)} ) }{ \sum_{n=1}^{R}\sum_{i=1}^{N_n}\exp( (\mathbf{b}'-\mathbf{b}^{(n)})\cdot\mathbf{X}_{ni}-F^{(n)} )}`,

where :math:`N_n` is the number of data points for the :math:`\mathbf{b}^{(n)}`;
:math:`O_{ni}` is the value of the observable of interest for the :math:`i` th 
data point corresponding to :math:`\mathbf{b}^{(n)}`; :math:`\mathbf{X}_{ni}`
is the generalised displacement and bias for the :math:`i` th 
data point corresponding to :math:`\mathbf{b}^{(n)}`; and :math:`F^{(n)}\equiv-\ln(Z^{(n)})`
is the 'free energy' associated with the :math:`n` th Hamiltonian. 
To apply the above equation, the free energies :math:`F^{(n)}` must be known. 
These can be obtained using

:math:`\exp(-F^{(n)}) = \sum_{p=1}^{R}\sum_{i=1}^{N_p}\frac{ \exp(\mathbf{b}^{(n)}\cdot\mathbf{X}_{pi}) }{\sum_{q=1}^{R}\exp(\mathbf{b}^{(q)}\cdot\mathbf{X}_{pi}+F^{(q)})N_q}`,

which must be solved using an iterative procedure.


"""

import numpy as np




def free_energies(b, X, nmaxit=20, weights=None):

    r"""
    General function to calculate the relative free energies for MHR

    General function to calculate the relative free energies :math:`F^{(1)},F^{(2)}\dotsc` 
    for MHR from simulation data. An iterative proccedure is used to solve the relevant
    equation.

    Arguments:
        b (2 dimensional array): Values of :math:`\mathbf{b}^{(n)}`. `b[n]` is :math:`\mathbf{b}^{(n)}`.
          `b[n][i]` is the `i` th displacement for :math:`\mathbf{b}^{(n)}`.

        X (list of 3-dimensional arrays): Generalised displacements data for various :math:`\mathbf{b}^{(n)}`.
          `X[n]` is the data pertaining to :math:`\mathbf{b}^{(n)}`, and is an array. `X[n][i,k]` is the 
          `k` th generalised displacement for the `i` th data point in the data pertaining to 
          :math:`\mathbf{b}^{(n)}`.

        nmaxit (int) : Number of iterations to perform to solve the equation.

        weights (list of arrays): Weights to be applied to each data point in `X`;
          The `i` th data point pertaining to :math:`\mathbf{b}^{(n)}` will be counted `weight[n][i]` 
          times. If `None` then all data points are counted once.

    Returns:
        array: Free energies :math:`F^{(1)},F^{(2)},\dotsc` corresponding to :math:`\mathbf{b}^{(1)},\mathbf{b}^{(1)},\dotsc`;
          `F[n]` is the free energy corresopnding to `b[n]`

    """

    # Relevant equation:
    # \exp(-F^{(n)}) = \sum_{p=1}^{R}\sum_{i=1}^{N_p}\frac{ \exp(\mathbf{b}^{(n)}\cdot\mathbf{X}_{pi}) }{\sum_{q=1}^{R}\exp(\mathbf{b}^{(q)}\cdot\mathbf{X}_{pi}+F^{(q)})N_q}

    
    nrun = len(b)        
    assert len(X) == nrun, "Check 'b' and 'X' have matching lengths"
                      
    # Free energies for each data set
    fold = np.ones(nrun)
    f = np.zeros(nrun)

    # Number of data points in each data set
    ndata = np.zeros(nrun, dtype = 'int')
    for irun1 in range(nrun):
        ndata[irun1] = X[irun1].shape[0]

        
    for n in range(nmaxit):
        
        # Begin iteration
        for i in range(nrun):
            f[i] = 0.0
        
            # f = free_energy(...)
            for irun1 in range(nrun):
                for idata in range(ndata[irun1]):
                    # Accumulate the denominator
                    sum = 0.0
                    for irun2 in range(nrun):
                        arg = np.dot(b[irun2,:],X[irun1][idata,:]) + fold[irun2]       
                        sum += 1.0*ndata[irun2]*np.exp(arg)

                    # 'sum' now the denominator in the equation given above
                    # Calculate the numerator and add the term to the sum
                    arg = np.dot(b[irun1,:],X[irun1][idata,:])
                    if weights == None:
                        f[i] += (1.0/sum)*np.exp(arg)
                    else:
                        f[i] += (weights[irun1][idata]/sum)*np.exp(arg)

        #TU: 'f' is now the RHS of (1)
        fold[:] = -np.log(f[:])

        #TU: 'fold' is now f_n in (1)

        #TU: Shift the free energies at the end of each iteration so 
        #    that they are as close as possible to 0; to prevent
        #    overflows and underflows
        fold = fold - fold.min()
        
    return fold




def reweight_observable(b, X, obs, bnew, fe=None, weights=None):

    r"""
    General function to reweight an observable using MHR.

    General function to reweight an observable using MHR.

    Arguments:
        b (2 dimensional array): Values of :math:`\mathbf{b}^{(n)}`. `b[n]` is :math:`\mathbf{b}^{(n)}`.
          `b[n][i]` is the `i` th displacement for :math:`\mathbf{b}^{(n)}`.

        X (list of 3-dimensional arrays): Generalised displacements data for various :math:`\mathbf{b}^{(n)}`.
          `X[n]` is the data pertaining to :math:`\mathbf{b}^{(n)}`, and is an array. `X[n][i][k]` is the 
          `k` th generalised displacement for the `i` th data point in the data pertaining to 
          :math:`\mathbf{b}^{(n)}`.

        obs (list of 2-dimensional arrays): Values of the observables: `obs[n][i]` is the observable
           corresponding to the `i` th data point at :math:`\mathbf{b}^{(n)}`, i.e. :math:`O_{ni}`

        bnew (array): The set of generalised displacements, :math:`\mathbf{b}'`, to be reweighted to.
           `bnew[i]` is the `i` th displacement for :math:`\mathbf{b}'`

        fe (array) (optional): Free energies :math:`F^{(1)},F^{(2)},\dotsc` corresponding to 
          :math:`\mathbf{b}^{(1)},\mathbf{b}^{(1)},\dotsc`; `F[n]` is the free energy corresopnding 
          to `b[n]`. If this is absent then it is calculated using the `free energies` function

        weights (list of arrays): Weights to be applied to each data point in `X`;
          The `i` th data point pertaining to :math:`\mathbf{b}^{(n)}` will be counted `weight[n][i]` 
          times. If `None` then all data points are counted once.

    Returns:
        float: The value of the observable at :math:`\mathbf{b}'` calculated using MHR.

    """

    # Relevant equation:
    # `\langle O'\rangle = \frac{ \sum_{n=1}^{R}\sum_{i=1}^{N_n}O_{ni}\exp( (\mathbf{b}'-\mathbf{b}^{(n)})\cdot\mathbf{X}_{ni}-F^{(n)} ) }{ \sum_{n=1}^{R}\sum_{i=1}^{N_n}\exp( (\mathbf{b}'-\mathbf{b}^{(n)})\cdot\mathbf{X}_{ni}-F^{(n)} )}`,

    
    nrun = len(b)
    assert len(X) == nrun, "Check 'X' and 'b' have matching lengths"
    assert len(obs) == nrun, "Check 'obs' and 'b' have matching lengths"

    ndata = np.zeros(nrun, dtype = 'int')

    # If free energies are specified then use them; if not then calculate them from scratch
    # using default parameters
    if fe == None:
        fe = free_energies(b, X, weights=weights)
    
    
    for irun1 in range(nrun):
        assert len(X[irun1]) == len(obs[irun1]), "Check 'X' and 'obs' have same shape"
        # Set ndata to the number of energy data points in 'e[i,:]' - for run 'i'
        ndata[irun1] = X[irun1].shape[0]

    # Calculate denominator in the equation
    denom = 0.0
    for irun1 in range(nrun):
        for idata in range(ndata[irun1]):
            arg = np.dot((bnew[:]-b[irun1,:]),X[irun1][idata,:]) - fe[irun1]
            if weights == None:
                denom += np.exp(arg)
            else:
                denom += weights[irun1][idata]*np.exp(arg)
            
    # Calculate the value
    robs = 0.0
    for irun1 in range(nrun):
        for idata in range(ndata[irun1]):
            arg = np.dot((bnew[:]-b[irun1,:]),X[irun1][idata,:]) - fe[irun1]
            if weights == None:
                robs += (1.0/denom)*np.exp(arg)*obs[irun1][idata]
            else:
                robs += (weights[irun1][idata]/denom)*np.exp(arg)*obs[irun1][idata]
            
    return robs






def reweight_observable_nvt(kT, E, obs, kT_new, weights=None):

    r"""
    Calculate an observable in the NVT ensemble at a new temperature using MHR.

    Calculate an observable in the NVT ensemble at a new temperature using MHR.

    Arguments:
        kT (array): Values of :math:`kT` for the various simulations.

        E (list of arrays): `E[n]` is an array containing the energies for the `n` th simulation;
          `E[n][i]` is the energy for the `i` th data point.

        obs (list of arrays): `obs[n][i]` is the observable corresponding to the `i` th data point
           in the `n` th simulation.

        kT_new (array): The :math:`kT` to be reweighted to

        weights (list of arrays): Weights to be applied to each data point in `X`;
          The `i` th data point pertaining to :math:`\mathbf{b}^{(n)}` will be counted `weight[n][i]` 
          times. If `None` then all data points are counted once.

    Returns:
        float: The value of the observable at `kT_new` calculated using MHR.

    """
    
    nrun = len(kT)
    
    b = []
    for n in range(nrun):
        b.append([ -1.0/kT[n] ])
    b = np.asarray(b)
    
    X = []
    for n in range(nrun):
        Xn = np.zeros( (len(E[n]),1) )
        Xn[:,0] = E[n]
        X.append(Xn)

    obs2 = []
    for n in range(nrun):
        obs2n = np.zeros( (len(obs[n]),1) )
        obs2n[:,0] = obs[n]
        obs2.append(Xn)

    bnew = np.asarray([-1.0/kT_new])
    
    return reweight_observable(b, X, obs, bnew, weights=weights)






def reweight_observable_muvt(kT, mu, E, N, obs, kT_new, mu_new, weights=None):

    r"""
    Calculate an observable in the muVT ensemble at a new temperature and/or chemical potential
    using MHR.

    Calculate an observable in the muVT ensemble at a new temperature and/or chemical potential
    using MHR.

    Arguments:
        kT (array): Values of :math:`kT` for the various simulations.

        mu (array): Values of :math:`\mu` for the various simulations.

        E (list of arrays): `E[n]` is an array containing the energies for the `n` th simulation;
          `E[n][i]` is the energy for the `i` th data point.

        N (list of arrays): `N[n]` is an array containing the number of particles for the `n` th simulation;
          `N[n][i]` is the number of particles for the `i` th data point.

        obs (list of arrays): `obs[n][i]` is the observable corresponding to the `i` th data point
           in the `n` th simulation.

        kT_new (array): The :math:`kT` to be reweighted to

        mu_new (array): The new :math:`\mu` to be reweighted to

        weights (list of arrays): Weights to be applied to each data point in `X`;
          The `i` th data point pertaining to :math:`\mathbf{b}^{(n)}` will be counted `weight[n][i]` 
          times. If `None` then all data points are counted once.

    Returns:
        float: The value of the observable at `kT_new` and `mu_new` calculated using MHR.

    """
    
    nrun = len(kT)
    
    b = []
    for n in range(nrun):
        b.append([ -1.0/kT[n], mu[n]/kT[n] ])
    b = np.asarray(b)
    
    X = []
    for n in range(nrun):
        Xn = np.zeros( (len(E[n]),2) )
        Xn[:,0] = E[n]
        Xn[:,1] = N[n]
        X.append(Xn)

    obs2 = []
    for n in range(nrun):
        obs2n = np.zeros( (len(obs[n]),1) )
        obs2n[:,0] = obs[n]
        obs2.append(Xn)

    bnew = np.asarray([-1.0/kT_new, mu_new/kT_new])
    
    return reweight_observable(b, X, obs, bnew, weights=weights)




def reweight_observable_npt(kT, P, E, V, obs, kT_new, P_new, weights=None):

    r"""
    Calculate an observable in the NPT ensemble at a new temperature and/or pressure
    using MHR.

    Calculate an observable in the muVT ensemble at a new temperature and/or pressure
    using MHR.

    Arguments:
        kT (array): Values of :math:`kT` for the various simulations.

        P (array): Values of :math:`P` for the various simulations.

        E (list of arrays): `E[n]` is an array containing the energies for the `n` th simulation;
          `E[n][i]` is the energy for the `i` th data point.

        V (list of arrays): `V[n]` is an array containing the volumes for the `n` th simulation;
          `V[n][i]` is the volume for the `i` th data point.

        obs (list of arrays): `obs[n][i]` is the observable corresponding to the `i` th data point
           in the `n` th simulation.

        kT_new (array): The :math:`kT` to be reweighted to

        P (array): The new :math:`P` to be reweighted to

        weights (list of arrays): Weights to be applied to each data point in `X`;
          The `i` th data point pertaining to :math:`\mathbf{b}^{(n)}` will be counted `weight[n][i]` 
          times. If `None` then all data points are counted once.

    Returns:
        float: The value of the observable at `kT_new` and `P` calculated using MHR.

    """
    
    nrun = len(kT)
    
    b = []
    for n in range(nrun):
        b.append([ -1.0/kT[n], -P[n]/kT[n] ])
    b = np.asarray(b)
    
    X = []
    for n in range(nrun):
        Xn = np.zeros( (len(E[n]),2) )
        Xn[:,0] = E[n]
        Xn[:,1] = V[n]
        X.append(Xn)

    obs2 = []
    for n in range(nrun):
        obs2n = np.zeros( (len(obs[n]),1) )
        obs2n[:,0] = obs[n]
        obs2.append(Xn)

    bnew = np.asarray([-1.0/kT_new, -P_new/kT_new])
    
    return reweight_observable(b, X, obs, bnew, weights=weights)
