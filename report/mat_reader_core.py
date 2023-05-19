from msilib.schema import Error
from .matreader import states
from .matreader.states import States, StartEnd
from .matreader.processrawevents import (_getTrialsPorts,
                                         _extractTrialsPortsEvents)
from .definitions import StimAfterPokeOut
import calendar
from collections import defaultdict, deque
import datetime as dt
import glob
import itertools as it
import ntpath
import numpy as np
import pandas as pd
import pathlib
from scipy.io import loadmat
import sys
import traceback

MIN_SESSION_TRIALS_LEN = 10
MIN_DF_COLS_DROP = ["States", "drawParams","rDots", "visual", "Subject", "File",
                    "Protocol", "OptoEnabled_stimulus_delivery", ]
# GUI_OmegaTable is important but has an a special a treatment.
# See processTrial() function for more details.
IMP_GUI_COLS = ["GUI_ExperimentType", "GUI_SecExperimentType",
    "GUI_StimAfterPokeOut", "GUI_CatchError", "GUI_PercentCatch",
    "GUI_FeedbackDelayMax","GUI_FeedbackDelayTau",
    "GUI_MinSampleType", "GUI_MinSample", "GUI_MinSampleMin",
    "GUI_MinSampleMax", "GUI_RewardAfterMinSampling", "GUI_StimulusTime",
    "GUI_FeedbackDelaySelection", "GUI_CalcLeftBias", "GUI_MouseState",
    "GUI_MouseWeight", "GUI_OptoBrainRegion", "GUI_OptoStartState1",
    "GUI_LeftBiasVal", "GUI_OptoEndState1", "GUI_OptoEndState2",
    #GUI_OptoOr2P,
    "GUI_OptoMaxTime", "GUI_OptoStartDelay",
    ]
sys.modules["states"] = states # A bad hak needed for old classes
_months_3chars = list(calendar.month_abbr)
# Any value would do to uniquely identify the return
_BAD_FILE_NAME_FORMAT = "Bad File Name"
_BAD_FILE_STRUCTURE = "Bad File Structure"
_BAD_FILE_FEW_TRIALS = "Unaccepted Few Trials Session"
_TEMP_STORED_FILE = "Temp file - ignored"
_SKIPPED_SESS = "Session should be skipped"
def decomposeFilePathInfo(filepath):
  filename = ntpath.basename(filepath)
  # Check the file is not a repeated file from one-drive
  # Good name e.g: M5_Mouse2AFC_Oct30_2018_Session1.mat
  filename = filename.rstrip(".mat")
  try:
    if "session" not in filename.lower():
      raise ValueError()
    mouse_name, protocol, month_day, year, session_num = filename.rsplit("_", 4)
    is_ver2 = False
  except ValueError:
    # Maybe it's a version 2 filename?
    # Good name e.g: Dummy Subject_Mouse2AFC_20200818_150459
    try:
      mouse_name, protocol, date, time = filename.rsplit("_", 3)
      is_ver2 = True
    except ValueError:
      return None
  if not is_ver2:
    if len(month_day) != 5: # e.g Oct30
      return None
    month, day = month_day[:-2], month_day[-2:]
    try:
      day = int(day)
      month = _months_3chars.index(month)
      year = int(year)
      session_num = int(session_num.lower().lstrip("session")) # e.g: Session1
    except ValueError:
      return None
  else:
    try:
      year, month, day = int(date[0:4]), int(date[4:6]), int(date[6:])
      # TODO: Time is currently being treated as session num, fix it
      session_num = time[:3]
    except ValueError:
      return None
  return mouse_name, protocol, (year, month, day), session_num

def uniqueSessID(decomposed_name):
  mouse_name, protocol, (year, month, day), session_num = decomposed_name
  return (mouse_name, dt.date(year=year, month=month, day=day), session_num)

