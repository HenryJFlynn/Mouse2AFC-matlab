import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from report import analysis, utils as mainutils, splitdata

class VevHow:
  Mean = 'X'
  Median = 'D'
  Mode = 'o'

def WTAcrossSess(df, *, plot, save_figs, save_prefix):
  print(df.Name.unique())
  # Not used:
  # RDK_WT2: No catch trials
  # RDK_WT3: No catch trials
  # N3: Not enough confidence trials at all
  #df = df[~df.Name.isin(["N1"])]
  #df = df[df.Name == "wfThy2"]
  dfs_original = []
  dfs_corrected = []

  for name, animal_df in df.groupby(df.Name):
    animal_df = animal_df.copy() # Avoid copy-setting warning
    # Reject non-mode max-feedback-delay
    # animal_df.validFB = animal_df.validFB & \
    #                ((animal_df.GUI_RewardAfterMinSampling == 0) |
    #                 (animal_df.CenterPortRewAmount == 0))
    # animal_df.validFB = animal_df.validFB & \
    #                (animal_df.GUI_FeedbackDelayMax ==
    #                 animal_df[animal_df.validFB].GUI_FeedbackDelayMax.mode()[0])
    # if name == "Rbp4_M2_1":
    #   animal_df.validFB = animal_df.validFB & (animal_df.FeedbackTime <= 4.5)
    #   animal_df.validFB = animal_df.validFB & (animal_df.FeedbackTime > 1.5)
    # else:
    #   animal_df.validFB = animal_df.validFB & (animal_df.FeedbackTime <= 3.5)
    #   animal_df.validFB = animal_df.validFB & (animal_df.FeedbackTime >= 1.5)
    # animal_df.validFB = animal_df.validFB & \
    #                 (animal_df.GUI_FeedbackDelayTau ==
    #                 animal_df[animal_df.validFB].GUI_FeedbackDelayTau.mode()[0])
    # centerRewardDistr(animal_df[animal_df.validFB], name, save_figs, save_prefix)

    # reactVsWT(animal_df[animal_df.validFB], name, save_figs, save_prefix)
    # Restrict to time under median reaction-time
  #   animal_df.validFB = animal_df.validFB & \
  #  (animal_df.calcReactionTime <= animal_df[animal_df.validFB].calcReactionTime.median())
    # Reject really long waiting time
    # animal_df.validFB = animal_df.validFB & (animal_df.FeedbackTime < 10)

    grp_sess = mainutils.grpBySess(animal_df)
    print(f"{name} - Num sessions: {len(grp_sess)}")
    accepted_sess = []
    for sess_info, sess_df in grp_sess:
      sess_str = f"{sess_info[0].strftime('%Y_%m_%d')}_Sess{sess_info[1]}"
      print("Session info:", sess_str)
      accepted_df = plotSessWT(sess_df, plot=plot, animal_name=name,
                               sess_name=sess_str, save_figs=save_figs,
                               save_prefix=save_prefix)
      if accepted_df is not None:
        accepted_sess.append(sess_df)
        df_incorrect_trials, _, _ = dfByTrialType(accepted_df)
        sess_len = len(sess_df)
        all_conf_len = len(accepted_df)
        incorrect_conf_len = len(df_incorrect_trials)
        if incorrect_conf_len  > 20 and (all_conf_len/sess_len) > 0.2:
          #dfs_filtered.append(accepted_df)
          dfs_original.append(sess_df)
          dfs_corrected.append(accepted_df)
          print(f"Accepted sessions with feedback count: "
                f"{all_conf_len}/{sess_len} trials ("
                f"{incorrect_conf_len} incorrect)")
        else:
          print(f"Rejected sessions with feedback count: "
                f"{all_conf_len}/{sess_len} trials ("
                f"{incorrect_conf_len} incorrect)")
    if len(accepted_sess):
      trialsDistrib(pd.concat(accepted_sess), axes=plt.axes())
      plt.show()
      # PsycStim_axes = analysis.psychAxes(name)
      # analysis.psychAnimalSessions(pd.concat(accepted_sess), name,
      #                             PsycStim_axes, analysis.METHOD)
      # plt.show()

  #vevaiometric(df, vev_ax1, combine_sides=False)
  #vevaiometric(df, vev_ax3, combine_sides=True)
  def normalizeBySide(df):
    return pd.concat([normalizeWT(getSideDF(df, is_left=True)),
                      normalizeWT(getSideDF(df, is_left=False))])

  dfs_original_wt = pd.concat(dfs_original)
  dfs_original_norm = pd.concat(map(normalizeBySide, dfs_original))
  dfs_corrected_wt = pd.concat(dfs_corrected)
  dfs_corrected_norm = pd.concat(map(normalizeBySide, dfs_corrected))

  fig, vev_axs = plt.subplots(1, 4)
  fig.set_size_inches(2*analysis.SAVE_FIG_SIZE[0], 1*analysis.SAVE_FIG_SIZE[1])
  plotAllVev(dfs_original_norm, dfs_corrected_norm, vev_axs)
  if save_figs:
    names = df.Name.unique()
    animal_name = "All Animals" if len(names) > 1 else names[0]
    analysis.savePlot(f"{save_prefix}/{animal_name}/vev_mean")
  plt.show()

  return dfs_original_wt, dfs_original_norm, dfs_corrected_wt,\
         dfs_corrected_norm

