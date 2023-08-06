""" Functions for analysing Monte Carlo time series """




import numpy as np
import logging

import scipy.special
import scipy.stats

logger = logging.getLogger(__name__)


# Values of the student's t-distribution corresponding to 95% confidence
# interval (two tailed), for t-distributions with various degrees of freedom. 
# TDIST[n] is defined as follows: the student's t-distribution with 'n'
# degrees of freedom will be between -TDIST[n] and TDIST[n] is 95%.
# The maximum 'n' tabulated here is 100. Note that the analogous value for
# 'n' in the infinite limit is 1.960.
TDIST = ( float('NaN'), 12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365,
          2.306, 2.262, 2.228, 2.201, 2.179, 2.160, 2.145, 2.131, 2.120,
          2.110, 2.101, 2.093, 2.086, 2.080, 2.074, 2.069, 2.064, 2.060,
          2.056, 2.052, 2.048, 2.045, 2.042, 2.040, 2.037, 2.035, 2.032,
          2.030, 2.028, 2.026, 2.024, 2.023, 2.021, 2.020, 2.018, 2.017,
          2.015, 2.014, 2.013, 2.012, 2.011, 2.010, 2.009, 2.008, 2.007,
          2.006, 2.005, 2.004, 2.003, 2.002, 2.002, 2.001, 2.000, 2.000,
          1.999, 1.998, 1.998, 1.997, 1.997, 1.996, 1.995, 1.995, 1.994,
          1.994, 1.993, 1.993, 1.993, 1.992, 1.992, 1.991, 1.991, 1.990,
          1.990, 1.990, 1.989, 1.989, 1.989, 1.988, 1.988, 1.988, 1.987,
          1.987, 1.987, 1.986, 1.986, 1.986, 1.986, 1.985, 1.985, 1.985,
          1.984, 1.984, 1.984 )




def tdist(n):

    r"""Returns the value of the student's t-distribution corresponding to
    a 95% confidence interval

    Returns the value of the student's t-distribution corresponding to
    a 95% confidence interval (two-tailed) and `n` degrees of freedom.

    Parameters
    ----------
    n : int
        The number of degrees of freedom for the t-distribution

    Returns
    -------
    float
       The value corresponding to the two-tailed 95% confidence interval.
       For `n>100` the value corresponding to the normal distribution
       (which is the t-distribution in the limit of infinite degrees of
       freedom) is returned, namely 1.960. For `n<1` NaN is returned.

    Notes
    -----
    * For a given `n`, this function returns the two-tailed 95% confidence  
      interval for the student's t-distribution with 'n' degrees of freedom.
      This is the value :math:`x` for which the probability that the 
      t-distribution with `n` degrees of freedom is between :math:`-x` and
      :math:`x` is 95%
    * The values returned by this function are accurate to only 3 decimal
      places

    """

    if n > 100:

        return 1.960
 
    elif n <= 0:

        return float('NaN')

    else:

        return TDIST[n]




