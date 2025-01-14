function TaskParameters = CreateTaskParameters(GUICurVer)
TaskParameters = struct;
%% Experiment
TaskParameters.GUI.ExperimentType = ExperimentType.LightIntensity;
TaskParameters.GUIMeta.ExperimentType.Style = 'popupmenu';
TaskParameters.GUIMeta.ExperimentType.String = ExperimentType.String;
TaskParameters.GUI.SecExperimentType = ExperimentType.SoundIntensity;
TaskParameters.GUIMeta.SecExperimentType.Style = 'popupmenu';
TaskParameters.GUIMeta.SecExperimentType.String = ExperimentType.String;
TaskParameters.GUI.SecExpUseProb = 0;
TaskParameters.GUI.SecExpProbUseAloneProb = 1;
TaskParameters.GUI.SecExpInverseStimDirRatio = 0;
TaskParameters.GUIMeta.SecExpStimDir.String = SecExpStimDir.String;
TaskParameters.GUI.SecExpStimIntensity = SecExpStimIntensity.HundredPercent;
TaskParameters.GUIMeta.SecExpStimIntensity.Style = 'popupmenu';
TaskParameters.GUIMeta.SecExpStimIntensity.String = SecExpStimIntensity.String;
TaskParameters.GUIPanels.Experiment = {'ExperimentType','SecExperimentType',...
    'SecExpUseProb','SecExpProbUseAloneProb','SecExpInverseStimDirRatio',...
    'SecExpStimIntensity'};
%% General
TaskParameters.GUI.ITI = 0; % (s)
TaskParameters.GUI.RewardAmount = 5;
TaskParameters.GUI.ChoiceDeadLine = 20;
TaskParameters.GUI.TimeOutIncorrectChoice = 0; % (s)
TaskParameters.GUI.TimeOutBrokeFixation = 0; % (s)
TaskParameters.GUI.TimeOutEarlyWithdrawal = 0; % (s)
TaskParameters.GUI.TimeOutMissedChoice = 0; % (s)
TaskParameters.GUI.TimeOutSkippedFeedback = 0; % (s)
TaskParameters.GUI.HabituateIgnoreIncorrect = 0; % (s)
TaskParameters.GUIMeta.HabituateIgnoreIncorrect.Style = 'checkbox';
TaskParameters.GUI.PlayNoiseforError = 0;
TaskParameters.GUIMeta.PlayNoiseforError.Style = 'checkbox';
TaskParameters.GUI.PCTimeout = true;
TaskParameters.GUIMeta.PCTimeout.Style = 'checkbox';
TaskParameters.GUI.WaitFinalPokeOutSec = 1;
TaskParameters.GUI.StartEasyTrials = 10;
TaskParameters.GUI.Percent50Fifty = 0;
TaskParameters.GUI.Ports_LMRAudLRAir = 123568;
TaskParameters.GUI.Wire1VideoTrigger = false;
TaskParameters.GUIMeta.Wire1VideoTrigger.Style = 'checkbox';
TaskParameters.GUIPanels.General = {'ITI','RewardAmount','ChoiceDeadLine','TimeOutIncorrectChoice',...
    'TimeOutBrokeFixation','TimeOutEarlyWithdrawal','TimeOutMissedChoice','TimeOutSkippedFeedback',...
    'HabituateIgnoreIncorrect','PlayNoiseforError','PCTimeout','WaitFinalPokeOutSec','StartEasyTrials',...
    'Percent50Fifty','Ports_LMRAudLRAir','Wire1VideoTrigger'};