def centerRewardDistr(df, animal_name, save_figs, save_prefix):
  ax = plt.axes()
  print("Len disabled center:", len(df[df.GUI_RewardAfterMinSampling == 0]))
  print("Center counts:")
  df = df.copy() # Avoid warning
  cntr_rew = df[df.GUI_RewardAfterMinSampling == 1].CenterPortRewAmount
  print(cntr_rew.value_counts())
  del cntr_rew # No longer needed
  df.loc[df.GUI_RewardAfterMinSampling == 0, 'CenterPortRewAmount'] = -1
  ax = plt.axes()
  _, bins, _ = ax.hist(df.CenterPortRewAmount)
  ax.set_xlabel("CenterRewardAmount")
  print("Bins range:", bins)
  ax2 = ax.twinx()
  for bin_idx in range(len(bins) - 1):
    bin_left = bins[bin_idx]
    bin_right = bins[bin_idx+1]
    df_bin = df[(bin_left <= df.CenterPortRewAmount) &
                (df.CenterPortRewAmount < bin_right)]
    x_mid = (bin_left + bin_right)/2
    X_PORTION = (bin_right - bin_left) * 0.3
    df_incorrect, df_correct_fb, df_correct_catch = dfByTrialType(df_bin)
    for sub_df, edg_clr, mrk_clr, x, label in [
              (df_incorrect, 'r', 'r', x_mid - X_PORTION, "Error"),
              (df_correct_fb, 'g', 'g', x_mid, "Correct"),
              (df_correct_catch, 'g', 'w', x_mid + X_PORTION, "Catch Correct")]:
      if not len(sub_df):
        continue
      Xs = [x]*len(sub_df)
      ax2.scatter(Xs, sub_df.calcReactionTime, c=mrk_clr, edgecolors=edg_clr,
                  label=label)
      ax2.scatter(Xs[0], sub_df.calcReactionTime.median(), s=8, c='k',
                  label="Median")
    label_once = True
  for quantile_val in [0.75, 0.9, 0.95, 0.99]:
    ax2.axhline(df.calcReactionTime.quantile(quantile_val), linestyle="dashed",
                color='gray')
  ax2.axhline(df.calcReactionTime.quantile(0.5), linestyle="dashed",
              color='cyan')
  for quantile_val in [0.01, 0.1, 0.25]:
    ax2.axhline(df.calcReactionTime.quantile(quantile_val), linestyle="dashed",
                color='blue')
  for zscore_rank in [2, 3]:
    df_filtered = analysis.filterZScore(zscore_rank, df)
    ax2.axhline(df_filtered.calcReactionTime.max(), linestyle="dotted",
                color='purple', label=f"Z-score (rank-{zscore_rank})")
  ax.set_xlabel("Center Reward Amount")
  ax.set_ylabel("Trial Count")
  ax2.set_ylabel("Reaction Time")
  legendUnique(ax, ax2, fontsize='x-small')
  ax.set_title(df.Name.unique()[0])
  if save_figs:
    analysis.savePlot(f"{save_prefix}/{animal_name}/cntrRewardDistr")
  plt.show()

