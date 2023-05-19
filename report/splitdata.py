import numpy as np
import pandas as pd

# TODO: Add tests
def byDV(df, combine_sides=False, periods=3, separate_zero=True):
  bins = rngDV(periods=periods, combine_sides=combine_sides,
               separate_zero=separate_zero)
  # groups = []
  # DV = df.DV if not combine_sides else df.DV.abs()
  # # TODO: Use _splitByBins()
  # for (left, right)  in zip(rng, rng[1:]):
  #   if left >= 0:
  #     group_df = df[(left <= DV) & (DV < right)]
  #   else:
  #     group_df = df[(left < DV) & (df.DV <= right)]
  #   entry = pd.Interval(left=left, right=right), (left+right)/2, group_df
  #   groups.append(entry)
  # return groups
  return _splitByBins(df, bins, combine_sides=combine_sides)

def byPerf(df, combine_sides=False, periods=3, separate_zero=True,
           fit_fn_periods=10):
  bins = rngByPerf(df, periods=periods, separate_zero=separate_zero,
                   combine_sides=combine_sides, fit_fn_periods=fit_fn_periods)
  return _splitByBins(df, bins, combine_sides=combine_sides)

def byQuantile(df, combine_sides=False, periods=3, separate_zero=True):
  bins = rngByQuantile(df, periods=periods, separate_zero=separate_zero,
                       combine_sides=combine_sides)
  return _splitByBins(df, bins, combine_sides=combine_sides)


def _splitByBins(df, bins, combine_sides=False):
  groups = []
  DV = df.DV.abs() if combine_sides else df.DV
  for dv_rng, dv_df in df.groupby(pd.cut(DV, bins, include_lowest=True)):
    # We add zero to avoid having -0.0 printed
    dv_rng = pd.Interval(np.around(dv_rng.left, 2) + 0, dv_rng.right)
    entry = dv_rng, (dv_rng.left+dv_rng.right)/2, dv_df
    groups.append(entry)
  return groups


def rngDV(*, periods, combine_sides, separate_zero):
  import numpy as np
  periods += 1 # To include zero point
  rng = np.linspace(0, 1, periods) + 0.01
  if not combine_sides:
    _min = -rng[::-1]
    if not separate_zero:
      _min = _min[:-1]
      rng[0] = 0
    rng = np.concatenate([_min, rng])
  else:
    if not separate_zero:
      rng = rng[1:]
    rng = np.concatenate([[0], rng])
  return rng

def rngByPerf(df, *, periods, combine_sides, separate_zero, fit_fn_periods):
  df = df[df.ChoiceLeft.notnull()]
  stims, stim_count, stim_ratio_correct = [], [], []
  for _, _, dv_df in byDV(df, periods=fit_fn_periods,
                          combine_sides=combine_sides):
    if not len(dv_df):
      continue
    DV = dv_df.DV
    if combine_sides:
      DV = DV.abs()
    stims.append(DV.mean())
    stim_count.append(len(dv_df))
    perf_col = dv_df.ChoiceCorrect if combine_sides else dv_df.ChoiceLeft
    stim_ratio_correct.append(perf_col.mean())
  # TODO: Move psychFitBasic out of analysis
  from analysis import psychFitBasic
  pars, fitFn = psychFitBasic(stims=stims, stim_count=stim_count, nfits=200,
                              stim_ratio_correct=stim_ratio_correct)
  if combine_sides:
    possible_dvs = np.linspace(0,1,101)
  else:
    possible_dvs = np.linspace(-1,1,201)
  fits = fitFn(possible_dvs)
  min_perf = fits[0] if combine_sides else fits[possible_dvs == 0]
  max_perf_l, max_perf_r = fits[0], fits[-1]
  bins = [0]
  if separate_zero:
    if not combine_sides:
      bins = [-0.01] + bins
    bins += [0.01]
  cut_offs_perf = []
  def curBin(i, periods, is_neg):
    # If periods == 2, and we want to get 66.667% and 83.334%, then in ideal
    # case min_perf is 50% and max perf is 100%.
    max_perf = max_perf_r if not is_neg else max_perf_l
    cutoff_perf = min_perf + (max_perf-min_perf)*i/periods
    cutoff_idx = np.argmin(np.abs(fits-cutoff_perf))
    new_bin = possible_dvs[cutoff_idx]
    mult = 1 if not is_neg else -1
    # Do we need to handle close to zero cases here?
    if new_bin >= 1:
      new_bin = 1
      mult = -1*(periods-i)
    elif new_bin <= -1:
      new_bin = -1
      mult = periods-i
    while new_bin in bins:
      new_bin += 0.01*mult
    if not is_neg:
      bins.append(new_bin)
      cut_offs_perf.append(fits[cutoff_idx])
    else:
      bins.insert(0, new_bin)
      cut_offs_perf.insert(0, fits[cutoff_idx])

  for i in range(1, periods):
    curBin(i, periods, is_neg=False)
    if not combine_sides:
      curBin(i, periods, is_neg=True)
  bins += [1.01]
  if not combine_sides:
    bins = [-1.01] + bins
  # print("Closest dvs are: ", bins, "at perfms:", cut_offs_perf,
  #       "with min. perf:", min_perf, "and max perf L/R:", max_perf_l,
  #       max_perf_r)
  return bins

def rngByQuantile(df, *, periods, combine_sides, separate_zero):
  #_, bins = pd.qcut(df.DV.abs().rank(method='first'), periods, retbins=True)
  _, bins = pd.qcut(df.DV.abs(), periods, retbins=True, duplicates='drop')
  # print("Len:", bins)
  bins[-1] = 1.01
  if not combine_sides:
    if separate_zero:
      bins[0] = 0.01
      _min = bins[::-1]
    else:
      bins[0] = 0
      _min = -bins[::-1][:-1] # What would be a cleaner syntax?
    bins = np.concatenate([_min, bins])
  else:
    if not separate_zero:
      bins[0] = 0
    else:
      bin_offset_idx = 0 if bins[0] != 0 else 1
      bins = np.concatenate([[0, 0.01], bins[bin_offset_idx:]])
  # print("Returning bins:", bins)
  return bins