%% StimDelay
TaskParameters.GUI.StimDelayAutoincrement = 0;
TaskParameters.GUIMeta.StimDelayAutoincrement.Style = 'checkbox';
TaskParameters.GUIMeta.StimDelayAutoincrement.String = 'Auto';
TaskParameters.GUI.StimDelayMin = 0.3;
TaskParameters.GUI.StimDelayMax = 0.6;
TaskParameters.GUI.StimDelayIncr = 0.01;
TaskParameters.GUI.StimDelayDecr = 0.01;
TaskParameters.GUI.StimDelayGrace = 0.1;
TaskParameters.GUI.StimDelay = TaskParameters.GUI.StimDelayMin;
TaskParameters.GUIMeta.StimDelay.Style = 'text';
TaskParameters.GUI.PreStimuDelayCntrReward = 0;
TaskParameters.GUIPanels.StimDelay = {'StimDelayAutoincrement','StimDelayMin','StimDelayMax','StimDelayIncr','StimDelayDecr','StimDelayGrace','PreStimuDelayCntrReward'};
%% FeedbackDelay
TaskParameters.GUI.FeedbackDelaySelection = FeedbackDelaySelection.Fix;
TaskParameters.GUIMeta.FeedbackDelaySelection.Style = 'popupmenu';
TaskParameters.GUIMeta.FeedbackDelaySelection.String = FeedbackDelaySelection.String;
TaskParameters.GUI.FeedbackDelayMin = 0;
TaskParameters.GUI.FeedbackDelayMax = 0;
TaskParameters.GUI.FeedbackDelayIncr = 0.01;
TaskParameters.GUI.FeedbackDelayDecr = 0.01;
TaskParameters.GUI.FeedbackDelayTau = 0.1;
TaskParameters.GUI.FeedbackDelayGrace = 0.4;
TaskParameters.GUI.IncorrectChoiceSignalType = IncorrectChoiceSignalType.BeepOnWire_1;
TaskParameters.GUIMeta.IncorrectChoiceSignalType.Style = 'popupmenu';
TaskParameters.GUIMeta.IncorrectChoiceSignalType.String = IncorrectChoiceSignalType.String;
TaskParameters.GUI.ITISignalType = ITISignalType.None;
TaskParameters.GUIMeta.ITISignalType.Style = 'popupmenu';
TaskParameters.GUIMeta.ITISignalType.String = ITISignalType.String;
TaskParameters.GUI.FeedbackDelay = TaskParameters.GUI.FeedbackDelayMin;
TaskParameters.GUIMeta.FeedbackDelay.Style = 'text';
TaskParameters.GUIPanels.FeedbackDelay = {'FeedbackDelaySelection','FeedbackDelayMin','FeedbackDelayMax','FeedbackDelayIncr','FeedbackDelayDecr','FeedbackDelayTau','FeedbackDelayGrace','IncorrectChoiceSignalType','ITISignalType'};
%% Air control
TaskParameters.GUI.CutAirStimDelay = true;
TaskParameters.GUIMeta.CutAirStimDelay.Style = 'checkbox';
TaskParameters.GUI.CutAirSampling = true;
TaskParameters.GUIMeta.CutAirSampling.Style = 'checkbox';
TaskParameters.GUI.CutAirReward = false;
TaskParameters.GUIMeta.CutAirReward.Style = 'checkbox';
TaskParameters.GUIPanels.AirControl = {'CutAirStimDelay','CutAirReward','CutAirSampling'};
%% Stimulus and Sampling Params
% Stimulus
TaskParameters.GUI.LeftBias = 0.5;
TaskParameters.GUIMeta.LeftBias.Style = 'slider';
TaskParameters.GUIMeta.LeftBias.Callback = @UpdateLeftBiasVal;
TaskParameters.GUI.LeftBiasVal = TaskParameters.GUI.LeftBias;
TaskParameters.GUIMeta.LeftBiasVal.Callback = @UpdateLeftBias;
TaskParameters.GUI.CorrectBias = false;
TaskParameters.GUIMeta.CorrectBias.Style = 'checkbox';
TaskParameters.GUI.CalcLeftBias = 0.5;
TaskParameters.GUIMeta.CalcLeftBias.Style = 'text';
TaskParameters.GUI.StimulusSelectionCriteria = StimulusSelectionCriteria.DiscretePairs;
TaskParameters.GUIMeta.StimulusSelectionCriteria.Style = 'popupmenu';
TaskParameters.GUIMeta.StimulusSelectionCriteria.String = StimulusSelectionCriteria.String;
TaskParameters.GUI.BetaDistAlphaNBeta = 0.3;
TaskParameters.GUI.OmegaTable.Omega =  [100:-5:55]';
TaskParameters.GUI.OmegaTable.RDK = (TaskParameters.GUI.OmegaTable.Omega - 50)*2;
TaskParameters.GUIMeta.OmegaTable.RDK.Style = 'text';
% Set first and last 3 values to be the effective ones
TaskParameters.GUI.OmegaTable.OmegaProb = zeros(numel(TaskParameters.GUI.OmegaTable.Omega),1);
TaskParameters.GUI.OmegaTable.OmegaProb(1) = 9; % 100
TaskParameters.GUI.OmegaTable.OmegaProb(2) = 8; % 95
TaskParameters.GUI.OmegaTable.OmegaProb(3) = 7; % 90
TaskParameters.GUI.OmegaTable.OmegaProb(4) = 6; % 85
TaskParameters.GUI.OmegaTable.OmegaProb(5) = 5; % 80
TaskParameters.GUI.OmegaTable.OmegaProb(6) = 4; % 75
TaskParameters.GUI.OmegaTable.OmegaProb(7) = 3; % 70
TaskParameters.GUI.OmegaTable.OmegaProb(8) = 2; % 65
TaskParameters.GUI.OmegaTable.OmegaProb(9) = 1; % 60
TaskParameters.GUI.OmegaTable.OmegaProb(10) = 0; % 55
TaskParameters.GUI.CurrentStim = 0;
TaskParameters.GUIMeta.CurrentStim.Style = 'text';
TaskParameters.GUIMeta.OmegaTable.Style = 'table';
TaskParameters.GUIMeta.OmegaTable.String = 'Omega probabilities';
TaskParameters.GUIMeta.OmegaTable.ColumnLabel = {'Stim %','RDK Coh', 'P(a)'};
TaskParameters.GUIMeta.OmegaTable.ColumnEditable = [true, false, true];
TaskParameters.GUIMeta.OmegaTable.Callback = @UpdateOmegaTableCb;
% Sampling
TaskParameters.GUI.StimulusTime = 0.3;
TaskParameters.GUI.RewardAfterMinSampling = false;
TaskParameters.GUIMeta.RewardAfterMinSampling.Style = 'checkbox';
TaskParameters.GUI.CenterPortRewAmount = 0.5;
TaskParameters.GUI.MinSampleMin = 0;
TaskParameters.GUI.MinSampleMax = 0;
TaskParameters.GUI.MinSampleType = MinSampleType.AutoIncr;
TaskParameters.GUIMeta.MinSampleType.Style = 'popupmenu';
TaskParameters.GUIMeta.MinSampleType.String = MinSampleType.String;
TaskParameters.GUI.MinSampleIncr = 0.05;
TaskParameters.GUI.MinSampleDecr = 0.02;
TaskParameters.GUI.MinSampleNumInterval = 1;
TaskParameters.GUI.MinSampleRandProb = 0;
TaskParameters.GUI.MinSample = TaskParameters.GUI.MinSampleMin;
TaskParameters.GUIMeta.MinSample.Style = 'text';
TaskParameters.GUI.PercentForcedLEDTrial = 0;
TaskParameters.GUI.PortLEDtoCueReward = false;
TaskParameters.GUIMeta.PortLEDtoCueReward.Style = 'checkbox';
TaskParameters.GUI.SecExpAloneMinSample = 0;
% This is a hidden field
TaskParameters.GUI.PrimaryOriginalMinSample = NaN;
% Auditory Specific
TaskParameters.GUI.SumRates = 100;
% Light Intensity Specific
TaskParameters.GUI.LeftPokeAttenPrcnt = 73;
TaskParameters.GUI.CenterPokeAttenPrcnt = 95;
TaskParameters.GUI.RightPokeAttenPrcnt = 73;
TaskParameters.GUI.UsePCSpeakers = 1;
TaskParameters.GUIMeta.UsePCSpeakers.Style = 'checkbox';
TaskParameters.GUI.AudStimType = 1;
TaskParameters.GUIMeta.AudStimType.Style = 'popupmenu';
TaskParameters.GUIMeta.AudStimType.String = AudStimType.String;
TaskParameters.GUI.LeftSpeakerAttenPrcnt = 80;
TaskParameters.GUI.RightSpeakerAttenPrcnt = 80;
TaskParameters.GUI.RightSpeakerAttenPrcnt = 80;
TaskParameters.GUI.StimAfterPokeOut = StimAfterPokeOut.NotUsed;
TaskParameters.GUIMeta.StimAfterPokeOut.Style = 'popupmenu';
TaskParameters.GUIMeta.StimAfterPokeOut.String = StimAfterPokeOut.String;
TaskParameters.GUI.BeepAfterMinSampling = false;
TaskParameters.GUIMeta.BeepAfterMinSampling.Style = 'checkbox';
TaskParameters.GUIPanels.PoissonClicks = {'SumRates'};
TaskParameters.GUIPanels.LightIntensity = {'LeftPokeAttenPrcnt','CenterPokeAttenPrcnt','RightPokeAttenPrcnt','StimAfterPokeOut', 'BeepAfterMinSampling'};
TaskParameters.GUIPanels.SoundIntensity = {'UsePCSpeakers','AudStimType','LeftSpeakerAttenPrcnt','RightSpeakerAttenPrcnt'};
TaskParameters.GUIPanels.StimulusSelection = {'OmegaTable','BetaDistAlphaNBeta',...
    'StimulusSelectionCriteria','LeftBias','LeftBiasVal','CorrectBias'};
