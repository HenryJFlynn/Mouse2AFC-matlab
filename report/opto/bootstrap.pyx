# from cython.parallel import prange
import numpy as np
cimport numpy as np
cimport cython

from libc.stdlib cimport malloc, free, rand
from libc.math cimport isnan
from libc.stdio cimport printf

#from np.random import choice
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cpdef np.ndarray[np.float64_t, ndim=1] bootstrap(
  np.ndarray[np.float64_t, ndim=1] col,
  np.ndarray[np.float64_t, ndim=1] gains_distr,
  np.int32_t num_cycles,
  np.int32_t len_control_trials, np.int32_t len_opto_trials):
  # from report.utils import bootStrap
  # p = 0
  grps_sizes_li = (len_control_trials, len_opto_trials)
  # cdef np.ndarray[np.float64_t, ndim=1] gains_distr = np.empty(num_cycles,
  #                                                              dtype=np.double)
  cdef np.float64_t min_positive_val = 1/len_control_trials
  # We can reuse the same array for both
  cdef np.ndarray[size_t , ndim=1] rand_cntrl_idxs = np.empty(len_control_trials,
                                                              dtype=np.uintp)
  cdef np.ndarray[size_t , ndim=1] rand_opto_idxs = np.empty(len_opto_trials,
                                                             dtype=np.uintp)

  if True:
    _hotLoop(col, gains_distr, num_cycles, len_control_trials, len_opto_trials)
    # print("Gains distr:", gains_distr)
  else:
    for idx in np.arange(num_cycles):
      # Can we provide the choice arrays?
      col_cntrl = np.random.choice(col, len_control_trials, replace=True)
      col_opto = np.random.choice(col, len_opto_trials, replace=True)
      cntrl_mean = col_cntrl.mean()
      zero_if_zero = np.count_nonzero(cntrl_mean)
      cntrl_mean = zero_if_zero*cntrl_mean + (1-zero_if_zero)*min_positive_val
      # assert cntrl_mean2 == cntrl_mean
      # test_gain = ((col_opto.mean()/cntrl_mean)-1)
      gains_distr[idx] = (col_opto.mean()/cntrl_mean)-1
      # if (is_positive_gain and test_gain > obsv_gain) or (
      #     not is_positive_gain and test_gain < obsv_gain):
      #   p += 1
    # print("Gain distr:", gains_distr)
  return gains_distr


from cython.parallel import prange

@cython.cdivision(True)
@cython.wraparound(False)
@cython.boundscheck(False)
cdef void _hotLoop(np.float64_t[:] col, np.float64_t[::1] gains_distr,
                   Py_ssize_t num_cycles, int len_control_trials,
                   int len_opto_trials) nogil:
  cdef Py_ssize_t i, j, col_len = len(col)
  cdef np.float64_t cntrl_mean, opto_mean, res

  for i in prange(num_cycles, nogil=True):
    cntrl_mean = 0
    for j in range(len_control_trials):
      cntrl_mean += col[rand()%col_len]
    # Avoid dividing by zero
    # Branching is bad in a hot-loop, but this should be a rare occassion
    if cntrl_mean == 0:
      cntrl_mean = 1
    cntrl_mean = cntrl_mean/len_control_trials
    opto_mean = 0
    for j in range(len_opto_trials):
      opto_mean += col[rand()%col_len]
    opto_mean = opto_mean/len_opto_trials
    # res = ((opto_mean/cntrl_mean)-1)
    # if isnan(res):
    #   printf("Found nan with cntrl_mean=%d - opto_mean=%d\n", cntrl_mean,
    #          opto_mean)
    gains_distr[i] = ((opto_mean/cntrl_mean)-1)