def _extractGUI(data, max_trials, is_mini_df, new_data_format):
  diff_arrs = {"Difficulty1": [], "Difficulty2":[], "Difficulty3":[],
               "Difficulty4": []}
  def processTrial(trial_gui, gui_dict):
    if not new_data_format:
      trial_gui = trial_gui.GUI
    for param_name in dir(trial_gui):
      if param_name.startswith("__") or "_fieldnames" in param_name:
        continue
      elif param_name == "OmegaTable":
        table = getattr(trial_gui, param_name)
        # Non-zero omega-probabilities the ones that user chose to activate
        if trial_gui.ExperimentType == 4:
          if hasattr(table, "RDK"):
            src_table = table.RDK
          else:
            src_table = table.Omega
            table.Omega = (table.Omega - 50)*2
        else:
          src_table = table.Omega
        diffs = src_table[np.where(table.OmegaProb)[0]]
        # Ensure it's sorted in descending order
        diffs[::-1].sort()
        for i in range(4): # 0 -> 3
          diff_val = diffs[i] if i < len(diffs) else np.nan
          diff_arrs["Difficulty{}".format(i+1)].append(diff_val)
      if is_mini_df and ("GUI_" + param_name) not in IMP_GUI_COLS:
        continue
      else:
        param_val = getattr(trial_gui, param_name)
        if param_name == "StimAfterPokeOut" and \
           param_val == StimAfterPokeOut.NotUsedMatlab:
           param_val = 0 # i.e StimAfterPokeOut.NotUsed
        gui_dict["GUI_" + param_name].append(param_val)
  gui_dict = defaultdict(list)
  deque(map(lambda trial_gui: processTrial(trial_gui, gui_dict),
            data.TrialSettings[:max_trials]))
  #print("GUI dict:", gui_dict)
  # print("Diff arrays:", diff_arrs)
  #feedback_type = list(map(lambda param:param.FeedbackDelaySelection,
  #                        data.TrialSettings))
  #catch_error = list(map(lambda param:param.CatchError,
  #                    data.TrialSettings))
  # Modifying a dictionary while looping on it is dangerous, however
  # hopefully it should be okay because we are just reassigning values
  for key in gui_dict.keys():
    gui_dict[key] = gui_dict[key][:max_trials]
  return gui_dict, diff_arrs

def _loadOrCreateDf(append_df):
  if append_df:
    df = pd.read_pickle(append_df)
    # https://stackoverflow.com/a/47545241/11996983
    cols = ["Name", "Date", "SessionNum"]
    skip_sessions = df.groupby(cols).size().reset_index()[cols].to_numpy()
    skip_sessions = frozenset(map(lambda el: tuple(el), skip_sessions))
  else:
    df = pd.DataFrame()
    skip_sessions = set()
  return df, skip_sessions

def loadFiles(files_patterns=["*.mat"], stop_at=10000, mini_df=False,
              append_df=None, few_trials_sessions=[]):
  if isinstance(files_patterns, (str, pathlib.Path)):
    files_patterns = [str(files_patterns)]
  else:
    try:
      if not all(isinstance(elem, str) for elem in files_patterns):
        raise Exception()
    except:
      raise Exception(f"File patterns argument must be an iterable of strings, "
                      f"not {type(files_patterns)}")
  old_df, skip_sessions = _loadOrCreateDf(append_df)
  updated_df = False
  skip_few_sess_ids = frozenset(map(
      lambda fp:uniqueSessID(decomposeFilePathInfo(fp)), few_trials_sessions))
  count=1
  bad_filenames=[]
  bad_files_structure=[]
  bad_files_few_trials=[]
  all_ses_dfs_li = []
  chained_globs=it.chain.from_iterable(
                            glob.iglob(pattern) for pattern in files_patterns)
  #print("File patterns:", files_patterns)
  #chained_globs=list(chained_globs); print("Globs:", chained_globs)
  for fp in chained_globs:
    sess_df = _startProcessFile(fp, mini_df, skip_sessions, skip_few_sess_ids)
    if not isinstance(sess_df, pd.DataFrame):
      if sess_df in [_TEMP_STORED_FILE, _SKIPPED_SESS]:
        continue
      if   sess_df == _BAD_FILE_NAME_FORMAT: bad_filenames.append(fp)
      elif sess_df == _BAD_FILE_FEW_TRIALS:  bad_files_few_trials.append(fp)
      elif sess_df == _BAD_FILE_STRUCTURE:   bad_files_structure.append(fp)
      continue
    all_ses_dfs_li.append(sess_df)
    updated_df = True
    count+=1
    if count == stop_at:
      break

  if len(bad_filenames):
    print("didn't processing the following files as they looked different:")
    [print("- ", fp) for fp in bad_filenames]
  if len(bad_files_structure):
    print("Found internal errors while processing the following files:")
    [print("- ", fp) for fp in bad_files_structure]
  if len(bad_files_few_trials):
    print("DIdn't process files with zero or very few trials:")
    [print("- ", fp) for fp in bad_files_few_trials]
  print()
  final_df = pd.concat([old_df] + all_ses_dfs_li, ignore_index=True, sort=False)
  final_df = reduceTypes(final_df)
  return final_df, few_trials_sessions + bad_files_few_trials, updated_df