TaskParameters.GUIPanels.Sampling = {'RewardAfterMinSampling','CenterPortRewAmount','MinSampleMin',...
                                     'MinSampleMax','MinSampleType','MinSampleIncr','MinSampleDecr','MinSampleNumInterval','MinSampleRandProb',...
                                     'StimulusTime','PortLEDtoCueReward','PercentForcedLEDTrial','SecExpAloneMinSample'};
%% Summary Tab
TaskParameters.GUI.MouseState = MouseState.FreelyMoving;
TaskParameters.GUIMeta.MouseState.Style = 'popupmenu';
TaskParameters.GUIMeta.MouseState.String = MouseState.String;
TaskParameters.GUI.MouseWeight = nan;
TaskParameters.GUI.Block = '';
TaskParameters.GUIMeta.Block.Style = 'text';
TaskParameters.GUI.Performance = '(Calc. after 1st trial)';
TaskParameters.GUIMeta.Performance.Style = 'text';
TaskParameters.GUI.AllPerformance = '(Calc. after 1st trial)';
TaskParameters.GUIMeta.AllPerformance.Style = 'text';
TaskParameters.GUI.IsCatch = 'false';
TaskParameters.GUIMeta.IsCatch.Style = 'text';
TaskParameters.GUI.IsOptoTrial = 'false';
TaskParameters.GUIMeta.IsOptoTrial.Style = 'text';
TaskParameters.GUIPanels.CurrentTrial = {'MouseState','MouseWeight',...
    'StimDelay','MinSample','CurrentStim','CalcLeftBias',...
    'FeedbackDelay','IsCatch','IsOptoTrial','Block','Performance',...
    'AllPerformance'};
