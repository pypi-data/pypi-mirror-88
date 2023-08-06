"""Single Histograms and Single Histogram Reweighters

"""

# Ignore pylint "no-member" problem
# pylint: disable=E1101

import warnings
import numpy

from dlmontepython.htk.parameter import Parameter

def boltzmann_weights(alpha, b_old, b_new, sobs, free0=None):

    """Compute single set of weights w_i = exp[a (b_old - b_new) s_i].

    Arguments:
    alpha (float):           constant
    b_old (float):           "old" value of reweighting parameter
    b_new (float):           "new" value of reweighting parameter
    sobs (numpy.ndarray):    Set of measurements of appropriate action s_i

    The units of a, (b_old - beta_new), and s_i must be consistent.

    Optional:
    free0 (numpy.ndarray):   offset (dimensionless) free energy or ln(weight)
                             value for each observation in s_i.

    If the definition of (b_old - b_new) has the wrong sign in a
    particular context, an additional sign should be included in
    the constant alpha.
    """

    weights = numpy.zeros(sobs.size)
    weights[:] = numpy.exp(alpha*(b_old - b_new)*sobs[:])

    if free0 is not None:
        weights[:] *= numpy.exp(free0[:])

    return weights


def boltzmann_reweight_obs(obs, alpha, b_old, b_new, sobs, free0=None):

    """Reweight observable.

    if db = b_old - b_new, the reweighted observable value is:

        <obs>_b_new = sum_i o_i exp[a.db.s_i] / sum_i exp[a.db.s_i]

    where the relevant observations, and those of the action s_i
    are taken at b_old.

    Arguemnts:
    obs (numpy.ndarray):     observables (at b_old) to be reweighted
    alpha (float):           constant
    b_old (float):           "old" value of reweighting parameter
    b_new (float):           "new" value of reweighting parameter
    sobs (numpy.ndarray):    observations of action s_i at b_old

    Returns:
    (float):                 expectation value of reweighted observable
    """

    if free0 is None:
        free0 = numpy.zeros(sobs.size)

    # If the energies are large, overflow can result in the exponent
    # (often for exp(x) with x >~ 700.0). Overflow may be avoided by
    # multiplying numerator and denominator by exp[-maxval(s_i)].
    # Overflow generates a Warning()

    # A sort into ascending values can also help to mitigate
    # accumulation of round-off

    # However, the sort can be rather slower, so...

    warnings.filterwarnings("error")

    db = b_old - b_new

    try:
        robs = numpy.sum(numpy.exp(alpha*db*sobs[:] + free0[:])*obs[:])
        rnrm = numpy.sum(numpy.exp(alpha*db*sobs[:] + free0[:]))

        result = robs/rnrm

    except Warning:
        # Try again...

        sarg = alpha*db*sobs[:] + free0[:]

        ind = numpy.argsort(sarg)
        sobsort = sarg[ind]
        obsort = obs[ind]
        esmax = sobsort[-1]

        robs = numpy.sum(numpy.exp(sobsort[:] - esmax)*obsort[:])
        rnrm = numpy.sum(numpy.exp(sobsort[:] - esmax))

        result = robs/rnrm


    return result



class Reweighter(object):

    """Machinery for reweighting observations.

    Set up a reweighter for reweighting to new values of some parameter
    appearing in the relevant action,

    It is essential to get the units of alpha, b_old, and S_i correct
    and consistent; this will depend on the Hamiltonian under
    consideration. Reweighting will go badly wrong if the product
    a.(b-b').s_i is not dimensionless.
    """

    def __init__(self, name, b_old, alpha, sobs):

        """Initialise from constant data.

        Arguemnts:
        name (string):        a descriptive name used as unique id
        b_old (Parameter):    parameter associated with observations S_i
        alpha (Parameter):    "a" constant
        sobs (Observable):    the series of measurements in the action S_i
        """

        self.name = name
        self.b_old = b_old
        self.alpha = alpha
        self.sobs = sobs


    def __str__(self):

        """Return a readable summary"""

        rstr = "alpha= {!r}, b_old= {!r}, b_new= {!r}, sobs= {}"\
            .format(self.alpha, self.b_old, self.b_new, self.sobs)

        return "Reweighter({})".format(rstr)


    def rid(self):

        """Return reweighter id, which is lower case name"""

        return self.name.lower()


    def compute_weights(self, b_new):

        """Compute Boltzmann weights w_i = exp[a*(b_old - b_new)*S_i)]

        Arguments:
        b_new (float):           "new" value of reweighting parameter

        Returns:
        weights (numpy.ndarray): Computed weights
        """

        return boltzmann_weights(self.alpha, self.b_old, b_new, self.sobs.data)


    def reweight_obs(self, obs, b_new, free0=None):

        """Reweight observations to new value of reweighting parameter.

        Arguments:
        obs (numpy.ndarray):                 observations to be reweighted
        b_new (scalar or numpy.ndarray):     new value or values

        The number of observations must match those in the action
        supplied to the constructor.

        Returns:
        Reweighted expectation value (scalar or numpy.ndarray)
        """

        b_array = numpy.array(b_new, copy=False)

        sobs = self.sobs.data

        try:
            result = numpy.zeros(len(b_array))
            itr = numpy.nditer(b_array, flags=['c_index'])

            while not itr.finished:
                rvalue = boltzmann_reweight_obs(obs, self.alpha, self.b_old,
                                                itr[0], sobs, free0)
                result[itr.index] = rvalue
                itr.iternext()

        except TypeError:

            # If beta_new is a scalar, return a scalar

            result = boltzmann_reweight_obs(obs, self.alpha, self.b_old, b_new,
                                            sobs, free0)

        return result