def _startProcessFile(fp, mini_df, skip_sessions, skip_few_sess_ids):
  if "temp_" in fp:
    return _TEMP_STORED_FILE
  decomposed_name = decomposeFilePathInfo(fp)
  if not decomposed_name:
    print(f"Skipping badly formatted filename: {fp}")
    # bad_filenames.append(fp)
    return _BAD_FILE_NAME_FORMAT
  unique_sess_id = uniqueSessID(decomposed_name)
  if unique_sess_id in skip_sessions:
    print(f"Already existing in dataframe: {fp}")
    return _SKIPPED_SESS
  elif unique_sess_id in skip_few_sess_ids:
    print(f"Not loading already-known few trials sessions: {fp}")
    return _SKIPPED_SESS

  try:
    mat = loadmat(fp, struct_as_record=False, squeeze_me=True)
  except (TypeError, ValueError, Exception) as e:
    print(f"Failed to to load Matlab file {fp} due to: {e}")
    traceback.print_exc()
    # bad_files_structure.append(fp)
    return _BAD_FILE_STRUCTURE
  data = mat['SessionData']
  try:
    sess_df = _processFileData(data, mini_df, fp, decomposed_name)
  except Exception as e:
    print(f"Didn't process {fp} due to: {e}")
    traceback.print_exc()
    #bad_files_structure.append(fp)
    return _BAD_FILE_STRUCTURE
  return sess_df # This can be a df or _BAD_FILE_FEW_TRIALS