def block_averages(y, blocksize, reverse=False):

    r"""Extracts block averages from a time series
    
    Partitions the time series `y` into contiguous blocks, 
    calculates the average for each block, and returns these
    averages

    Parameters
    ----------
    y : array
        The time series under consideration
    blocksize : int
        The number of elements in `y` to include in a block
    reverse : bool
        If False (default) then blocks are constructed by iterating
        over elements in `y` starting from the first element in
        `y`. If True then blocks are constructed by iterating
        over elements in `y` starting from the last element in
        `y`, and proceeding to the first.
    
    Returns
    -------
    array
       An array containing the averages for all blocks

    Notes
    -----
    * The array returned by this function will be empty if
      `blocksize` is larger than the size of `y`    
    * Depending on the block size, if `reverse` is False then some
      elements at the end of `y` may not being included in any block.
      Conversely if `reverse` is True then some elements at the 
      beginning of `y` may not be included in any block.


    """

    logger.debug("Entered 'block_averages' function")
    logger.debug("len(y) = "+str(len(y)))
    logger.debug("y[0:9] = "+str(y[0:9]))
    logger.debug("blocksize = "+str(blocksize))
    logger.debug("reverse = "+str(reverse))

    # The number of blocks in the data
    nblocks = len(y) // blocksize

    logger.debug("nblocks = "+str(nblocks))

    if nblocks < 1:
        logger.debug("DEBUG WARNING: Found "+str(nblocks)+" blocks during block averaging")

    averages = np.zeros(nblocks)

    if reverse:

        for i in range(0,nblocks):
            logger.debug("block "+str(i)+": range = ["+str(len(y)-(i+1)*blocksize)+":"+str(len(y)-i*blocksize)+"]")
            averages[i] = np.mean( y[ (len(y)-(i+1)*blocksize) : (len(y)-i*blocksize) ] )
            logger.debug("block "+str(i)+": mean = "+str(averages[i]))

    else:

        for i in range(0,nblocks):
            logger.debug("block "+str(i)+": range = ["+str(i*blocksize)+":"+str((i+1)*blocksize)+"]")
            averages[i] = np.mean( y[ (i*blocksize) : ((i+1)*blocksize) ] )
            logger.debug("block "+str(i)+": mean = "+str(averages[i]))

    logger.debug("Exiting 'block_averages'")

    return averages



def standard_error(y, blocksize=1, reverse=False, assume_independent=False):

    r"""Calculates the standard error in data, optionally taking into account
    correlations and using block averaging.
    
    Calculates the standard error in data, optionally taking into account
    correlations and using block averaging. The following formula is used to
    calculate the standard error :math:`\sigma_{err}=\sqrt{\frac{s}{N}}\sigma`,
    where :math:`\sigma`, :math:`N` and :math:`s` are, respectively, the 
    standard deviation of, number of data points in, and statistical inefficiency
    of the data (or block averages formed from the data - see below).

    Parameters
    ----------
    y : array
        The time series under consideration
    blocksize : int
        For the purpose of calculating the standard error the data `y` is partitioned
        into blocks each comprised of `blocksize` elements. The block averages, i.e. the
        averages of `y` for all blocks, are used as the data going forwards to calculate
        the standard error.        
    reverse : bool
        If False (default) then blocks are constructed by iterating
        over elements in `y` starting from the first element in
        `y`. If True then blocks are constructed by iterating
        over elements in `y` starting from the last element in
        `y`, and proceeding to the first.
    assume_independent : bool
        If True then the block averages are assumed to be uncorrelated (in other words
        'independent observations'), and the statistical inefficiency is assumed
        to be 1 for the purposes of calculating the standard error. If False (default)
        the statistical inefficiency is calculated for the block averages.
    
    Returns
    -------
    float
       The mean value of `y`
    float
       The standard error in `y`

    Notes
    -----
    * The returned standard error will be 'NaN' if there are less than two
      blocks of data in `y`, and the returned mean will be 'NaN' if there 
      is less than one block.
    * Depending on the block size, if `reverse` is False then some
      elements at the end of `y` may not being included in any block.
      Conversely if `reverse` is True then some elements at the 
      beginning of `y` may not be included in any block.

    """

    mean = float('NaN')
    stderr = float('NaN')

    logger.debug("Entered 'block_uncertainty' function")
    logger.debug("len(y) = "+str(len(y)))
    logger.debug("y[0:9] = "+str(y[0:9]))
    logger.debug("blocksize = "+str(blocksize))
    logger.debug("reverse = "+str(reverse))
    logger.debug("assume_independent = "+str(assume_independent))

    # The number of blocks in the data
    nblocks = len(y) // blocksize

    logger.debug("nblocks = "+str(nblocks))

    if nblocks < 1:
        logger.debug("Found  0 blocks during block averaging")
        logger.debug("Returning mean, stderr = "+str(mean)+", "+str(stderr))
        # Return NaN for mean and stderr
        logger.debug("Exiting 'block_averages'")
        return mean, stderr

    logger.debug("Calculating block_averages...")
    averages = block_averages(y,blocksize,reverse)
    logger.debug("averages = "+str(averages))

    mean = np.mean(averages)
    logger.debug("mean of block averages = "+str(mean))

    if nblocks >1:

        logger.debug("Found "+str(nblocks)+" > 1 blocks during block averaging")
        logger.debug("Proceeding with stderr calculation...")

        if assume_independent:
            logger.debug("assume_independent=True: Setting inefficiency to 1")
            s=1
        else:
            logger.debug("assume_independent=False: Calculating inefficiency...")
            s = inefficiency(averages)
            logger.debug("s = "+str(s))

        logger.debug("Calculating standard error...")
        stderr = np.sqrt(np.var(averages)*s/nblocks )
        logger.debug("stderr = "+str(stderr))

        logger.debug("Returning mean, stderr = "+str(mean)+", "+str(stderr))
        logger.debug("Exiting 'block_averages'")
        return mean, stderr

    else: 

        logger.debug("Found 1 block during block averaging")
        logger.debug("Returning mean, stderr = "+str(mean)+", "+str(stderr))
        # Return NaN for stderr
        logger.debug("Exiting 'block_averages'")
        return mean, stderr