class BetaReweighter(Reweighter):

    """Reweighter for Boltzmann weights exp[a*(beta_old - beta_new)S_i]

    This is a convenience which can be used when the
    reweighting parameter is the inverse tempertature
    beta = 1/k_bT. S_i is then expected to be the total energy.
    """

    def __str__(self):

        """Return BetaReweighter(contents)"""

        rstr = "name= {!r}, beta_old= {!r}, alpha= {!r}, sobs= {}" \
            .format(self.name, self.b_old, self.alpha, self.sobs)

        return "BetaReweighter({})".format(rstr)


class KTReweighter(Reweighter):

    """Reweighter for Boltzmann weights exp[a*(1/kt_old - 1/kt_new)*S_i]

    This is a convenience to allow reweighting using new value of kT.
    """

    def __init__(self, name, kt_old, alpha, sobs):

        """Initialise reweighting constants including kT.

        Arguments:
        name (string):         a descriptive name
        kt_old (Parameter):    fixed value of kT relevant for sobs
        alpha (Parameter):     a constant
        sobs (numpy.ndarray):  observations of the action S_i
        """

        b_old = Parameter(1.0/kt_old, kt_old.label)
        super(KTReweighter, self).__init__(name, b_old, alpha, sobs)

        self.kt_old = kt_old


    def __str__(self):

        """It's less confusing to report kt_old, rather than b_old."""

        rstr = "name={!r}, kt_old={!r}, alpha={!r}, sobs={}" \
            .format(self.name, self.kt_old, self.alpha, self.sobs)

        return "KTReweighter({})".format(rstr)


    def compute_weights(self, kt_new):

        """Compute single set of Boltzmann weights for new temperature"""

        b_new = 1.0/kt_new

        return super(KTReweighter, self).compute_weights(b_new)


    def reweight_obs(self, obs, kt_new, free0=None):

        """Reweight observation to new value of kT.

        Arguments:
        obs (numpy.ndarray):               observations to be reweighted
        kt_new (float or numpy.ndarray):   new value or values of kT

        Returns:
        (float or numpy.ndarray): reweighted value or values
        """

        b_new = 1.0/kt_new

        return super(KTReweighter, self).reweight_obs(obs, b_new, free0)