def reactVsWT(df, animal_name, save_figs, save_prefix):
  df_incorrect, df_correct_fb, df_correct_catch = dfByTrialType(df)
  # cut_off = max(df_incorrect.calcReactionTime.quantile(0.99),
  #               df_correct_catch.calcReactionTime.quantile(0.99))
  catch_trials_df = pd.concat([df_incorrect, df_correct_catch])
  if not len(catch_trials_df):
    print(f"Not enough trials for {animal_name}. Returning")
    return

  if catch_trials_df.MinSample.mean() > catch_trials_df.ST.mean()*0.7:
    rt_str = "calcReactionTime"
  else:
    rt_str = "ST"
  # catch_trials_df = catch_trials_df[catch_trials_df[rt_str] >= catch_trials_df[rt_str].median()]
  reaction_time_col = catch_trials_df[rt_str]
  #[(0.75, "cyan"), (0.9, "blue"), (0.95, "purple"), (1, "brown")]:
  cut_off = reaction_time_col.quantile(0.9)
  print("Cut off:", cut_off)

  ax = plt.axes()
  for sub_df, color in [(df_incorrect, 'r'), (df_correct_catch, 'g')]:
    ax.scatter(sub_df.FeedbackTime, sub_df[rt_str], color=color, s=3)
  ax.set_xlabel("Waiting Time")
  ax.set_ylabel("Reaction Time" if rt_str == "ST" else "Decision Time")
  ax.axhline(catch_trials_df[rt_str].median(), linestyle="dashed",
             color='gray', label="Median")
  ax.axhline(catch_trials_df[rt_str].mean(), linestyle="dotted",
             color='purple', label="Mean")
  ax.axhline(catch_trials_df[rt_str].min(), linestyle="-", color='k',
             label="Limits")
  ax.axhline(catch_trials_df[rt_str].max(), linestyle="-", color='k')
  for quantile, color in [(1, 'b')]:
    sub_df = catch_trials_df[
                       reaction_time_col < reaction_time_col.quantile(quantile)]
    linFitFn = linearFit(sub_df.FeedbackTime, sub_df[rt_str])
    Xs_fit = np.linspace(0, catch_trials_df.FeedbackTime.max()+1)
    Ys_fit = linFitFn(Xs_fit)
    quantile_str = " ({quantile:.2f} quantile)" if quantile < 1 else ""
    ax.plot(Xs_fit, Ys_fit, color=color, label=f"Lin-Fit{quantile_str}")
  ax.legend(loc="upper right", fontsize="x-small")
  ax.set_ylim(bottom=0, top=cut_off)
  ax.set_title(df.Name.unique()[0])
  if save_figs:
    analysis.savePlot(f"{save_prefix}/{animal_name}/RTvsWT")
  plt.show()

def initialFilter(name, animal_df):
  if name == "RDK_Thy2":
    print("Processing", name)
    animal_df = animal_df[animal_df.Date >= dt.date(2019,5,22)]
    animal_df = animal_df[animal_df.Date <= dt.date(2019,6,26)]
    animal_df = animal_df[animal_df.Date != dt.date(2019,6,5)]
    animal_df = animal_df[animal_df.Date != dt.date(2019,6,7)]
    animal_df = animal_df[animal_df.Date != dt.date(2019,6,10)]
    animal_df = animal_df[animal_df.Date != dt.date(2019,6,24)]
    #df = df[df.Date >= dt.date(2019,5,22)]
  elif name == "RDK_Thy1":
    animal_df = animal_df[animal_df.Date >= dt.date(2019,3,12)]
    animal_df = animal_df[animal_df.Date <= dt.date(2019,5,31)]
  else:
    animal_df = animal_df[animal_df.Date >= dt.date(2019,6,1)]
  animal_df.validFB = animal_df.validFB & \
                   (animal_df.GUI_FeedbackDelayMax ==
                    animal_df[animal_df.validFB].GUI_FeedbackDelayMax.mode()[0])
  valid_sessions = []
  for sess_info, sess_df in mainutils.grpBySess(animal_df):
    if len(sess_df[sess_df.validFB & (sess_df.CatchTrial == True) &
                  (sess_df.ChoiceCorrect == True)]) > 2:
      valid_sessions.append(sess_df)
  animal_df = pd.concat(valid_sessions)
  animal_valid_df,  = animal_df[animal_df.validFB]
  animal_non_valid_df = animal_df[~animal_df.validFB]
  #animal_valid_df_filtered = filterWTByDV(animal_valid_df, combine_sides=False)
  animal_valid_df_filtered = animal_valid_filtered
  rt_quantile = animal_valid_filtered.calcReactionTime.quantile(0.75)
  animal_valid_filtered.validFB = animal_valid_filtered.validFB & \
                          (animal_valid_filtered.calcReactionTime < rt_quantile)
  animal_valid_df.loc[
    ~animal_valid_df.index.isin(animal_valid_df_filtered.index),
    'validFB'] = False
  animal_df = pd.concat([animal_valid_df, animal_non_valid_df])
  return animal_df