% Extended Report Tab
TaskParameters.GUI.PrimExpPerformance = '(Calc. after PrimExp 1st trial)';
TaskParameters.GUI.PrimExpAllPerformance = '(Calc. after PrimExp 1st trial)';
TaskParameters.GUI.SecExpPerformance = '(Calc. after 2ndExp 1st trial)';
TaskParameters.GUI.SecExpAllPerformance = '(Calc. after 2ndExp 1st trial)';
TaskParameters.GUIMeta.PrimExpPerformance.Style = 'text';
TaskParameters.GUIMeta.PrimExpAllPerformance.Style = 'text';
TaskParameters.GUIMeta.SecExpPerformance.Style = 'text';
TaskParameters.GUIMeta.SecExpAllPerformance.Style = 'text';
TaskParameters.GUIPanels.ExtendedReport = {'PrimExpPerformance',...
    'PrimExpAllPerformance','SecExpPerformance','SecExpAllPerformance'};
% General Visual options
TaskParameters.GUI.VisualStimAnglePortRight = VisualStimAngle.Degrees90;
TaskParameters.GUIMeta.VisualStimAnglePortRight.Style = 'popupmenu';
TaskParameters.GUIMeta.VisualStimAnglePortRight.String = VisualStimAngle.String;
TaskParameters.GUI.VisualStimAnglePortLeft = VisualStimAngle.Degrees270;
TaskParameters.GUIMeta.VisualStimAnglePortLeft.Style = 'popupmenu';
TaskParameters.GUIMeta.VisualStimAnglePortLeft.String = VisualStimAngle.String;
TaskParameters.GUI.circleRDK = 0;
TaskParameters.GUIMeta.circleRDK.Style = 'checkbox';
TaskParameters.GUI.screenDistCm = 30;
TaskParameters.GUI.screenWidthCm = 20;
TaskParameters.GUI.apertureSizeWidth = 36; % size of circular aperture [w,h] in degrees
TaskParameters.GUI.apertureSizeHeight = 36;
TaskParameters.GUI.centerX = 0; % center of render of stimulus (x,y)
TaskParameters.GUI.centerY = 0;
TaskParameters.GUIPanels.VisualGeneral = {'VisualStimAnglePortRight',...
    'VisualStimAnglePortLeft','circleRDK','screenDistCm','screenWidthCm',...
    'apertureSizeWidth','apertureSizeHeight','centerX','centerY'};