class ChainReweighter(Reweighter):

    r"""Reweighter for two or more parameters at a time.

    Reweighting can take place wrt more than one parameter, e.g.,

    <O>_{b1', b2',...} = \sum O_i exp1 exp2 ...  / \sum exp1 exp2 ...

    where exp1 = exp[ a1 (b1_old - b1_new) S1_i ]
          exp2 = exp[ a2 (b2_old - b2_new) S2_i ]
    and so on.

    This reweighter provides explicit reweighting of one parameter
    directly, and at the same time other parameters via specification
    of the appropriate set of Boltzmann weight factors w_i = exp_i.

    All the weight factors must have the same number of observations.
    """

    def __init__(self, name, b_old, alpha, sobs, *weights):

        """Initialise superclass along with one or more weights.

        """

        super(ChainReweighter, self).__init__(name, b_old, alpha, sobs)
        self.weights = list(weights)


    def __str__(self):

        rstr = "name={!r}, kt_old={!r}, alpha={!r}, sobs={}, weights={!r}" \
            .format(self.name, self.b_old, self.alpha, self.sobs, self.weights)

        return "ChainReweighter({})".format(rstr)


    def compute_weights(self, b_new):

        r"""Compute aggregate weights:

        w_i = exp[a(b_old - b_new)S_i + fobs_i ]

        where fobs_i = \sum_j ln(w_i) for the sets of weights j supplied
        to the constructor.

        Arguemnts:
        b_new (float):        the "new" value of the reweighting parameter
        """

        weights = boltzmann_weights(self.alpha, self.b_old, b_new,
                                    self.sobs.data, self.fobs())
        return weights


    def reweight_obs(self, obs, b_new, free0=None):

        """Reweight observable

        Arguments:
        obs (numpy.ndarray):    obsevations to be rewighted
        b_new (float):          'new' value of reweighting parameter
        free0 (numpy.ndarray):  weight factors (see fobs())

        Returns:
        (float or numpy.ndarray) reweighted obseravble(s)
        """

        if free0 is None:
            fobs = self.fobs()
        else:
            fobs = free0

        robs = super(ChainReweighter, self).reweight_obs(obs, b_new, fobs)

        return robs


    def fobs(self):

        """Return aggregate ln(weight) factors"""

        fobs = numpy.zeros(self.sobs.data.size)
        for weight in self.weights:
            fobs[:] = fobs[:] + numpy.log(weight[:])

        return fobs


class Histogram(object):

    """Histogram object"""

    def __init__(self, obs, nbins=10):

        """Container for actual histogram data

        Arguments:
        obs(numpy.ndarray):     observations to be binned
        nbins (integer):        number of bins

        The numpy.histogram function is useed to do the binning.
        """

        self.nbins = nbins
        self.obs = obs
        self.wgt = numpy.ones(obs.size)
        self.reweighters = []


    def add_reweighter(self, reweighter):

        """Register a (uniquely named) reweighter"""

        present = False
        key = reweighter.name
        for exist in self.reweighters:
            if key == exist.name:
                present = True

        if not present:
            self.reweighters.append(reweighter)
        else:
            raise ValueError("Already a reweighter {!r}".format(key))


    def weight_wrt(self, rid, rnew):

        """Recompute weights appropriate for reweighter id"""

        found = False
        for reweighter in self.reweighters:
            if rid == reweighter.name:
                found = True
                self.wgt = reweighter.compute_weights(rnew)

        if not found:
            raise ValueError("Don't know how to reweight {}".format(rid))


    def statistic(self):

        """Compute histogram statistics using the current weights

        These are the moments of the histogram, and not of the
        observations. They are therefore subject to binning errors.
        """

        obsrange = (self.obs.min(), self.obs.max())

        px, xbin = \
            numpy.histogram(self.obs, bins=self.nbins, range=obsrange, \
                            density=True, weights=self.wgt)

        x = numpy.zeros(self.nbins)
        dx = numpy.zeros(self.nbins)
        dx[0:] = xbin[1:] - xbin[0:-1]
        x[0:] = xbin[0:-1] + 0.5*dx[0:]

        # Central moments to third order

        hm0 = numpy.sum(px[:]*dx[:])
        hm1 = numpy.sum(x[:]*px[:]*dx[:])
        hm2 = numpy.sum((x[:] - hm1)**2*px[:]*dx[:])
        hm3 = numpy.sum((x[:] - hm1)**3*px[:]*dx[:])

        # h_infinity moment:
        hinf = numpy.max(numpy.abs(x[:] - hm1))

        return hm0, hm1, hm2, hm3, hinf


    def plot(self, pyplot):

        """Plot current histogram with pyplot"""

        obsrange = (self.obs.min(), self.obs.max())

        px, xbin = numpy.histogram(self.obs, bins=self.nbins, range=obsrange,
                                   density=True, weights=self.wgt)

        barwidth = (obsrange[1] - obsrange[0])/self.nbins
        bars = pyplot.bar(xbin[0:-1], px, width=barwidth)

        return bars


    #TU: Added by me
    def arrays(self, obsmin, obsmax):

        """Returns the histogram data as two arrays: the probability density 
           (stored in the 2nd returned array) vs. the observable (stored in the
           1st returned array)."""

        obsrange = (obsmin, obsmax)

        px, xbin = numpy.histogram(self.obs, bins=self.nbins, range=obsrange,
                                   density=True, weights=self.wgt)

        return xbin, px
