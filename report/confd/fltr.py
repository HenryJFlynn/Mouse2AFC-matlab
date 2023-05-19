import pandas as pd
from report.definitions import ExperimentType
from report.utils import grpBySess

_sess_used, _sess_dropped = 0, 0
def filterInvalidSessions(df, *, min_easiest_perf, exp_type):
  # df = df[df.Name == "RDK_WT1"]
  global _sess_used, _sess_dropped
  _sess_dropped = 0 # TODO: Remove global variables
  _sess_used = 1
  df.loc[:, "keep"] = False
  df.loc[:, "validFB"] = False
  # I get the following error if I used the below line:
  # 'cannot reindex from a duplicate axis' and
  # 'AttributeError: 'DataFrame' object has no attribute 'Name''
  # rather than fixing it, I'll work around it for now by simply looping
  # df = grpBySess(df).apply(_fltrSSn, exp_type=exp_type,
  #                          min_easiest_perf=min_easiest_perf)
  dfs = []
  for _, grp in grpBySess(df):
    dfs.append(_fltrSSn(grp, exp_type=exp_type,
                        min_easiest_perf=min_easiest_perf))
  df = pd.concat(dfs)
  del dfs # We no longer needed it
  df = df[df.keep]
  df.drop(columns="keep", inplace=True)
  print(f"Dropped {_sess_dropped:,}/{_sess_used:,} sessions")
  print(f"Valid Trials: {len(df[df.validFB]):,}/Total: {len(df):,}")
  return df

def _fltrSSn(ssn_df, exp_type, min_easiest_perf):
  validFB = _trialConds(ssn_df, exp_type=exp_type)
  if validFB.any():
    validFB = validFB & _sessConds(ssn_df, exp_type=exp_type,
                                   min_easiest_perf=min_easiest_perf)
    if validFB.any():
      ssn_df = ssn_df.copy()
      ssn_df.loc[:, "validFB"] = validFB
      # print(f"Len ssn_df: {len(ssn_df[ssn_df.validFB])}")
      ssn_df.loc[:, "keep"] = True
  # By default, ssn_df[validFB] and ssn_df[keep] already exist and are False
  return ssn_df

def _trialConds(df, exp_type):
  ct_tn = df[df.CatchTrial == True].TrialNumber
  return (
      # ( (30 <= df.TrialNumber) & (df.TrialNumber <= df.MaxTrial - 30) ) &
      ( (ct_tn.min() <= df.TrialNumber) & (df.TrialNumber <= ct_tn.max()) ) &
      ( df.calcMovementTime < 1) &
      # ( df.GUI_FeedbackDelayMax >= 2 ) & # We will pick up the mode later
      ( (df.GUI_FeedbackDelaySelection == 3) & (df.GUI_CatchError == True) ) &
      ( (0.5 < df.FeedbackTime) & (df.FeedbackTime < 19) ) &
      ( ~df.Name.isin(["Dummy Subject", "HomeCageHabutate"]) ) &
      ( df.GUI_ExperimentType == exp_type ) &
      ( df.Difficulty3.notnull() ) # At least 3 difficulties exist
      #( (65 < df.SessionPerformance) & (df.SessionPerformance < 85) )
  )

def _sessConds(df, exp_type, min_easiest_perf):
  global _sess_used, _sess_dropped # TODO: Fix this, remove global variables
  cct = df[df.CatchTrial == True]
  cct_choice = cct[cct.ChoiceCorrect.notnull()]
  if not len(cct_choice):
    return False
  ##
  _sess_used += 1
  trial_difficulty_col = df.DV.abs() * 100
  if exp_type != ExperimentType.RDK: # TODO: Check this part
    trial_difficulty_col = (trial_difficulty_col/2)+50
  easiest_diff = df[trial_difficulty_col == df.Difficulty1]
  if len(easiest_diff):
    easiest_perf = (len(easiest_diff[easiest_diff.ChoiceCorrect == 1]) /
                    len(easiest_diff))
    #print("Easiest perf:", easiest_perf)
  else:
    easiest_perf = -1
  easiest_perf *= 100
  if easiest_perf < min_easiest_perf:
    _sess_dropped += 1
    print(f"Bad performance ({easiest_perf:.2f}%) for {df.Name.iloc[0]} - "
          f"{df.Date.iloc[0]}-Sess{df.SessionNum.iloc[0]} - "
          f"Len: {len(df)}")
  # else:
  #   print("Easiest perf:", easiest_perf)
  ##
  return (
      #( (len(cct) > 2) & (cct.TrialNumber.min() <= df.TrialNumber) &
      #  (df.TrialNumber <= cct.MaxTrial) ) &
      (easiest_perf >= min_easiest_perf)
  )