def _processFileData(data, mini_df, fp, decomposed_name):
  new_data_format=False
  if hasattr(data.Custom, 'Trials'):
    new_data_format=True
    max_trials = len(data.RawEvents.Trial)
    print(f"Max Trials: {max_trials}")
    # Assign everything in Custom.Trials to Custom directly to be compitable
    # with old file structure that had everything at Custom directly.
    for field_name in data.Custom.Trials[0]._fieldnames:
      field_val = np.array(deque(map(lambda t:getattr(t, field_name),
                                    data.Custom.Trials[:max_trials])))
      setattr(data.Custom, field_name, field_val)
  if isinstance(data.Custom.ChoiceLeft, (int, float, complex)) or \
     len(data.Custom.ChoiceLeft) <= MIN_SESSION_TRIALS_LEN:
    return _BAD_FILE_FEW_TRIALS
  print("Processing", fp)
  max_trials = np.uint16(len(data.Custom.ChoiceLeft))
  new_dict = {}
  filter_vals = ["PulsePalParamStimulus", "PulsePalParamFeedback",
                 "RewardMagnitude", "_fieldnames", "CatchCount", "TrialStart",
                 "GracePeriod", "CatchOmegaTrack"]
  for field_name in dir(data.Custom):
    if field_name in filter_vals or field_name.startswith("__"):
      continue
    field_val = getattr(data.Custom, field_name)
    if hasattr(field_val, "__len__"):
        field_val = field_val[:max_trials]
    if field_name in ["GratingOrientation", "LightIntensityLeft",
                      "LightIntensityRight", "DotsCoherence"] and \
      len(field_val) == 0:
      field_val = [np.nan] * max_trials
    new_dict[field_name] = field_val

  found_ReactionTime = "ReactionTime" in new_dict
  if not found_ReactionTime:
    reaction_times = []
  #print("Found ReactionTime:", found_ReactionTime)
  new_dict["TrialStartTimestamp"] = data.TrialStartTimestamp[:max_trials]
  gui_dict, diff_arrs = _extractGUI(data, max_trials,
                  is_mini_df=mini_df, new_data_format=new_data_format)
  new_dict.update(gui_dict)
  new_dict.update(diff_arrs)
  #new_dict["CatchError"] = catch_error[:max_trials]
  #new_dict["FeedbackTrialSettings"] = feedback_type[:max_trials]
  def extractStates(trial):
    states = States()
    added = False
    for state_name in dir(trial.States):
      if not state_name.startswith('_'):
        start_end = StartEnd(getattr(trial.States, state_name))
        setattr(states, state_name, start_end)
        added = True
        if not found_ReactionTime and state_name == 'WaitCenterPortOut':
          if not np.isnan(start_end.end):
            reaction_times.append(start_end.end - start_end.start)
          else:
            reaction_times.append(-1) # Match what we write in MATLAB
    if not added:
      print("States:", dir(trial.States))
    return states

  for perf_key, dest_key in [("AllPerformance", "SessionAllPerformance"),
                             ("Performance", "SessionPerformance")]:
    last_trial_settings = data.TrialSettings[max_trials-1]
    if not new_data_format:
      last_trial_settings = last_trial_settings.GUI
    if hasattr(last_trial_settings, perf_key):
      perf_str = getattr(last_trial_settings, perf_key)
      perf = float(perf_str.split('%')[0])
    else:
      perf = float('nan')
    new_dict[dest_key] = perf
  new_dict["MaxTrial"] = max_trials
  if not mini_df and hasattr(data, "RawEvents"):
    # Extract trial_states anyhow as they calculate ReactionTime
    trials_states = list(map(extractStates, data.RawEvents.Trial[:max_trials]))
    # TODO: Change this to an assert, it should always be
    # equal to max_trials
    if len(trials_states) == max_trials + 1: # Needed for old files
      trials_states = trials_states[:-1]
    new_dict["States"] = trials_states
  if not found_ReactionTime:
    new_dict["ReactionTime"] = [np.nan] * max_trials
  calcRT, calcMT = _calcReactionAndMovementTimes(
                                              data.RawEvents.Trial[:max_trials],
                                              data.TrialSettings[:max_trials],
                                              new_data_format, fp, max_trials)
  new_dict["calcReactionTime"] = calcRT
  new_dict["calcMovementTime"] = calcMT
  new_dict["File"] = fp
  # In couple of cases, I found some strange behavior where
  # data.Filename didn't match filepath. Probably due to human error
  # while handling OneDrive sync conflicts
  if hasattr(data, "Filename"):
    mouse_name, protocol, (year, month, day), session_num = \
                                            decomposeFilePathInfo(data.Filename)
  else:
    mouse_name, protocol, (year, month, day), session_num = decomposed_name
  # data.Custom.Subject can incorrectly computed (e.g name, vgat2.1 is
  # computed as just vgat2). We compute it from fileame instead.
  new_dict["Name"] = mouse_name
  new_dict["Date"] = dt.date(year, month, day)
  new_dict["SessionNum"] = np.uint8(session_num)
  if hasattr(data, "Protocol") and len(data.Protocol):
    protocol = data.Protocol
  # else use the older value of protocol we computed above
  print("Assigning protocol:", protocol)
  new_dict["Protocol"] = protocol
  try:
    new_dict["SessionStartTime_UTC"] = data.Info.SessionStartTime_UTC
  except:
    new_dict["SessionStartTime_UTC"] = "        " # e.g: 15:43:02
  if False:
    for key, val in new_dict.items():
      if hasattr(val,"__len__"):
        if len(val) != max_trials:
          print("Key:", key, " - val.shape: ", len(val),
              "- type:", type(val), "- expected?: ", max_trials)
  sess_df = pd.DataFrame(new_dict)
  sess_df = reduceTypes(sess_df)
  if mini_df:
    cols_to_keep = list(filter(lambda col:col not in MIN_DF_COLS_DROP,
                               sess_df.columns))
    dropped_cols = set(sess_df.columns) - set(cols_to_keep)
    print("Dropping", dropped_cols, "columns. Remaining cols:",
          len(cols_to_keep))#,":", df2.columns)
    #df2.drop(columns=cols_to_drop)
    sess_df = sess_df[cols_to_keep]
  return sess_df

