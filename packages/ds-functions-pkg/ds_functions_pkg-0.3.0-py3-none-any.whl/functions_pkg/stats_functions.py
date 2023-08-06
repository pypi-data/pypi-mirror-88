import numpy as np
import scipy.stats as stats

# ================================================================
# 95% CONFIDENCE INTERVAL FUNCTION
# ================================================================


def get_95_ci(x1, x2):
    #  Calculate a 95% CI for 2 1d numpy arrays
    signal = x1.mean() - x2.mean()
    noise = np.sqrt(x1.var() / x1.size + x2.var() / x2.size)
    ci_lo = signal - 1.96 * noise
    ci_hi = signal + 1.96 * noise
    return ci_lo, ci_hi


# ================================================================
# COMMON LANGUAGE EFFECT SIZE
# ================================================================

def cles_ind(x1, x2):
    """
    COMMON LANGUAGE EFFECT SIZE

    Interpret as the probability that a score sampled
    at random from one distribution will be greater than
    a score sampled from some other distribution.
    Based on: http://psycnet.apa.org/doi/10.1037/0033-2909.111.2.361

    :param x1: sample 1
    :param x2: sample 2
    :return: (float) common language effect size
    """
    x1 = np.array(x1)
    x2 = np.array(x2)
    diff = x1[:, None] - x2
    cles = max((diff < 0).sum(), (diff > 0).sum()) / diff.size
    return cles


# ================================================================
# 2 MEDIAN GROUP TEST CONFIDENCE INTERVAL
# ================================================================

def calc_non_param_ci(x1, x2, alpha=0.05):
    """Calc confidence interval for 2 group median test
    Process:
    * Find all pairwise diffs
    * Sort diffs
    * Find appropriate value of k
    * Choose lower bound from diffs as: diffs[k]
    * Choose upper bound from diffs as: diffs[-k]
    Based on: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2545906/

    :param x1: sample 1
    :param x2: sample 2
    :param alpha: significance level
    :return: (tuple) confidence interval bounds
    """

    x1 = np.array(x1)
    x2 = np.array(x2)

    n1 = x1.size
    n2 = x2.size
    cv = stats.norm.ppf(1 - alpha / 2)

    # Find pairwise differences for every datapoint in each group
    diffs = (x1[:, None] - x2).flatten()
    diffs.sort()

    # For an approximate (1-a)% confidence interval first calculate K:
    k = int(round(n1 * n2 / 2 - (cv * (n1 * n2 * (n1 + n2 + 1) / 12) ** 0.5)))

    # The Kth smallest to the Kth largest of the n x m differences
    # n1 and n2 should be > ~20
    ci_lo = diffs[k]
    ci_hi = diffs[-k]

    return ci_lo, ci_hi
