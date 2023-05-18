import numpy as np
class CurTaskParameters:
  class Figures:
    class OutcomePlot:
      Position = np.array([ 200,  200, 1000,  400])

    class ParameterGUI:
      Position = np.array([  50,   50, 1360,  700])


  class GUI:
    AllPerformance = '100.00%/3T'
    BeepAfterMinSampling = 0
    BetaDistAlphaNBeta = 0.3
    CalcLeftBias = 0.5
    CatchError = 0
    CenterPokeAttenPrcnt = 95
    CenterPortRewAmount = 0.5
    ChoiceDeadLine = 20
    ComputerName = 'DESKTOP-V7K1079'
    CorrectBias = 0
    CurrentStim = '100% R'
    CutAirReward = 0
    CutAirSampling = 1
    CutAirStimDelay = 1
    ExperimentType = 2
    FeedbackDelay = 0
    FeedbackDelayDecr = 0.01
    FeedbackDelayGrace = 0.4
    FeedbackDelayIncr = 0.01
    FeedbackDelayMax = 0
    FeedbackDelayMin = 0
    FeedbackDelaySelection = 1
    FeedbackDelayTau = 0.1
    GUIVer = 29
    HabituateIgnoreIncorrect = 0
    ITI = 0
    ITISignalType = 1
    IncorrectChoiceSignalType = 4
    IsCatch = 'false'
    IsOptoTrial = 'false'
    LeftBias = 0.5
    LeftBiasVal = 0.5
    LeftPokeAttenPrcnt = 73
    MinSample = 0.5
    MinSampleDecr = 0.02
    MinSampleIncr = 0.05
    MinSampleMax = 1
    MinSampleMin = 0.5
    MinSampleNumInterval = 2
    MinSampleRandProb = 1
    MinSampleType = 4
    MouseState = 2
    MouseWeight = np.nan
    class OmegaTable:
      Omega = np.array([100,  95,  90,  85,  80,  75,  70,  65,  60,  55])
      OmegaProb = np.array([9, 0, 0, 0, 1, 0, 0, 0, 1, 0])
      RDK = np.array([100,  90,  80,  70,  60,  50,  40,  30,  20,  10])

    OptoBrainRegion = 1
    OptoEndState1 = 13
    OptoEndState2 = 14
    OptoMaxTime = 10
    OptoOr2P = 1
    OptoProb = 0
    OptoStartDelay = 0
    OptoStartState1 = 8
    PCTimeout = 1
    Percent50Fifty = 0
    PercentCatch = 0.2
    PercentForcedLEDTrial = 0
    Performance = '100.00%/3T'
    PlayNoiseforError = 0
    PortLEDtoCueReward = 0
    Ports_LMRAir = 1238
    PreStimuDelayCntrReward = 0
    RewardAfterMinSampling = 0
    RewardAmount = 5
    RightPokeAttenPrcnt = 73
    ShowFeedback = 1
    ShowFix = 1
    ShowPsycStim = 1
    ShowST = 1
    ShowTrialRate = 1
    ShowVevaiometric = 1
    StartEasyTrials = 4
    StimAfterPokeOut = 1
    StimDelay = 0.12020747578128728
    StimDelayAutoincrement = 0
    StimDelayDecr = 0.01
    StimDelayGrace = 0.1
    StimDelayIncr = 0.01
    StimDelayMax = 0.2
    StimDelayMin = 0
    StimulusSelectionCriteria = 2
    StimulusTime = 0.3
    SumRates = 100
    TableNote = np.nan
    TimeOutBrokeFixation = 0
    TimeOutEarlyWithdrawal = 0.7
    TimeOutIncorrectChoice = 0
    TimeOutMissedChoice = 0
    TimeOutSkippedFeedback = 0
    VevaiometricMinWT = 0.5
    VevaiometricNBin = 8
    VevaiometricShowPoints = 1
    VevaiometricYLim = 20
    VisualStimAnglePortLeft = 7
    VisualStimAnglePortRight = 3
    Wire1VideoTrigger = 0
    apertureSizeHeight = 36
    apertureSizeWidth = 36
    centerX = 0
    centerY = 0
    circleArea = 1017.876
    cyclesPerSecondDrift = 5
    dotLifetimeSecs = 1
    dotSizeInDegs = 2
    dotSpeedDegsPerSec = 25
    drawRatio = 0.2
    gaborSizeFactor = 1
    gaussianFilterRatio = 0.1
    nDots = 51
    numCycles = 5
    phase = 0.5
    screenDistCm = 30
    screenWidthCm = 20

  class GUIMeta:
    class AllPerformance:
      Style = 'text'

    class BeepAfterMinSampling:
      Style = 'checkbox'

    class CalcLeftBias:
      Style = 'text'

    class CatchError:
      Style = 'checkbox'

    class CorrectBias:
      Style = 'checkbox'

    class CurrentStim:
      Style = 'text'

    class CutAirReward:
      Style = 'checkbox'

    class CutAirSampling:
      Style = 'checkbox'

    class CutAirStimDelay:
      Style = 'checkbox'

    class ExperimentType:
      String = np.array(['Auditory', 'LightIntensity', 'GratingOrientation', 'RandomDots'])
      Style = 'popupmenu'

    class FeedbackDelay:
      Style = 'text'

    class FeedbackDelaySelection:
      String = np.array(['Fix', 'AutoIncr', 'TruncExp', 'None'])
      Style = 'popupmenu'

    class HabituateIgnoreIncorrect:
      Style = 'checkbox'

    class ITISignalType:
      String = np.array(['None', 'Beep', 'PortLED'])
      Style = 'popupmenu'

    class IncorrectChoiceSignalType:
      String = np.array(['None', 'NoisePulsePal', 'PortLED', 'BeepOnWire_1'])
      Style = 'popupmenu'

    class IsCatch:
      Style = 'text'

    class IsOptoTrial:
      Style = 'text'

    class LeftBias:
      Callback = None
      Style = 'slider'

    class LeftBiasVal:
      Callback = None

    class MinSample:
      Style = 'text'

    class MinSampleType:
      String = np.array(['FixMin', 'AutoIncr', 'RandBetMinMax_DefIsMax', 'RandNumIntervalsMinMax_DefIsMax'])
      Style = 'popupmenu'

    class MouseState:
      String = np.array(['FreelyMoving', 'HeadFixed'])
      Style = 'popupmenu'

    class OmegaTable:
      ColumnEditable = np.array([1, 0, 1])
      ColumnLabel = np.array(['Stim %', 'RDK Coh', 'P(a)'])
      class RDK:
        Style = 'text'

      String = 'Omega probabilities'
      Style = 'table'

    class OptoBrainRegion:
      String = np.array(['V1_L', 'V1_R', 'V1_Bi', 'M2_L', 'M2_R', 'M2_Bi'])
      Style = 'popupmenu'

    class OptoEndState1:
      String = np.array(['ITI_Signal', 'WaitForCenterPoke', 'PreStimReward', 'TriggerWaitForStimulus', 'WaitForStimulus', 'StimDelayGrace', 'broke_fixation',
 'stimulus_delivery', 'early_withdrawal', 'BeepMinSampling', 'CenterPortRewardDelivery', 'TriggerWaitChoiceTimer', 'WaitCenterPortOut',
 'WaitForChoice', 'WaitForRewardStart', 'WaitForReward', 'RewardGrace', 'Reward', 'WaitRewardOut', 'RegisterWrongWaitCorrect', 'WaitForPunishStart',
 'WaitForPunish', 'PunishGrace', 'Punishment', 'timeOut_EarlyWithdrawal', 'timeOut_EarlyWithdrawalFlashOn', 'timeOut_IncorrectChoice',
 'timeOut_SkippedFeedback', 'timeOut_missed_choice', 'ITI', 'ext_ITI'])
      Style = 'popupmenu'

    class OptoEndState2:
      String = np.array(['ITI_Signal', 'WaitForCenterPoke', 'PreStimReward', 'TriggerWaitForStimulus', 'WaitForStimulus', 'StimDelayGrace', 'broke_fixation',
 'stimulus_delivery', 'early_withdrawal', 'BeepMinSampling', 'CenterPortRewardDelivery', 'TriggerWaitChoiceTimer', 'WaitCenterPortOut',
 'WaitForChoice', 'WaitForRewardStart', 'WaitForReward', 'RewardGrace', 'Reward', 'WaitRewardOut', 'RegisterWrongWaitCorrect', 'WaitForPunishStart',
 'WaitForPunish', 'PunishGrace', 'Punishment', 'timeOut_EarlyWithdrawal', 'timeOut_EarlyWithdrawalFlashOn', 'timeOut_IncorrectChoice',
 'timeOut_SkippedFeedback', 'timeOut_missed_choice', 'ITI', 'ext_ITI'])
      Style = 'popupmenu'

    class OptoOr2P:
      String = np.array(['Optogenetics', 'TwoPhoton_Shutter'])
      Style = 'popupmenu'

    class OptoStartState1:
      String = np.array(['ITI_Signal', 'WaitForCenterPoke', 'PreStimReward', 'TriggerWaitForStimulus', 'WaitForStimulus', 'StimDelayGrace', 'broke_fixation',
 'stimulus_delivery', 'early_withdrawal', 'BeepMinSampling', 'CenterPortRewardDelivery', 'TriggerWaitChoiceTimer', 'WaitCenterPortOut',
 'WaitForChoice', 'WaitForRewardStart', 'WaitForReward', 'RewardGrace', 'Reward', 'WaitRewardOut', 'RegisterWrongWaitCorrect', 'WaitForPunishStart',
 'WaitForPunish', 'PunishGrace', 'Punishment', 'timeOut_EarlyWithdrawal', 'timeOut_EarlyWithdrawalFlashOn', 'timeOut_IncorrectChoice',
 'timeOut_SkippedFeedback', 'timeOut_missed_choice', 'ITI', 'ext_ITI'])
      Style = 'popupmenu'

    class PCTimeout:
      Style = 'checkbox'

    class Performance:
      Style = 'text'

    class PlayNoiseforError:
      Style = 'checkbox'

    class PortLEDtoCueReward:
      Style = 'checkbox'

    class RewardAfterMinSampling:
      Style = 'checkbox'

    class ShowFeedback:
      Style = 'checkbox'

    class ShowFix:
      Style = 'checkbox'

    class ShowPsycStim:
      Style = 'checkbox'

    class ShowST:
      Style = 'checkbox'

    class ShowTrialRate:
      Style = 'checkbox'

    class ShowVevaiometric:
      Style = 'checkbox'

    class StimAfterPokeOut:
      Style = 'checkbox'

    class StimDelay:
      Style = 'text'

    class StimDelayAutoincrement:
      String = 'Auto'
      Style = 'checkbox'

    class StimulusSelectionCriteria:
      String = np.array(['BetaDistribution', 'DiscretePairs'])
      Style = 'popupmenu'

    class TableNote:
      Style = 'text'

    class VevaiometricShowPoints:
      Style = 'checkbox'

    class VisualStimAnglePortLeft:
      String = np.array(['Degrees0', 'Degrees45', 'Degrees90', 'Degrees135', 'Degrees180', 'Degrees225', 'Degrees270', 'Degrees315'])
      Style = 'popupmenu'

    class VisualStimAnglePortRight:
      String = np.array(['Degrees0', 'Degrees45', 'Degrees90', 'Degrees135', 'Degrees180', 'Degrees225', 'Degrees270', 'Degrees315'])
      Style = 'popupmenu'

    class Wire1VideoTrigger:
      Style = 'checkbox'

    class circleArea:
      Style = 'text'

    class nDots:
      Style = 'text'


  class GUIPanels:
    AirControl = np.array(['CutAirStimDelay', 'CutAirReward', 'CutAirSampling'])
    Auditory = 'SumRates'
    CurrentTrial = np.array(['MouseState', 'MouseWeight', 'StimDelay', 'MinSample', 'CurrentStim', 'CalcLeftBias', 'FeedbackDelay', 'IsCatch', 'IsOptoTrial', 'Performance',
 'AllPerformance'])
    FeedbackDelay = np.array(['FeedbackDelaySelection', 'FeedbackDelayMin', 'FeedbackDelayMax', 'FeedbackDelayIncr', 'FeedbackDelayDecr', 'FeedbackDelayTau', 'FeedbackDelayGrace',
 'IncorrectChoiceSignalType', 'ITISignalType'])
    General = np.array(['ExperimentType', 'ITI', 'RewardAmount', 'ChoiceDeadLine', 'TimeOutIncorrectChoice', 'TimeOutBrokeFixation', 'TimeOutEarlyWithdrawal',
 'TimeOutMissedChoice', 'TimeOutSkippedFeedback', 'HabituateIgnoreIncorrect', 'PlayNoiseforError', 'PCTimeout', 'StartEasyTrials', 'Percent50Fifty',
 'PercentCatch', 'CatchError', 'Ports_LMRAir', 'Wire1VideoTrigger'])
    Grating = np.array(['gaborSizeFactor', 'phase', 'numCycles', 'cyclesPerSecondDrift', 'gaussianFilterRatio'])
    LightIntensity = np.array(['LeftPokeAttenPrcnt', 'CenterPokeAttenPrcnt', 'RightPokeAttenPrcnt', 'StimAfterPokeOut', 'BeepAfterMinSampling'])
    Optogenetics = np.array(['OptoProb', 'OptoOr2P', 'OptoStartState1', 'OptoStartDelay', 'OptoMaxTime', 'OptoEndState1', 'OptoEndState2', 'OptoBrainRegion', 'IsOptoTrial'])
    RandomDots = np.array(['drawRatio', 'circleArea', 'nDots', 'dotSizeInDegs', 'dotSpeedDegsPerSec', 'dotLifetimeSecs'])
    Sampling = np.array(['RewardAfterMinSampling', 'CenterPortRewAmount', 'MinSampleMin', 'MinSampleMax', 'MinSampleType', 'MinSampleIncr', 'MinSampleDecr',
 'MinSampleNumInterval', 'MinSampleRandProb', 'StimulusTime', 'PortLEDtoCueReward', 'PercentForcedLEDTrial'])
    ShowPlots = np.array(['ShowPsycStim', 'ShowVevaiometric', 'ShowTrialRate', 'ShowFix', 'ShowST', 'ShowFeedback'])
    StimDelay = np.array(['StimDelayAutoincrement', 'StimDelayMin', 'StimDelayMax', 'StimDelayIncr', 'StimDelayDecr', 'StimDelayGrace', 'PreStimuDelayCntrReward'])
    StimulusSelection = np.array(['OmegaTable', 'TableNote', 'BetaDistAlphaNBeta', 'StimulusSelectionCriteria', 'LeftBias', 'LeftBiasVal', 'CorrectBias'])
    Vevaiometric = np.array(['VevaiometricYLim', 'VevaiometricMinWT', 'VevaiometricNBin', 'VevaiometricShowPoints'])
    VisualGeneral = np.array(['VisualStimAnglePortRight', 'VisualStimAnglePortLeft', 'screenDistCm', 'screenWidthCm', 'apertureSizeWidth', 'apertureSizeHeight', 'centerX',
 'centerY'])

  class GUITabs:
    General = np.array(['CurrentTrial', 'AirControl', 'General', 'FeedbackDelay', 'StimDelay'])
    Opto = 'Optogenetics'
    Plots = np.array(['ShowPlots', 'Vevaiometric'])
    Sampling = np.array(['CurrentTrial', 'LightIntensity', 'Auditory', 'Sampling', 'StimulusSelection'])
    Visual = np.array(['CurrentTrial', 'Grating', 'RandomDots', 'VisualGeneral'])


