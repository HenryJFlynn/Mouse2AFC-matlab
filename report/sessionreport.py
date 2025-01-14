# Call from MATLAB:
# !python -c "import sys; sys.path.append(r'C:\Users\hatem\OneDrive\Documents\BpodUser\Protocols\Mouse2AFC\report'); import sessionreport; sessionreport.showAndSaveReport(r'dummy')"
#
# You need to have the following libraries:
# pip install numpy scipy matplotlib pandas scikit-learn statsmodels colour click
# For development run:
# conda -n analysis -c conda-forge python=3.7 numpy scipy matplotlib pandas scikit-learn statsmodels colour click tqdm ipykernel ipython

from calendar import weekday
from enum import auto
import os
import pathlib
import sys
import shutil
import time
import traceback
import matplotlib.pyplot as plt
from numpy.core.shape_base import block
try:
  from . import analysis
  from . import mat_reader_core
except:
  pass


class PlotHandler():
  def __init__(self):
    self._should_close = None # It will be set later
    self._plot_showing = None
    self._cur_running_fig = None
    analysis.setMatplotlibParams(silent=True)

  def _closeWindow(self):
    assert self._should_close is not None
    # If the user click on the figure then this method is called twice, once for
    # th timer but the if statement below is not executed, and a second time
    # when the user actually click the close button. This second time also the
    # the if statement doesn't execute but the window is closed anyway.
    if self._should_close:
      self._should_close = None
      plt.close(self._cur_running_fig)

  def _disableAutoClose(self, event):
    assert self._should_close is not None
    self._should_close = False

  def _closeHandler(self, event):
    assert self._plot_showing == True
    self._plot_showing = False

  def pltInBgnd(self, *, fig, auto_close_after_ms):
    if auto_close_after_ms:
      self.waitForCurFig()
    self._cur_running_fig = fig
    self._should_close = True
    if auto_close_after_ms:
      self._plot_showing = True
      block=False
      fig.canvas.mpl_connect('button_press_event', self._disableAutoClose)
      #fig.canvas.mpl_connect('resize_event', self._disableAutoClose)
      fig.canvas.mpl_connect('close_event', self._closeHandler)
      # We don't use the _timer instance but we need to keep a reference to it,
      # otherwise the timer won't run
      self._timer = fig.canvas.new_timer(interval = auto_close_after_ms)
      self._timer.add_callback(self._closeWindow)
      self._timer.start()
    else:
      self._plot_showing = False
      block=True
    plt.show(block=block)

  def waitForCurFig(self):
    start = time.time()
    while self._plot_showing:
      time.sleep(0.00001)
      self._cur_running_fig.canvas.flush_events()