def _calcReactionAndMovementTimes(raw_events_li, trials_settings,
                                  new_data_format, fp, max_trials):
  reaction_times = []
  movement_times = []
  _extractTrialsPortsEvents(raw_events_li, trials_settings, new_data_format)
  trials_ports = _getTrialsPorts(trials_settings, new_data_format)
  for idx, (this_trial_ports, trial_states_events) in \
                                    enumerate(zip(trials_ports, raw_events_li)):
    t_reaction_time, t_movement_time = _calcTrialReactionAndMovementTimes(
                     this_trial_ports, trial_states_events, fp, trial_num=idx+1)
    reaction_times.append(t_reaction_time)
    movement_times.append(t_movement_time)
  assert len(reaction_times) == max_trials
  assert len(movement_times) == max_trials
  return reaction_times, movement_times

def _calcTrialReactionAndMovementTimes(this_trial_ports, trial_states_events,
                                       fp, trial_num):
  # Okay, ideally states and events should exist in certain
  # sequences that we can even assert on. However, given enough
  # animals and trials, eventually some wires get loose and some
  # port{in/out} never get registered. So asserts are treated
  # as warnings instead with Matlab trial number and filename.
  trial_states = trial_states_events.States
  try:
    trial_events = trial_states_events.Events
  except Exception as e:
    if trial_num != 1: # Happens sometimes at trial 1, not sure why
      raise e
  # print("Matlab trial:", idx+1)
  WaitForChoice_start = trial_states.WaitForChoice[0]
  # Sometimes WaitForChoice_start will be an array of arrays if
  # GUI_HabituateIgnoreIncorrect is enabled.
  if not np.isscalar(WaitForChoice_start):
    WaitForChoice_start = WaitForChoice_start[0]
  if np.isnan(WaitForChoice_start):
    if not np.isnan(trial_states.early_withdrawal[0]) and \
        not np.isnan(trial_states.broke_fixation[0]):
      print(f"Unexpected states (1) found in Matlab trial: {trial_num} - "
            f"file: {fp}", file=sys.stderr)
    return np.nan, np.nan

  l_port, c_port, r_port = this_trial_ports
  # Use -1 val as missing portout, should indicate a timeout_misside_choice.
  center_outs = getattr(trial_events, f"Port{c_port}Out", -1)
  if isinstance(center_outs, (int, float, complex)):
    center_outs = np.array([center_outs])
  # Some states didn't exist in old protocols
  try:
    reaction_start = trial_states.StimulusTime[-1]
  except AttributeError:
    use_center_reward = True
  else:
    use_center_reward = np.isnan(reaction_start)
  if use_center_reward:
    # I assume that the end of CenterPortRewardDelivery will
    # always be reliable. The side effect is that it will give
    # very very small decision time value in for reaction-time
    # experiments.
    reaction_start = trial_states.CenterPortRewardDelivery[-1]
  if np.isnan(reaction_start):
    return np.nan, np.nan
  # Calculate reaction-time
  post_stim_out = center_outs[center_outs >= reaction_start]
  if len(post_stim_out) == 0:
    if np.isnan(trial_states.timeOut_missed_choice[0]):
      print(f"Unexpected states (2) found in Matlab trial: {trial_num} "
            f"- file: {fp}", file=sys.stderr)
    # Declare reaction_end to be sure that the code won't blow up
    reaction_end = np.nan
    reaction_time = np.nan
  else:
    reaction_end = post_stim_out[0]
    reaction_time = reaction_end - reaction_start
    if reaction_end - reaction_start < 0.0015:
      reaction_time = np.nan
  # Calculate movement time
  # It should never happen that timeOut_missed_choice would
  # not be null and reaction time reaction end is nan
  if np.isnan(trial_states.timeOut_missed_choice[0]):
    if not np.isnan(reaction_end):
      movement_start = reaction_end
      lr_ins = np.array([])
      for port in [l_port, r_port]:
        ins = getattr(trial_events, f"Port{port}In", [])
        if type(ins) == float:
          ins = [ins]
        lr_ins = np.append(lr_ins, ins)
      lr_ins = np.array(lr_ins)
      first_post_stim_in = lr_ins[lr_ins > movement_start]
      if len(first_post_stim_in) < 1:
        print(f"Unexpected states (3) found in Matlab trial: {trial_num}"
              f"- file: {fp}", file=sys.stderr)
        movement_time = np.nan
      else:
        first_post_stim_in = first_post_stim_in[0]
        movement_time = first_post_stim_in - movement_start
    else:
      print(f"Unexpected states (4) found in Matlab trial: {trial_num} "
            f"- file: {fp}", file=sys.stderr)
      movement_time = np.nan
  else:
    movement_time = np.nan
  return reaction_time, movement_time