def autocorrelation(y):

    r"""Calculates the autocorrelation function of a time series

    Calculates the autocorrelation function of a time series. The
    definition of the autocorrelation function used here is given
    below

    Parameters
    ----------
    y : array
        The time series under consideration

    Returns
    -------
    array
        The autocorrelation function for `y`, as defined below, for 
        :math:`k=0,1,\dotsc,(N-1)`, where :math:`N` is the number
        of elements in `y`

    Notes
    -----
    * The autocorrelation function is defined here as
      :math:`\Psi_k=\frac{1}{(N-k)\text{Var}(y)}\sum_{i=1}^{N-k}(y_i-\bar{y})(y_{i+k}-\bar{y})`,
      where :math:`0\leq k\leq (N-1)`, :math:`\bar{y}` is the mean in `y` and
      :math:`\text{Var}(y)=\sqrt{\frac{1}{N}\sum_{i=1}^N(y_i-\bar{y})^2}`
      is the variance in `y`
    * Note that the number of pairs of elements in `y` which are
      used to calculate :math:`\Psi_k` is :math:`(N-k)`. Hence
      the autocorrelation becomes more 'noisy' with increasing
      :math:`k`
    * A single-element array with 'NaN' is returned if the number of
      elements in `y` is 0 or 1.

    """

    logger.debug("Entered 'autocorrelation' function")
    logger.debug("len(y) = "+str(len(y)))
    logger.debug("y[0:9] = "+str(y[0:9]))

    if len(y)<=1:
        logger.debug("len(y)<=1: returning single-value array containing NaN")
        return np.asarray( [float('NaN')] )

    mean =  np.mean(y)
    var = np.var(y)

    yshifted = y - mean

    logger.debug("mean = "+str(mean))
    logger.debug("var = "+str(var))
    logger.debug("yshifted[0:9] = "+str(yshifted[0:9]))

    autocorr = np.zeros(len(y))
    for k in range(0, len(y)):
        for i in range(0, len(y)-k):
            autocorr[k] += yshifted[i]*yshifted[i+k]
        autocorr[k] = autocorr[k] / (var * (len(y)-k))

    logger.debug("len(autocorr) = "+str(len(autocorr)))
    logger.debug("returned array [0:9] = "+str(autocorr[0:9]))
    logger.debug("Exiting 'autocorrelation'")
    return autocorr