def normalizeWT(df):
  df_incorrect_trials, _, df_correct_catch = dfByTrialType(df)
  df_catch = pd.concat([df_incorrect_trials, df_correct_catch])
  fb_time = df_catch.FeedbackTime
  if fb_time.min() < 0:
    print(f"***********DF has {len(fb_time[fb_time<0])}/{len(fb_time)} with "
           "-ve FeedbackTime value")
  fb_time = (fb_time-fb_time.min())/(fb_time.max()-fb_time.min())
  df_catch.FeedbackTime = fb_time
  return df_catch

def plotSessWT(df, *, plot, animal_name, sess_name, save_figs, save_prefix):
  if plot:
    fig = plt.figure(constrained_layout=True)
    fig.set_size_inches(2.5*analysis.SAVE_FIG_SIZE[0],
                        2*analysis.SAVE_FIG_SIZE[1])
    gs = fig.add_gridspec(2, 5)
    ax = fig.add_subplot(gs[0, :2])
    corrected_ax = fig.add_subplot(gs[0, 2:4])
    vev_axs = [fig.add_subplot(gs[1, i]) for i in range(4)]
    psych_axes = fig.add_subplot(gs[0, 4])
    psych_axes_corrected = fig.add_subplot(gs[1, 4])

  # Filter outliers
  df_left_filtered = filterOutliers(getSideDF(df, is_left=True))
  df_right_filtered = filterOutliers(getSideDF(df, is_left=False))
  df_filtered = pd.concat([df_left_filtered, df_right_filtered])
  # Linear regression
  corrected_df = calcCorrectedWT(df_filtered,
                                 (ax, corrected_ax) if plot else None)
  if plot:
    plotWTDots(ax, df, alpha=1)
    if corrected_df is not None:
      plotAllVev(df, corrected_df, vev_axs)

  if plot:
    feedback_min = [df.FeedbackTime.min()] * len(df)
    max_trials_seen = df.TrialNumber.max()
    # ax.fill_between(np.arange(1, max_trials_seen+1), feedback_min,
    #                 df.GUI_FeedbackDelayMax, color='b', alpha=0.1,
    #                 where=(df.validFB == True),  label="Included Feedback")
    # ax.fill_between(np.arange(1, max_trials_seen+1), feedback_min,
    #                 df.GUI_FeedbackDelayMax, color='r', alpha=0.1,
    #                 where=(df.validFB == False), label="Not Included Feedback")
    ax2 = ax.twinx()
    ax2.scatter(df.TrialNumber, df.calcReactionTime, marker='x', c='k', s=4,
                label="Reaction Time")
    #ewd_df = df[df.EarlyWithdrawal==True]
    EWD_Win_Size = 20
    ewd_rate = df.EarlyWithdrawal.rolling(EWD_Win_Size, center=True,
                                          min_periods=1).mean()
    ewd_rate *= df.calcReactionTime.max()
    ax2.plot(df.TrialNumber, ewd_rate, marker='D', c='purple', markersize=4,
             alpha=0.1, label=f"EWD Rate ({EWD_Win_Size} rolling win)")
    ax2.set_ylabel("Reaction Time (sec)")
    handles, labels = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(handles + handles2, labels + labels2, loc='upper left',
              fontsize='x-small')
    ax = setupAxes(ax)
    corrected_ax = setupAxes(corrected_ax)
    corrected_ax.set_xlim(ax.get_xlim())
    corrected_ax.set_ylim(ax.get_ylim())
    for vev_ax in vev_axs[2:]:
      vev_ax.set_ylim(vev_axs[0].get_ylim())
      vev_ax.set_title("Filtered " + vev_axs[0].get_title(), fontsize='x-small')

    animal_name = "Many Animals" if len(df.Name.unique()) > 1 \
                                 else df.Name.unique()[0]
    psych_axes = analysis.psychAxes(animal_name, psych_axes)
    analysis.psychAnimalSessions(df, animal_name, psych_axes, analysis.METHOD)
    # analysis.trialRate(df, ax=psych_axes_corrected,
    #                    max_sess_time_lim_bug=60*60*100, IQR_filter=False,
    #                    num_days_per_clr=1)
    trialsDistrib(df, axes=psych_axes_corrected)
    # if corrected_df is not None:
    #   psych_axes_corrected = analysis.psychAxes(animal_name,
    #                                             psych_axes_corrected)
    #   analysis.psychAnimalSessions(corrected_df, animal_name,
    #                                psych_axes_corrected, analysis.METHOD)
    if save_figs:
      analysis.savePlot(f"{save_prefix}/{animal_name}/ssns/{sess_name}_confd")
    plt.show()
  return corrected_df