class MakeAndSavePlots():
  def run(self, session_df, save_dir_or_none, show_fig,
          auto_close_after_ms=None):
    try:
      sess_date = session_df.Date
    except AttributeError:
      sess_date = session_df.SessionDate
    date_str = sess_date.unique()[0].strftime("%Y_%m_%d_%a")
    session_num = session_df.SessionNum.unique()[0]
    animal_name = session_df.Name.unique()[0]
    protocol_name = session_df.Protocol.unique()[0]
    if save_dir_or_none:
      pathlib.Path(save_dir_or_none).mkdir(parents=True, exist_ok=True)
    if auto_close_after_ms is None:
      auto_close_after_ms = 60000

    copy_to_daily_sessions = False
    onedrive_root_dir = os.getenv("OneDrive")
    if onedrive_root_dir:
      # "OneDrive/Figures/{ProtocolName}/" must exists
      daily_figures = "{}{}{}{}{}".format(onedrive_root_dir, os.path.sep,
                                         "Figures", os.path.sep, protocol_name)
      if os.path.exists(daily_figures):
        onedrive_todays_dir = "{}{}{}".format(daily_figures, os.path.sep,
                                              date_str)
        print("Todays dir:", onedrive_todays_dir)
        pathlib.Path(onedrive_todays_dir).mkdir(parents=False, exist_ok=True)
        copy_to_daily_sessions = True


    plot_handler = PlotHandler()
    try:
      fig = self._mainPlot(session_df)
      if show_fig:
        plot_handler.pltInBgnd(fig=fig, auto_close_after_ms=auto_close_after_ms)
    except Exception as err:
      print("An exception occurred in main fig:\n", traceback.format_exc(),
            file=sys.stderr)
    else:
      if save_dir_or_none:
        filename = "{}_Sess{}_{}_{}.png".format(date_str, session_num, "perf",
                                                animal_name)
        dst_path = "{}{}{}".format(save_dir_or_none, os.path.sep,filename)
        fig.savefig(dst_path)
        if copy_to_daily_sessions:
          daily_path = "{}{}{}.png".format(onedrive_todays_dir, os.path.sep,
                              "{}_Sess{}_perf".format(animal_name, session_num))
          shutil.copyfile(src=dst_path, dst=daily_path)

    if session_df.FeedbackTime.max() > 1 and \
     len(session_df[session_df.GUI_FeedbackDelaySelection == 3]) > 10:
      try:
        fig = self._confidencePlot(session_df)
        if show_fig:
          plot_handler.pltInBgnd(fig=fig, auto_close_after_ms=6000)
      except:
        print("An exception occurred in confidence fig:\n",
              traceback.format_exc(), file=sys.stderr)
      else:
        if save_dir_or_none:
          filename = "{}_Sess{}_{}_{}.png".format(date_str, session_num, "veva",
                                                  animal_name)
          fig.savefig("{}{}{}".format(save_dir_or_none, os.path.sep,filename))
          if copy_to_daily_sessions:
            daily_path = "{}{}{}.png".format(onedrive_todays_dir, os.path.sep,
                              "{}_Sess{}_veva".format(animal_name, session_num))
            shutil.copyfile(src=dst_path, dst=daily_path)

    plot_handler.waitForCurFig()
    if plt.get_fignums():
      plt.close()

  def _mainPlot(self, session_df):
    fig, axs = self._createSubplots(rows=2, cols=2,
                                    bottom=0.15, top=0.95,
                                    left=0.06, right=0.95,
                                    hspace=0.6, wspace=0.16,
                                    width_ratios=[1,2])

    animal_name = session_df.Name.unique()[0]
    psych_axes = analysis.psychAxes(animal_name, axes=axs[0][0])
    if "GUI_OptoBrainRegion" in session_df.columns:
      from .opto.optopsych import optoPsychPlot
      from .opto.optoutil import ChainedGrpBy
      for info, sub_df in ChainedGrpBy(session_df).byBrainRegion().byOptoConfig():
        brain_region, opto_config = info[-2], info[-1]
        optoPsychPlot(animal_name, sub_df, PsycStim_axes=psych_axes,
                      brain_region=brain_region, opto_config=opto_config,
                      by_animal=True, by_session=True, combine_sides=False,
                      save_figs=False, save_prefix=False,
                      incld_grp_info_lgnd=False)
    analysis.psychAnimalSessions(session_df, animal_name, psych_axes,
                                 analysis.METHOD)

    Plot = analysis.PerfPlots
    analysis.performanceOverTime(session_df, single_session=True, axes=axs[0][1],
                                 draw_plots=[Plot.Performance,
                                             Plot.DifficultiesCount,
                                             Plot.Bias,
                                             Plot.EarlyWD,
                                             Plot.MovementT,
                                             Plot.ReactionT,
                                             Plot.StimAPO])
    analysis.performanceOverTime(session_df, single_session=True, axes=axs[1][1],
                                 draw_plots=[Plot.Performance,
                                             Plot.Difficulties,
                                             Plot.SamplingT,
                                             Plot.CatchWT,
                                             Plot.MaxFeedbackDelay])

    analysis.trialRate(session_df, ax=axs[1][0], max_sess_time_lim_bug=3600*10,
                       IQR_filter=False, num_days_per_clr=None)
    return fig

  def _confidencePlot(self, session_df):
    fig, axs = self._createSubplots(rows=2, cols=2,
                                    bottom=0.07, top=0.92,
                                    left=0.06, right=0.98,
                                    hspace=0.31, wspace=0.19)

    analysis.accuracyWT(session_df, analysis.noFilter, axs[0][0],
                          how=analysis.AccWTMethod.Group0point15)
    analysis.trialsDistrib(session_df, analysis.noFilter, axs[0][1])

    max_feedbacktime=15
    analysis.vevaiometric(session_df, analysis.noFilter, axs[1][0],
                          max_feedbacktime)
    analysis.catchWTDistrib(session_df, analysis.noFilter, axs[1][1],
                            cumsum=True)
    return fig

  def _createSubplots(self, *,rows, cols, bottom, top, left, right, hspace,
                      wspace, width_ratios=None):
    if width_ratios:
      fig, axs = plt.subplots(rows, cols,
                              gridspec_kw={'width_ratios': width_ratios})
    else:
      fig, axs = plt.subplots(rows, cols)

    fig.set_size_inches(cols*analysis.SAVE_FIG_SIZE[0],
                        rows*analysis.SAVE_FIG_SIZE[1])
    fig.subplots_adjust(bottom=bottom, top=top, left=left, right=right,
                        hspace=hspace, wspace=wspace)
    return fig, axs

def _showSaveParsed(data_file, save_dir_or_None, show_fig,
                    auto_close_after_sec=None):
  session_df, _bad_ssns, _df_updated = mat_reader_core.loadFiles(data_file)
  print("Session df length:", len(session_df))
  if auto_close_after_sec is not None:
    auto_close_after_sec *= 1000 # Convert to ms
  MakeAndSavePlots().run(session_df, save_dir_or_None, show_fig=show_fig,
                         auto_close_after_ms=auto_close_after_sec)
  return session_df