def inefficiency(y):

    r"""Calculates the statistical inefficiency of data

    Calculates the statistical inefficiency of data. The
    definition of the statistical inefficiency used here is 
    given below

    Parameters
    ----------
    y : array
        The time series under consideration

    Returns
    -------
    float
        The statistical inefficiency of `y`, as defined below

    Notes
    -----
    * The statistical inefficiency is defined as :math:`s=1+2\sum_{k=1}^{\infty}\Phi_k`
      for a stationary infinite time series, where :math:`\Psi_k` is the autocorrelation 
      function (as defined in the function `autocorrelation` with :math:`N\to\infty`).
      It is a measure of the number of uncorrelated samples in the time series: an
      inefficiency of 1 signifies no correlations, while higher values signify increased
      correlations. Morevover the inefficiency is related to the autocorrelation time
      of the series. If we assume :math:`\Phi_k=\exp(-k/\tau)`, then it follows that
      :math:`s` and :math:`\tau` are related by :math:`\tau=-1/\ln[1-2/(s+1)]`.
    * Calculating :math:`s` directly via this formula (with the :math:`\infty` changed to
      :math:`(N-1)`, where :math:`N` is the size of the time series) will fail since 
      partial sums over :math:`k` do not converge. Here we use the 'initial positive 
      sequence estimator' of the sum - see C. J. Geyer, 'Practical Markov Chain Monte Carlo', 
      Statistical Science 7 473 (1992).
    * If the initial positive sequence estimator yields a value for the inefficiency less
      than 1, 1 is returned instead.
    * To calculate the statistical inefficiency of a time series as above, the time 
      series should be large enough that :math:`\Phi_k` can be estimated accurately
      enough.
    * A single-element array with 'NaN' is returned if the number of
      elements in `y` is 0 or 1.
    """

    logger.debug("Entered 'inefficiency' function")
    logger.debug("len(y) = "+str(len(y)))
    logger.debug("y[0:9] = "+str(y[0:9]))

    if len(y)<=1:
        logger.debug("len(y)<=1: returning single-value array containing NaN")
        return np.asarray( [float('NaN')] )
    
    logger.debug("Calculating autocorrelation function for statistical inefficiency...")
    autocorr = autocorrelation(y)
    logger.debug("len(autocorr) = "+str(len(autocorr)))
    logger.debug("autocorr[0:9] = "+str(autocorr[0:9]))

    if any( np.isnan(autocorr) ):
        logger.debug("Detected NaN in autocorr. Setting inefficiency to NaN and returning...")
        s = float('NaN')
        logger.debug("s = "+str(s))
        logger.debug("Exiting 'inefficiency'")
        return         

    # 's_sum' is the sum over 'k' mentioned above. Use the initial positive sequence 
    # estimator method to calculate this - sum over terms from i=1 to 2*m+1, where m
    # is the largest integer for which autocorr[2*n]+autocorr[2*n+1]>0 for n=1,2,...,m.
    # See C. J. Geyer, 'Practical Markov Chain Monte Carlo', Statistical Science 7 473 (1992)
    s_sum = 0.0
    for i in range(1,len(autocorr)-1):

        if i%2==0:
            logger.debug("i, s_sum, autocorr[i]+autocorr[i+1] = "+str(i)+" "+str(s_sum)+" "+str(autocorr[i]+autocorr[i+1]))

        if i%2==0 and (autocorr[i]+autocorr[i+1])<=0.0:
            break
        else:
            s_sum += autocorr[i]

    # The estimated statistical inefficiency
    s = 1.0+2.0*s_sum

    if s < 1.0:
        logger.debug("s = "+str(s)+" is less than 1.0. Setting it to 1.0")
        s = 1.0

    logger.debug("s = "+str(s))
    logger.debug("Exiting 'inefficiency'")

    return s


def autocorrelation_time(y):

    r"""Calculates the autocorrelation time of data

    Calculates the autocorrelation time of data.

    Parameters
    ----------
    y : array
        The time series under consideration

    Returns
    -------
    float
        The autocorrelation time of `y`, as defined below

    Notes
    -----
    * The statistical inefficiency is defined as :math:`s=1+2\sum_{k=1}^{\infty}\Phi_k`
      for a stationary infinite time series, where :math:`\Psi_k` is the autocorrelation 
      function (as defined in the function `autocorrelation` with :math:`N\to\infty`).
      It is a measure of the number of uncorrelated samples in the time series: an
      inefficiency of 1 signifies no correlations, while higher values signify increased
      correlations. The inefficiency is related to the autocorrelation time
      of the series. If we assume :math:`\Phi_k=\exp(-k/\tau)`, then it follows that
      :math:`s` and :math:`\tau` are related by :math:`\tau=-1/\ln[1-2/(s+1)]`. This is
      the definition of the autocorrelation time used here.
    * This function uses the function `inefficiency` to calculate the inefficiency,
      which is then converted into the autocorrelation time via the above equation.
    * If the inefficiency for `y` is less than 1.000000001 then an autocorrelation 
      time of 0 is returned.
    * A 'NaN' is returned if the number of elements in `y` is 0 or 1.
    """

    logger.debug("Entered 'autocorrelation_time' function")
    logger.debug("len(y) = "+str(len(y)))
    logger.debug("y[0:9] = "+str(y[0:9]))

    if len(y)<=1:
        logger.debug("len(y)<=1: returning NaN")
        return float('NaN')
    
    logger.debug("Calculating statistical inefficiency for autocorrelation time...")
    s = inefficiency(y)
    logger.debug("s = "+str(s))

    if s < 1.000000001:
        logger.debug("s<1.000000001: setting tau=0.0")
        tau = 0.0                    
    else:
        tau = -1.0/np.log(1.0-2.0/(s+1))

    logger.debug("tau = "+str(tau))
    logger.debug("Exiting 'autocorrelation_time'")

    return tau