def setupAxes(ax):
  ax.set_xlabel("Trial Number")
  ax.set_ylabel("Waiting Time (Sec)")
  ax.set_xlim(left=0)
  ax.set_ylim(bottom=0)
  return ax

def filterOutliers(df):
  df_incorrect, df_correct_fb, df_correct_catch = dfByTrialType(df)
  df_all_catch = pd.concat([df_incorrect, df_correct_catch])
  if len(df_all_catch):
    df_all_catch = analysis.filterQuantile(0.05, 0.95, group=df_all_catch)
    return pd.concat([df_all_catch, df_correct_fb])
  else:
    return df

def calcCorrectedWT(df, axes_if_plot):
  if axes_if_plot:
    plot = True
    ax, corrected_ax = axes_if_plot
  else:
    plot = False

  df_incorrect, df_correct_fb, df_correct_catch = dfByTrialType(df)
  df_catch = pd.concat([df_incorrect, df_correct_catch])
  if len(df_catch[df_catch.validFB]) == 0:
    return

  if plot:
    ax.axhline(df_catch.FeedbackTime.max() + 0.1, color="k")
    ax.axhline(df_catch.FeedbackTime.min() - 0.1, label=f"Quantile 5% +/-",
               color="k")

  orig_TrialNumber = df.TrialNumber
  fb_md = df_catch[df_catch.validFB].GUI_FeedbackDelayMax.mode()[0]
  all_similar_catch_error = df_catch[(df_catch.GUI_FeedbackDelayMax == fb_md) &
                                     (df_catch.ChoiceCorrect == False) &
                                     (df_catch.GUI_CatchError == True)]
  del fb_md # No longer needed
  # Reconstruct all the data after we removed the filtered data
  df = pd.concat([df_catch[df_catch.validFB],
                  df_correct_fb[df_correct_fb.validFB]])
  # Make a linear fit using all the the catch error data that has the same GUI
  # Feedback delay max
  # linFitFn = WTLinearFit(all_similar_catch_error)
  linFitFn = linearFit(all_similar_catch_error.TrialNumber,
                       all_similar_catch_error.FeedbackTime)
  linfit_line = linFitFn(orig_TrialNumber)
  if plot:
    ax.plot(orig_TrialNumber, linfit_line, color='gray', alpha=0.4,
            label="Linea Fit")
  mean_catch_point = linFitFn(all_similar_catch_error.TrialNumber.mean())
  print("Mean error catch trial number: ",
        all_similar_catch_error.TrialNumber.mean(), "- pred. val:",
        mean_catch_point)
  horz_line = np.array([mean_catch_point]*len(orig_TrialNumber))
  if plot:
    ax.plot(orig_TrialNumber, horz_line, color='cyan', alpha=0.4,
            label="Corrected Linear Fit")

  #display("Line line:", linfit_line.shape)
  #display("Horz line:", horz_line.shape)
  div_line = (horz_line/linfit_line) - 1
  #display("Div line:", div_line)
  ##factors = div_line[df_catch.TrialNumber-1]
  ##FBT = df_catch["FeedbackTime"]
  ##df_catch["FeedbackTime"] = FBT + (FBT*factors)
  df_corrected = pd.concat([df_catch[df_catch.validFB],
                            df_correct_fb[df_correct_fb.validFB]])
  if plot:
    plotWTDots(ax, pd.concat([df_catch, df_correct_fb]), alpha=0.3)
    plotWTDots(corrected_ax, df_corrected, alpha=1)
  # ZSCORE_RANK = 2
  # from analysis import filterZScore
  # accepted_df = filterZScore(zscore_rank=ZSCORE_RANK, group=accepted_df)
  # corrected_ax.axhline(accepted_df.FeedbackTime.max() + 0.1, color="gray")
  # corrected_ax.axhline(accepted_df.FeedbackTime.min() - 0.1,
  #                      label=f"Z-Score rank = {ZSCORE_RANK}", color="gray")
  return df_corrected