% Random dots options
% Use 20% of the screen size
TaskParameters.GUI.drawRatio = 0.2;
TaskParameters.GUI.circleArea = (pi*((TaskParameters.GUI.apertureSizeWidth/2).^2)); % assume apertureSize is the diameter
TaskParameters.GUIMeta.circleArea.Style = 'text';
TaskParameters.GUI.nDots = round(TaskParameters.GUI.circleArea * 0.05);
TaskParameters.GUIMeta.nDots.Style = 'text';
%dotsParams.nDots = 300;     % total number of dots
TaskParameters.GUI.dotSizeInDegs = 2; % size of dots in degrees
TaskParameters.GUI.dotSpeedDegsPerSec = 25; %degrees/second
TaskParameters.GUI.dotLifetimeSecs = 1;  %lifetime of each dot sec
TaskParameters.GUIPanels.RandomDots = {'drawRatio','circleArea','nDots',...
    'dotSizeInDegs','dotSpeedDegsPerSec','dotLifetimeSecs'};
% Random dots pulse
TaskParameters.GUI.dotsPulseCohr = 20;
TaskParameters.GUI.dotsPulseProb = 0;
TaskParameters.GUI.dotsPulseMinDur = 0.3;
TaskParameters.GUI.dotsPulseOffset_Neg1Rnd = -1;
TaskParameters.GUI.LastPulse = '';
TaskParameters.GUIMeta.LastPulse.Style = 'text';
TaskParameters.GUIPanels.RandomDotsPulse = {'dotsPulseCohr', 'dotsPulseProb',...
    'dotsPulseMinDur', 'dotsPulseOffset_Neg1Rnd', 'LastPulse'};