def equilibration_test(y, checktimes=[0.0,0.5], minslicesize=100, confint=0.05, minslicesize_corrtime=6.0):

    r"""Checks whether a time series has equilibrated

    Checks whether a time series has equilibrated. This function considers slices of
    the data series in order to find a slice which is 'flat'. Here a slice is a window of
    the time series which can begin anywhere, but must end at the end of the time
    series. The slices the function will consider are specified in `checktimes`. If a slice
    is found to be flat, then the start time of the slice is a conservative estimate of the
    equilibration time for the time series.

    Whether or not a slice is flat is determined by applying a Wilcoxon signed-rank test to
    both halves of the slice. This statistical test compares the two halves to ascertain if
    they have the same underlying distribution. The initial assumption here is that they do
    have the same distribution, i.e. that the slice is flat. The slice is deemed 'not flat'
    only if there is sufficient evidence to support this. With this in mind, `confint` is 
    the confidence interval associated with deeming a slice to be not flat: the higher 
    `confint`; the less likely this function is to deem a slice to be not flat. In other
    words, increasing `confint` makes the function more likely to say that a time series 
    has equilibrated. 

    Parameters
    ----------
    y : array
        The time series under consideration.
    checktimes : list
        A list of floats determining the slices of the time series to examine. Each
        element of the list corresponds to a slice, and is the fractional distance 
        along the time series at which the slice is to start. E.g. 0.5 corresponds 
        to a slice starting in the middle of the time series. The slices are examined
        in the order specified in the list, the function terminating if any slice 
        is found to be flat; thus the order of elements in the list should be in
        ascending order if one wishes to determine a more precise equilibration time
    minslicesize : int
        A slice with less than `minslicesize` elements will be deemed too small to 
        examine, and thus regarded as 'not flat'. This must be greater than 1.
    confint : float
        Confidence interval for deeming a slice to be 'not flat' using the Wilcoxon
        signed-rank test. `confint` should be between 0.0 and 1.0, where 1.0 
        corresponds to deeming all slices to be flat, and 0.0 corresponds to 
        deeming all slices to be not flat.
    minslicesize_corrtime : float
        If a slice is found which is flat according to the p-value test, the slice 
        must also be sufficiently large compared to the autocorrelation time for the 
        slice before the slice is 'confirmed' to be flat: the number of data points 
        in the slice must be at least `minslicesize_corrtime` times the 
        autocorrelation time before the slice is confirmed to be flat

    Returns
    -------
    flatslice : boolean
        True if the function finds a flat slice, False if it does not
    slicepos : int
        If `flatslice` is True then `slicepos` is the location beyond which the
        time series was deemed flat, i.e. it is the time series index corresponding
        to the start of the slice which was deemed flat. This corresponds to one of 
        fractional locations specified in `checktimes` - *the first in that list 
        which yields a flat slice*. If `flatslice` is False then `slicepos` is the 
        location of the start of the last slice considered by the algorithm

    Notes
    -----
    * A slice consisting entirely of all the same elements is consider to not be flat
      by this function.
    """

    logger.debug("Entered 'equilibration_test' function")
    logger.debug("len(y) = "+str(len(y)))
    logger.debug("y[0:10] = "+str(y[0:10]))

    assert minslicesize > 1

    if len(y)<2:
        logger.debug("Detected len(y)<2! Returning flatslice,slicepos = False,0")
        return False, 0

    flatslice = False

    for checktime in checktimes:

        logger.debug("Considering slice beginning at fraction "+str(checktime)+" of time series...")
        slicepos = int(checktime * len(y))
        slice = y[slicepos:]

        size = len(slice)

        logger.debug("  location of start of slice = "+str(slicepos))
        logger.debug("  size of slice = "+str(size))
        logger.debug("  first 10 data points in slice = "+str(slice[0:10]))

        if size < minslicesize:

            logger.debug("Slice is below size threshold. Assuming slice is not flat")
            break

        logger.debug("Slice is above size threshold")

        # Perform a Wilcoxon sign test, comparing the first half of the slice to
        # the second. Note that we disregard the last point in the slice if it has
        # an odd number of samples.
        logger.debug("Applying Wilcoxon sign test to both halves of slice...")
        halfpos = size//2
        slicehalf1 = slice[0:halfpos]
        slicehalf2 = slice[halfpos:(2*halfpos)]
        logger.debug("  location of half of slice = "+str(halfpos))
        logger.debug("  first 10 data points in 1st half of slice = "+str(slicehalf1[0:10]))
        logger.debug("  first 10 data points in 2nd half of slice = "+str(slicehalf2[0:10]))

        # The Wilcoxon test will return an error if there is no difference between the slices.
        # In this case we regard the slice as not flat (see doc comments for details) 
        if np.array_equal(slicehalf1, slicehalf2):
            logger.debug("  Detected half-slices are identical. Assuming slice as not flat.")
            break

        # The null hypothesis is that subtracting the values in the first slice from the second
        # slice gives a distribution which is symmetric about 0. The p-value is the probability that
        # the data conforms to this hypothesis given the null hypothesis: a low p-value signifies
        # that the data is not consistent with the hypothesis.
        teststat, pvalue = scipy.stats.wilcoxon(slicehalf1,slicehalf2)
        logger.debug("  p-value from Wilcoxon test = "+str(pvalue))       

        if pvalue < confint:
             
            logger.debug("p-value less than confint. Detected difference in both halves of slice.")
            logger.debug("Slice deemed not flat.")            

        else:

            logger.debug("p-value greater than confint. No detected difference in both halves of slice.")
            logger.debug("Slice deemed flat.")            
            flatslice = True

        
        if flatslice:

            logger.debug("This slice seems flat. Cross-checking size of slice against correlation time...")

            logger.debug("Calculating autocorrelation time via statistical inefficiency...")

            s = inefficiency(slice)

            # tau is the correlation time (assuming the corelation function is
            # of the form exp(-k/tau))

            # The inefficiency could be 1, in which case tau below would be log(0.0),
            # which is NaN. This special case corresponds to a correlation time of 0.
            if s < 1.0000000001:

                logger.debug("  inefficiency is == 1! Setting correlation time to 0")
                tau = 0.0
                logger.debug("  correlation time = "+str(tau))

            else:

                logger.debug("  inefficiency is > 1")
                tau = -1.0/np.log(1.0-2.0/(s+1))
                logger.debug("  correlation time = "+str(tau))
                logger.debug("  slice size in units of correlation time = "+str(size/tau))


            if size > tau * minslicesize_corrtime:

                logger.debug("Slice is larger enough than correlation time threshold. Slice is confirmed flat.")
                logger.debug("Exiting 'equilibration_test'; returning: "+str(flatslice)+", "+str(slicepos))
                return flatslice, slicepos

            else:
            
                logger.debug("Slice is not larger enough than correlation time. Slice is no longer deemed flat")
                flatslice = False


        logger.debug("Slice is not deemed flat.")


    logger.debug("No flat slices found")
    logger.debug("Exiting 'equilibration_test'; returning: "+str(flatslice)+", "+str(slicepos))

    return flatslice, slicepos