def plotWTDots(ax, df, alpha):
  df_incorrect, df_correct_fb, df_correct_catch = dfByTrialType(df)
  for sub_df, edg_clr, mrk_clr in  [(df_incorrect, 'r', 'r'),
                                    (df_correct_fb, 'g', 'g'),
                                    (df_correct_catch, 'g', 'w')]:
    ax.scatter(sub_df.TrialNumber, sub_df.FeedbackTime,
               c=mrk_clr, edgecolors=edg_clr, alpha=alpha)


def dfByTrialType(df):
  df_correct_catch = df[(df.ChoiceCorrect == True) & (df.CatchTrial == True)]
  df_correct_fb = df[(df.ChoiceCorrect == True) & (df.CatchTrial == False)]
  df_incorrect = df[df.ChoiceCorrect == False]
  return df_incorrect, df_correct_fb, df_correct_catch

def plotAllVev(dfs_original, dfs_corrected, rows_axs4, vev_hows=[VevHow.Mean]):
  VevHow_by_values = dict([(val, key) for (key, val) in vars(VevHow).items()
                           if not key.startswith('__')])
  from matplotlib.axes import Axes
  if isinstance(rows_axs4[0], Axes):
    rows_axs4 = [rows_axs4]
  for how, axs4 in zip(vev_hows, rows_axs4):
    vevaiometric(dfs_original, axs4[0], combine_sides=False, vev_hows=[how])
    vevaiometric(dfs_original, axs4[1], combine_sides=True, vev_hows=[how])
    vevaiometric(dfs_corrected, axs4[2], combine_sides=False, vev_hows=[how])
    vevaiometric(dfs_corrected, axs4[3], combine_sides=True, vev_hows=[how])
    if len(dfs_original.Name.unique()) > 1:
      [ax.set_title("Many Animals Vevaiometric") for ax in axs4]
    for ax in axs4:
      ax.set_title(f"{ax.get_title()} ({VevHow_by_values[how]})",
                   fontdict={"fontsize":"xx-small"})

def getSideDF(df, is_left):
  is_right = not is_left
  return df[df.ChoiceLeft == is_left]
  # return df[( (df.ChoiceCorrect == True) & (df.ChoiceLeft == is_left) ) | \
  #           ( (df.ChoiceCorrect == False) & (df.ChoiceLeft == is_right) )]