def reduceTypes(df, debug=False):
    for col_name in df.select_dtypes(include=['object']):
        if col_name in ["States", "Date", "GUI_OmegaTable"]: continue
        df[col_name] = df[col_name].astype(str)
    for col_name in df.columns:
        # print("Col:", col_name, "- type:", type(df[col_name].iloc[0]))
        if str(df[col_name].dtype) == 'object':
            try:
                temp = df[col_name].copy()
                temp[temp == 'nan'] = np.nan
                df[col_name] = pd.to_numeric(temp, downcast='float',
                                             errors='raise')
            except Exception as e:
                # print("Failed with:" + str(e))
                pass
            else:
                if debug:
                    print("Converted str '"+str(col_name)+"' to float")
    # Ignore converting floats, we get bigger files but at least we don't
    # introduce potetial rounding errors
    # for col_name in df.select_dtypes(include=['float64']):
    #     # Leave DV and StimulusOmega as they are sensitive to rounding
    #     if col_name in ["StimulusOmega", "DV", "LeftClickTrian",
    #                     "RightClickTrian"]:
    #         continue
    #     df[col_name] = df[col_name].astype('float32')

    # We would like to have boolean values with null entries, this is easier
    # said than done. We can either leave them as float32 (but we should makes
    # sure it is not string of floats) or convert them to a pandas Nullable
    # Integer type. The problem with the latter is that they seem not to play
    # nicely with matploblib or rather less known libraries like statsmodels.
    # For now, I'll leave them as float32.
    # for col_name in df.columns:
    #     unique_vals = df[col_name].unique()
    #     for val in unique_vals:
    #         # Simple try/except float casting won't work in cases where it's
    #         # empty string or empty brackets. Do this semi=manual check instead.
    #         if (type(val) == str and (val.upper() == "NAN" or
    #                                   val.replace('.','').isdigit())) \
    #            or isinstance(val,(np.floating, float)):
    #             #str_val = str(val).upper()
    #             #if str_val != "NAN" and not str_val.replace(".","").isdigit():
    #             #    continue
    #             float_val = float(val)
    #             if float_val in [0, 1] or np.isnan(float_val):
    #                 continue
    #         # If we reached here then we've fallen out of the nested if-s
    #         if debug:
    #             print("Not converting '"+str(col_name)+"' because of", val,
    #                 "of type", type(val), "- Unique values:",
    #                 "{}".format(unique_vals if len(unique_vals) < 10 else "{Many}"))
    #         break # It's not a boolean type
    #     else:
    #         # Don't use 'bool' or normal int values because they don't maintain
    #         # NaN values. Use instead one of pandas "Nullable Integer" classes,
    #         # If you are usig pandas > v1.0.x the new 'boolean' pandas type.
    #         if debug:
    #             print("Converting '"+str(col_name)+ "' with unique values:",
    #                   unique_vals)
    #         # Do it on two steps, else it sometimes complain it can't jump from
    #         # String to Int8
    #         df[col_name] = df[col_name].astype(np.float32)
    #         df[col_name] = df[col_name].astype('Int8')
    for col_name in df.select_dtypes(include=['int64']):
        if 0 <= df[col_name].min() and df[col_name].max() <= 255:
            df[col_name] = df[col_name].astype(np.uint8)
        else:
            df[col_name] = df[col_name].astype(np.int16)
    return df