% Grating orientation specific
TaskParameters.GUI.gaborSizeFactor = 1.2;
TaskParameters.GUI.phase = 0; % Phase of the wave, goes between 0 to 360
% Spatial Frequency (Cycles Per Pixel)
% One Cycle = Grey-Black-Grey-White-Grey i.e. One Black and One White Lobe
TaskParameters.GUI.numCycles = 20;
TaskParameters.GUI.cyclesPerSecondDrift = 5;
TaskParameters.GUI.gaussianFilterRatio = 0.1; % Gamma and circle blurness around grating
TaskParameters.GUIPanels.Grating = {'gaborSizeFactor','phase','numCycles',...
    'cyclesPerSecondDrift', 'gaussianFilterRatio'};
%% Plots
%Show Plots/
TaskParameters.GUI.ShowPsycStim = 1;
TaskParameters.GUIMeta.ShowPsycStim.Style = 'checkbox';
TaskParameters.GUI.ShowVevaiometric = 1;
TaskParameters.GUIMeta.ShowVevaiometric.Style = 'checkbox';
TaskParameters.GUI.ShowTrialRate = 1;
TaskParameters.GUIMeta.ShowTrialRate.Style = 'checkbox';
TaskParameters.GUI.ShowFix = 1;
TaskParameters.GUIMeta.ShowFix.Style = 'checkbox';
TaskParameters.GUI.ShowST = 1;
TaskParameters.GUIMeta.ShowST.Style = 'checkbox';
TaskParameters.GUI.ShowFeedback = 1;
TaskParameters.GUIMeta.ShowFeedback.Style = 'checkbox';
TaskParameters.GUIPanels.ShowPlots = {'ShowPsycStim','ShowVevaiometric','ShowTrialRate','ShowFix','ShowST','ShowFeedback'};
%Vevaiometric
TaskParameters.GUI.VevaiometricYLim = 20;
TaskParameters.GUI.VevaiometricMinWT = 0.5;
TaskParameters.GUI.VevaiometricNBin = 8;
TaskParameters.GUI.VevaiometricShowPoints = 1;
TaskParameters.GUIMeta.VevaiometricShowPoints.Style = 'checkbox';
TaskParameters.GUIPanels.Vevaiometric = {'VevaiometricYLim', ...
    'VevaiometricMinWT','VevaiometricNBin','VevaiometricShowPoints'};
%% Blocks
TaskParameters.GUI.Blk2Policy = Blk2Policy.NotUsed;
TaskParameters.GUIMeta.Blk2Policy.Style = 'popupmenu';
TaskParameters.GUIMeta.Blk2Policy.String = Blk2Policy.String;
TaskParameters.GUI.BlkSwitchCond = BlkSwitchCond.TrialsRandCountWithinLimits;
TaskParameters.GUIMeta.BlkSwitchCond.Style = 'popupmenu';
TaskParameters.GUIMeta.BlkSwitchCond.String = BlkSwitchCond.String;
TaskParameters.GUI.BlkSwitchLimitBot = 18;
TaskParameters.GUI.BlkSwitchLimitTop = 22;
TaskParameters.GUI.BlkSwitchPerfMinGoal = 80;
TaskParameters.GUI.BlkSwitchPerfMinGoalNumTrials = 4;
TaskParameters.GUIPanels.Block2 = {'Blk2Policy', 'BlkSwitchCond',...
    'BlkSwitchLimitBot','BlkSwitchLimitTop','BlkSwitchPerfMinGoal',...
    'BlkSwitchPerfMinGoalNumTrials'};