def trialsDistrib(df, axes):
  df_incorrect, df_correct_fb, df_correct_catch = dfByTrialType(df)
  all_catch_trials = pd.concat([df_incorrect, df_correct_catch])

  lower, upper = df.FeedbackTime.min(), df.FeedbackTime.max()
  # NUM_BINS=int((upper-lower)*10)
  #axes.hist(df_correct_fb.FeedbackTime,range=(lower,upper),bins=NUM_BINS,
  #          histtype='step',label="Water Delivery", color='b')

  #axes.hist(all_catch_trials.FeedbackTime,range=(lower,upper),bins=NUM_BINS,
  #          histtype='step',label="Catch Trials", color='k')
  from scipy.stats import gaussian_kde
  from sklearn.neighbors.kde import KernelDensity
  for data, label, color in [(df_correct_fb, "Water delivery", 'b'),
                             #(all_catch_trials, "Catch Trials All", 'k'),
                             (df_incorrect, "Catch Incorrect", 'r'),
                             (df_correct_catch, "Catch Correct", 'g')]:
    if not len(data.FeedbackTime):
      continue
    # Every half a second
    BIN_EVERY = 0.5 # BIN_EVERY
    num_bins = int((data.FeedbackTime.max()-data.FeedbackTime.min())/BIN_EVERY)
    num_bins = max(num_bins, 1)
    counts, bins, patches = axes.hist(data.FeedbackTime,
              range=(data.FeedbackTime.min(),data.FeedbackTime.max()),
              bins=num_bins, histtype='step',color=color,alpha=0.4)

    median = data.FeedbackTime.median()
    axes.axvline(median, linestyle="dashed",
                 label=f"{label} median (x={median:.2f})", color=color)
    mode = bins[np.where(counts == counts.max())[0]].mean() + (BIN_EVERY/2)
    axes.axvline(mode, linestyle="dotted", label=f"{label} mode (x={mode:.2f})",
                 color=color)
    xs = np.linspace(data.FeedbackTime.min()-0.3,
                     data.FeedbackTime.max() + 2,
                     10000)
    label_count = f"{label} ({len(data.FeedbackTime):,} points)"
    BANDWIDTH=0.2
    if True:
      density = gaussian_kde(data.FeedbackTime)
      density.covariance_factor = lambda : BANDWIDTH
      density._compute_covariance()
      y_data = density(xs)
      y_data *= counts.max() / y_data.max() # Find a good scaling point
      axes.plot(xs,y_data,color=color,label=label_count)
    if False:
      kde = KernelDensity(kernel='exponential', bandwidth=BANDWIDTH).fit(
                               data.FeedbackTime.to_numpy().reshape(-1,1))
      # score_samples() returns the log-likelihood of the samples
      y_data = np.exp(kde.score_samples(xs.reshape(-1,1)))
      y_data *= counts.max() / y_data.max()
      axes.plot(xs,y_data,color=color,label=label_count)
  axes.legend(loc='upper left', bbox_to_anchor=(1.02, 1), prop={'size':'x-small'})
  axes.set_xlabel("Waiting Time (s)")
  axes.set_ylabel("Trial Count")
  axes.set_xlim(0, 10)
  axes.set_xticks(np.arange(0, 10, 1))


def vevaiometric(df, ax, combine_sides, vev_hows=[VevHow.Mean]):
  MIN_NUM_POINTS_PER_DV = 5
  # Handle normalized and non-normalized feedback time
  MODE_BIN_EVERY = 0.05 if df.FeedbackTime.max() == 1 else 0.25
  df = df[df.validFB]
  df_incorrect, _, df_correct_catch = dfByTrialType(df)
  df_incorrect = df_incorrect.copy() # Remove copy warning
  df_correct_catch = df_correct_catch.copy() # Remove copy warning

  def plotSide(choice_df, color, label, count):
    Xs = []
    Ys = {VevHow.Mean:[],
          VevHow.Median:[],
          VevHow.Mode:[]}
    Ys_std = {VevHow.Mean:[],
              VevHow.Median:[],
              VevHow.Mode:[]}

    def calcPointY(dv_df, how):
      if how == VevHow.Mean:
        pt = dv_df.FeedbackTime.mean()
        std = dv_df.FeedbackTime.std()
      elif how == VevHow.Median:
        pt = dv_df.FeedbackTime.median()
        std = None
      elif how == VevHow.Mode:
        hist, bins_edges = np.histogram(dv_df.FeedbackTime, range=(0,19),
                                        bins=int(19/MODE_BIN_EVERY))
        # print(f"Bins edges for dv={dv_df.DV.mean()}: {bins_edges} -
        #      Hist: {hist}")
        mode = np.median(
                 bins_edges[np.where(hist == hist.max())[0]]) + MODE_BIN_EVERY/2
        # print("Mode:", mode)
        pt = mode
        std = None
      Ys[how].append(pt)
      Ys_std[how].append(std)

    if not len(choice_df):
      return
    for dv_range, single_dv, dv_df in splitdata.byDV(choice_df,
                                       combine_sides=combine_sides, periods=20):
      if len(dv_df) < MIN_NUM_POINTS_PER_DV:
        continue
      Xs += [dv_range.mid]
      #Ys += [dv_df.FeedbackTime.mean()]
      #Ys_std += [dv_df.FeedbackTime.std()]
      [calcPointY(dv_df, how) for how in vev_hows]
      scatter_dv = dv_df.DV
      if combine_sides:
        scatter_dv = scatter_dv.abs()
      ax.scatter(scatter_dv, dv_df.FeedbackTime, color=color, s=3, alpha=0.7)
    if sum(Xs) == 0:
      return
    done_once = False
    for how in vev_hows:
      label_ = f"{label} ({count} Trials)" if label and not done_once else None
      linestyle = "dashed" if how == VevHow.Mean else "dashed"  \
                           if how == VevHow.Median else "dotted"
      ax.plot(Xs, Ys[how], linestyle=linestyle, color=color, marker=how,
              markersize=5, label=label_)
      done_once = True
    linFitFn = linearFit(Xs, Ys[how])#choice_df.DV, choice_df.FeedbackTime)
    dv_direction = -1 if not combine_sides and (choice_df.DV < 0).any() else 1
    x_linfit_line = np.linspace(0, dv_direction, 100)
    y_linfit_line = linFitFn(x_linfit_line)
    del linFitFn
    ax.plot(x_linfit_line, y_linfit_line, color=color)

  df_incorrect.DV *= -1 # A hack to get it to point to the poked-in direction
  for choice_df, color, label in [
    (df_incorrect, 'r', f"Incorrect{' (inv.)' if not combine_sides else ''}"),
    (df_correct_catch, 'g', "Correct Catch")]:
    if not combine_sides:
      plotSide(choice_df[choice_df.DV <= 0], color, label, len(choice_df))
      plotSide(choice_df[choice_df.DV >= 0], color, label, len(choice_df))
    else:
      plotSide(choice_df, color, label, len(choice_df))

  xmin = -0.05 if combine_sides else -1.05
  ax.set_xlim(xmin, 1.05)
  x_ticks=np.arange(0 if combine_sides else -1 ,1.1,0.4)
  def cohrStr(tick):
    cohr = int(round(100*tick))
    return "{}%{}".format(abs(cohr),'R' if cohr<0 else "" if cohr==0 else 'L')
  x_labels=list(map(cohrStr, x_ticks))
  ax.set_xticks(x_ticks)
  ax.set_xticklabels(x_labels)
  ax.set_xlabel("RDK Coherence")
  ax.set_ylabel("Waiting Time (s)")
  ax.set_title("Vevaiometric - " + " ".join(df.Name.unique()))
  # Remove duplicate legend labels
  handles, labels = ax.get_legend_handles_labels()
  by_label = dict(zip(labels, handles))
  ax.legend(by_label.values(), by_label.keys(), loc='upper right',
            prop={'size':'small'}, ncol=1)
  ax.axvline(x=0, color='gray', linestyle='dashed', zorder=-1)