def showAndSaveReport():
  data_flie = sys.argv[1]
  save_dir = sys.argv[2]
  print("Data file:", data_flie)
  print("Save dir:", save_dir)
  temp_path = r"C:\Users\hatem\OneDrive\Documents\py_matlab\\"+ \
              r"wfThy2_Mouse2AFC_Dec05_2019_Session1.mat"
              #r"vgat4_Mouse2AFC_Dec09_2019_Session2.mat"
              #r"RDK_WT1_Mouse2AFC_Dec04_2019_Session1.mat"
  _showSaveParsed(data_flie, save_dir, show_fig=True)


import datetime as dt
import multiprocessing as mp
import os
from pathlib import Path
import matplotlib.pyplot as plt

def makeReport(session_name, save_fig=False, show_fig=True):
  animal=session_name.split("_")[0]
  matlab_file = r"C:\BpodUser\Data\__ANIMAL__\Mouse2AFC\Session Data\__SESSION__"
  matlab_file = matlab_file.replace("__ANIMAL__", animal).replace("__SESSION__", session_name)
  if save_fig:
    save_dir_or_None = r"C:\BpodUser\Data\__ANIMAL__\Mouse2AFC\Python Figures\\".replace("__ANIMAL__", animal)
  else:
    save_dir_or_None = None
  df = _showSaveParsed(matlab_file, save_dir_or_None=save_dir_or_None,
                       show_fig=show_fig, auto_close_after_sec=0)
  # display(df.Difficulty1)
  # plt.show()
  return df

def _wrapMakeReport(session_name):
  from io import StringIO
  import sys
  sys.stdout = mystdout = StringIO()
  sys.stderr = mystdout
  try:
    makeReport(session_name, save_fig=True, show_fig=False)
  except:
    print("Caught fatal err:", traceback.format_exc(), file=sys.stderr)
  return mystdout.getvalue()

def regenerateAllSessionReport(only_new_files=True):
  base_dir = Path(r"C:\BpodUser\data\\")
  animal_names_dirs = [_dir for _dir in base_dir.iterdir()
      if _dir.is_dir() and "Dummy" not in _dir.name and "Fake" not in _dir.name]

  final_dirs = []
  for _dir in animal_names_dirs:
    ct = os.stat(str(_dir)).st_ctime
    ct = dt.datetime.fromtimestamp(ct)
    if True:#§ct < dt.datetime(2019, 10, 1):# and ct <= dt.datetime(2020, 5, 1):
      #print("Iterating:", _dir, "Created on:", ct)
      final_dirs.append(str(_dir))
  print("Final dirs:", final_dirs)
  n_workers = max(1, mp.cpu_count()-3)
  print(f"Using {n_workers} workers")
  from datetime import date
  import calendar
  months_3letters = list(calendar.month_abbr)
  with mp.Pool(n_workers) as pool:
    results = []
    def _iterDir(animal_dir):
      nonlocal results
      data_path = Path(f"{animal_dir}/Mouse2AFC/Session Data")
      figs_path_base   = Path(f"{animal_dir}/Mouse2AFC/Python Figures/")
      # if True: # Enable for testing
      #   def makeReport(_f, show_fig, save_fig):
      #     print("Dry run for:", _f)
      if not data_path.exists():
        return
      for _file in data_path.iterdir():
        if _file.is_file() and _file.name.endswith(".mat"):
          if only_new_files:
            #WTS4_Mouse2AFC_Dec04_2019_Session1.mat
            try:
              animal_name, _, month_day, year, sess = _file.stem.rsplit('_', 4)
              sess_num = int(sess[7:])
            except:
              continue
            year = int(year)
            month, day = month_day[:3], int(month_day[3:])
            month = months_3letters.index(month)
            _date = date(year, month, day)
            weekday = calendar.day_abbr[_date.weekday()]
            py_fig_name = f"{year}_{month:02d}_{day:02d}_{weekday}_"\
                          f"Sess{sess_num}_perf_{animal_name}.png"
            #python_fig_name = "2020_01_14_Tue_Sess2_perf_WTS3.png"
            if Path(f"{figs_path_base}/{py_fig_name}").exists():
              continue
          results.append(pool.apply_async(_wrapMakeReport, [_file.name]))
      print(f"Fired {animal_dir} workers")
    [_iterDir(_dir) for _dir in final_dirs]
    print("Fired all workers")
    for r in results:
        print(r.get())
    print("Closing")
    pool.close()
    print("Joining")
    pool.join()
  print("All done")

if __name__ == "__main__":
  print("__file__", __file__)
  import importlib, sys, pathlib # https://stackoverflow.com/a/50395128/11996983
  PKG = os.path.dirname(os.path.realpath(__file__))
  PKG = pathlib.Path(PKG)
  __package__ = f"{PKG.name}"
  MODULE_PATH = f"{PKG}{pathlib.os.path.sep}__init__.py"
  MODULE_NAME = f"{PKG.name}"
  # print(MODULE_NAME, MODULE_PATH)
  spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
  module = importlib.util.module_from_spec(spec)
  sys.modules[spec.name] = module 
  spec.loader.exec_module(module)
  
  from . import analysis
  from . import mat_reader_core
  showAndSaveReport()