%Optogenetics
TaskParameters.GUI.OptoProb = 0;
TaskParameters.GUI.OptoOr2P = TTLWireUsage.Optogenetics;
TaskParameters.GUIMeta.OptoOr2P.Style = 'popupmenu';
TaskParameters.GUIMeta.OptoOr2P.String = TTLWireUsage.String;
TaskParameters.GUI.OptoStartState1 = MatrixState.stimulus_delivery;
TaskParameters.GUIMeta.OptoStartState1.Style = 'popupmenu';
TaskParameters.GUIMeta.OptoStartState1.String = MatrixState.String;
TaskParameters.GUI.OptoStartDelay = 0;
TaskParameters.GUI.OptoMaxTime = 10;
TaskParameters.GUI.OptoEndState1 = MatrixState.WaitCenterPortOut;
TaskParameters.GUIMeta.OptoEndState1.Style = 'popupmenu';
TaskParameters.GUIMeta.OptoEndState1.String = MatrixState.String;
TaskParameters.GUI.OptoEndState2 = MatrixState.WaitForChoice;
TaskParameters.GUIMeta.OptoEndState2.Style = 'popupmenu';
TaskParameters.GUIMeta.OptoEndState2.String = MatrixState.String;
TaskParameters.GUI.OptoBrainRegion = BrainRegion.V1_L;
TaskParameters.GUIMeta.OptoBrainRegion.Style = 'popupmenu';
TaskParameters.GUIMeta.OptoBrainRegion.String = BrainRegion.String;
TaskParameters.GUIPanels.Optogenetics = {'OptoProb', 'OptoOr2P',...
   'OptoStartState1', 'OptoStartDelay','OptoMaxTime',...
   'OptoEndState1','OptoEndState2','OptoBrainRegion','IsOptoTrial'};
% Catch Trials
TaskParameters.GUI.CatchTable.Omega = [100:-5:55]';
TaskParameters.GUIMeta.CatchTable.Omega.Style = 'text';
TaskParameters.GUI.CatchTable.EveryMin = zeros(numel(TaskParameters.GUI.CatchTable.Omega),1);
TaskParameters.GUI.CatchTable.EveryMax = zeros(numel(TaskParameters.GUI.CatchTable.Omega),1);
TaskParameters.GUIMeta.CatchTable.Style = 'table';
TaskParameters.GUIMeta.CatchTable.String = 'Catch Distribution';
TaskParameters.GUIMeta.CatchTable.ColumnLabel = {'Omega','EveryMin', 'EveryMax'};
TaskParameters.GUIMeta.CatchTable.ColumnEditable = [false, true, true];
TaskParameters.GUI.CatchError = false;
TaskParameters.GUIMeta.CatchError.Style = 'checkbox';
TaskParameters.GUI.CatchCanComeAfterErr = 0;
TaskParameters.GUIMeta.CatchCanComeAfterErr.Style = 'checkbox';
TaskParameters.GUI.CatchSepLeftRight = 0;
TaskParameters.GUIMeta.CatchSepLeftRight .Style = 'checkbox';
TaskParameters.GUI.CatchCorrectOnlyCounts = 0;
TaskParameters.GUIMeta.CatchCorrectOnlyCounts.Style = 'checkbox';
TaskParameters.GUIPanels.CatchDist = {'CatchTable','CatchError',...
  'CatchCanComeAfterErr','CatchSepLeftRight','CatchCorrectOnlyCounts'};

%%
TaskParameters.GUI = orderfields(TaskParameters.GUI);
%% Tabs
TaskParameters.GUITabs.General = {'CurrentTrial','Experiment','General','FeedbackDelay','StimDelay'};
TaskParameters.GUITabs.Sampling = {'CurrentTrial','LightIntensity','Sampling','StimulusSelection'};
TaskParameters.GUITabs.Blocks = {'CurrentTrial','Block2','ExtendedReport', 'CatchDist'};
TaskParameters.GUITabs.Visual = {'CurrentTrial','Grating','RandomDots','VisualGeneral','RandomDotsPulse'};
TaskParameters.GUITabs.Auditory = {'CurrentTrial','PoissonClicks','SoundIntensity',};
TaskParameters.GUITabs.Triggers = {'Optogenetics','AirControl'};
TaskParameters.GUITabs.Plots = {'ShowPlots','Vevaiometric'};
%%Non-GUI Parameters (but saved)
TaskParameters.Figures.OutcomePlot.Position = [200, 200, 1000, 400];
TaskParameters.Figures.ParameterGUI.Position =  [9, 454, 1474, 562];
TaskParameters.GUI.GUIVer = GUICurVer;
TaskParameters.GUI.ComputerName = 'Unassigned';
end