def linearFit2(x_data, y_data):
  from sklearn.linear_model import LinearRegression
  x, y = x_data.values.reshape((-1, 1)), y_data
  model = LinearRegression().fit(x, y)
  scored = model.score(x, y)
  def predict1d(x_data_pts):
    if isinstance(x_data_pts, pd.Series):
      val = x_data_pts.values.reshape((-1, 1))
    else:
      val = np.array([x_data_pts]).reshape((-1, 1))
    return model.predict(val).squeeze()
  return predict1d

def linearFit(x_data, y_data):
  # a, b = None, None
  # def predict1d(x):
  #   return (a * x) + b
  # a,b = np.polyfit(x, y, 1)
  # from scipy import optimize
  # fit_y_fit_a, fit_y_fit_b = optimize.curve_fit(linear_fit, x_data, y_data)[0]
  coef = np.polyfit(x_data, y_data, 1)
  predict1dFn = np.poly1d(coef)
  return predict1dFn

def filterWTByDV(df, combine_sides):
  ZSCORE_RANK = 2
  res_df = []
  from report import analysis
  for dv_range, dv_single_point, dv_df  in splitdata.byDV(df,
                                                   combine_sides=combine_sides):
    df_incorrect, df_correct_fb, df_correct_catch = dfByTrialType(df)
    df_incorrect = analysis.filterZScore(ZSCORE_RANK, df_incorrect)
    df_correct_catch = analysis.filterZScore(ZSCORE_RANK, df_correct_catch)
    res_df += [df_incorrect, df_correct_fb, df_correct_catch]
  return pd.concat(res_df)

def legendUnique(ax, ax2=None, **kargs):
  handles, labels = ax.get_legend_handles_labels()
  handles2, labels2 =  ax2.get_legend_handles_labels() if ax2 else ([], [])
  by_label = dict(zip(labels+labels2, handles+handles2))
  ax.legend(by_label.values(), by_label.keys(), **kargs)
