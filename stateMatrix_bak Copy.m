function sma = stateMatrix(iTrial)
global BpodSystem
global TaskParameters

function MatStr = str(matrix_state)
    MatStr = MatrixState.String(matrix_state);
end
CurTrial = BpodSystem.Data.Custom.Trials(iTrial);
%% Define ports
LeftPort = floor(mod(TaskParameters.GUI.Ports_LMRAudLRAir/100000,10));
CenterPort = floor(mod(TaskParameters.GUI.Ports_LMRAudLRAir/10000,10));
RightPort = floor(mod(TaskParameters.GUI.Ports_LMRAudLRAir/1000,10));
AirSolenoid = mod(TaskParameters.GUI.Ports_LMRAudLRAir,10);
LeftPortOut = strcat('Port',num2str(LeftPort),'Out');
CenterPortOut = strcat('Port',num2str(CenterPort),'Out');
RightPortOut = strcat('Port',num2str(RightPort),'Out');
LeftPortIn = strcat('Port',num2str(LeftPort),'In');
CenterPortIn = strcat('Port',num2str(CenterPort),'In');
RightPortIn = strcat('Port',num2str(RightPort),'In');

% Emulator timers doesn't work if time is less than 10 msec
MinDur = iff(BpodSystem.EmulatorMode, 0.01, 0.001);
% Duration of the TTL signal to denote start and end of trial for 2P
WireTTLDuration=0.02;

% PWM = (255 * (100-Attenuation))/100
LeftPWM = round((100-TaskParameters.GUI.LeftPokeAttenPrcnt) * 2.55);
CenterPWM = round((100-TaskParameters.GUI.CenterPokeAttenPrcnt) * 2.55);
RightPWM = round((100-TaskParameters.GUI.RightPokeAttenPrcnt) * 2.55);
LEDErrorRate = 0.1;

IsLeftRewarded = CurTrial.LeftRewarded;

[StartStim, ContStim, StopStim, TaskParameters.GUI,...
 BpodSystem.Data.Custom.drawParams] = HandleStateMatrixStim(TaskParameters.GUI,...
    CurTrial, LeftPort, LeftPWM,RightPort, RightPWM,...
    BpodSystem.Data.Custom.soundParams,...
    BpodSystem.SystemSettings.dotsMapped_file, BpodSystem.Path.CurrentDataFile);
switch TaskParameters.GUI.StimAfterPokeOut
  case StimAfterPokeOut.NotUsed
    [WaitForDecisionStim, WaitFeedbackStim, WaitForPokeOutStim] = deal(StopStim);
  case StimAfterPokeOut.UntilFeedbackStart
    WaitForDecisionStim = ContStim;
    [WaitFeedbackStim, WaitForPokeOutStim] = deal(StopStim);
  case StimAfterPokeOut.UntilFeedbackEnd
    [WaitForDecisionStim, WaitFeedbackStim] = deal(ContStim);
    WaitForPokeOutStim = StopStim;
  case StimAfterPokeOut.UntilEndOfTrial
    [WaitForDecisionStim, WaitFeedbackStim, WaitForPokeOutStim]= deal(ContStim);
end
% Valve opening is a bitmap. Open each valve separately by raising 2 to
% the power of port number - 1
LeftValve = 2^(LeftPort-1);
CenterValve = 2^(CenterPort-1);
RightValve = 2^(RightPort-1);
AirSolenoidOn = 2^(AirSolenoid-1);
AirSolenoidOff = 0;

LeftValveTime  = GetValveTimes(CurTrial.RewardMagnitude(1), LeftPort);
CenterValveTime  = GetValveTimes(CurTrial.CenterPortRewAmount, CenterPort);
RightValveTime  = GetValveTimes(CurTrial.RewardMagnitude(2), RightPort);

RewardIn = iff(IsLeftRewarded, LeftPortIn, RightPortIn);
RewardOut = iff(IsLeftRewarded, LeftPortOut, RightPortOut);
PunishIn = iff(IsLeftRewarded, RightPortIn, LeftPortIn);
PunishOut = iff(IsLeftRewarded, RightPortOut, LeftPortOut);
IncorrectConsequence = iff(~TaskParameters.GUI.HabituateIgnoreIncorrect,...
                           str(MatrixState.WaitForPunishStart),...
                           str(MatrixState.RegisterWrongWaitCorrect));
ValveTime = iff(IsLeftRewarded, LeftValveTime, RightValveTime);
ValveCode = iff(IsLeftRewarded, LeftValve, RightValve);
% CatchTrial
if ~CurTrial.CatchTrial
    RewardIfNotCatch = {'ValveState', ValveCode};
    RewardDur = ValveTime;
else
    RewardIfNotCatch = {};
    RewardDur = MinDur; %Const.FEEDBACK_CATCH_MAX_SEC - TaskParameters.GUI.FeedbackDelay;
end

% Incorrect Choice signal
if TaskParameters.GUI.CatchError || TaskParameters.GUI.IncorrectChoiceSignalType == IncorrectChoiceSignalType.None
    PunishmentDuration = MinDur;%iff(TaskParameters.GUI.CatchError,Const.FEEDBACK_CATCH_MAX_SEC,MinDur);
    IncorrectChoice_Signal = {};
elseif TaskParameters.GUI.IncorrectChoiceSignalType == IncorrectChoiceSignalType.NoisePulsePal
    PunishmentDuration = MinDur;
    IncorrectChoice_Signal = {'SoftCode', 11};
elseif TaskParameters.GUI.IncorrectChoiceSignalType == IncorrectChoiceSignalType.BeepOnWire_1
    PunishmentDuration = 0.25;
    IncorrectChoice_Signal = {'WireState', 2^0};
elseif TaskParameters.GUI.IncorrectChoiceSignalType == IncorrectChoiceSignalType.PortLED
    PunishmentDuration = 0.1;
    IncorrectChoice_Signal = {strcat('PWM',num2str(LeftPort)),LeftPWM,strcat('PWM',num2str(CenterPort)),CenterPWM,strcat('PWM',num2str(RightPort)),RightPWM};
else
    assert(false, 'Unexpected IncorrectChoiceSignalType value');
end

ValveOrWireSolenoid='ValveState';
if TaskParameters.GUI.CutAirStimDelay && TaskParameters.GUI.CutAirSampling
    AirFlowStimDelayOff = {ValveOrWireSolenoid, AirSolenoidOn};
    AirFlowStimDelayOn = {};
    AirFlowSamplingOff = {ValveOrWireSolenoid, AirSolenoidOn}; % Must set it on again
    AirFlowSamplingOn = {ValveOrWireSolenoid, AirSolenoidOff};
elseif TaskParameters.GUI.CutAirStimDelay
    AirFlowStimDelayOff = {ValveOrWireSolenoid, AirSolenoidOn};
    AirFlowStimDelayOn = {ValveOrWireSolenoid, AirSolenoidOff};
    AirFlowSamplingOff = {};
    AirFlowSamplingOn = {};
elseif TaskParameters.GUI.CutAirSampling
    AirFlowStimDelayOff = {};
    AirFlowStimDelayOn = {};
    AirFlowSamplingOff = {ValveOrWireSolenoid, AirSolenoidOn};
    AirFlowSamplingOn = {ValveOrWireSolenoid, AirSolenoidOff};
else
    AirFlowStimDelayOff = {};
    AirFlowStimDelayOn = {};
    AirFlowSamplingOff = {};
    AirFlowSamplingOn = {};
end

if TaskParameters.GUI.CutAirReward
    AirFlowRewardOff = {'ValveState', AirSolenoidOn};
else
    AirFlowRewardOff = {};
end
AirFlowRewardOn = {'ValveState', AirSolenoidOff};

% Check if to play beep at end of minimum sampling
MinSampleBeep = iff(TaskParameters.GUI.BeepAfterMinSampling, {'SoftCode',12}, {});
MinSampleBeepDuration = iff(TaskParameters.GUI.BeepAfterMinSampling, MinDur, 0);
% GUI option RewardAfterMinSampling
% If center-reward is enabled, then a reward is given once MinSample
% is over and no further sampling is given.
RewardCenterPort = iff(TaskParameters.GUI.RewardAfterMinSampling, {'ValveState',CenterValve}, {});
Timer_CPRD = iff(TaskParameters.GUI.RewardAfterMinSampling, CenterValveTime, MinDur);

% White Noise played as Error Feedback
ErrorFeedback = iff(TaskParameters.GUI.PlayNoiseforError, {'SoftCode',11}, {});

% FeedbackDelayCorrect = iff(CurTrial.CatchTrial, Const.FEEDBACK_CATCH_MAX_SEC, TaskParameters.GUI.FeedbackDelay);
% GUI option CatchError
% FeedbackDelayError = iff(TaskParameters.GUI.CatchError, Const.FEEDBACK_CATCH_MAX_SEC, TaskParameters.GUI.FeedbackDelay);
SkippedFeedbackSignal = iff(TaskParameters.GUI.CatchError, {}, ErrorFeedback);

% ITI signal
if TaskParameters.GUI.ITISignalType == ITISignalType.Beep
    ITI_Signal_Duration = MinDur;
    ITI_Signal = {'SoftCode', 12};
elseif TaskParameters.GUI.ITISignalType == ITISignalType.PortLED
    ITI_Signal_Duration = 0.1;
    ITI_Signal = {strcat('PWM',num2str(LeftPort)),LeftPWM,strcat('PWM',num2str(CenterPort)),CenterPWM,strcat('PWM',num2str(RightPort)),RightPWM};
elseif TaskParameters.GUI.ITISignalType == ITISignalType.None
    ITI_Signal_Duration = MinDur;
    ITI_Signal = {};
else
    assert(false, 'Unexpected ITISignalType value');
end

%Wire1 settings
Wire1OutError = iff(TaskParameters.GUI.Wire1VideoTrigger, {'WireState', 2^1}, {});
Wire1OutCorrect = iff(TaskParameters.GUI.Wire1VideoTrigger && CurTrial.CatchTrial, {'WireState', 2^1}, {});

% LED on the side lateral port to cue the rewarded side at the beginning of
% the training. On auditory discrimination task, both lateral ports are
% illuminated after end of stimulus delivery.
if CurTrial.ForcedLEDTrial
    RewardedPort = iff(IsLeftRewarded, LeftPort, RightPort);
    RewardedPortPWM = iff(IsLeftRewarded, LeftPWM, RightPWM);
    ForcedLEDStim = {strcat('PWM',num2str(RewardedPort)),RewardedPortPWM};
elseif TaskParameters.GUI.ExperimentType == ExperimentType.Auditory
    ForcedLEDStim = {strcat('PWM',num2str(LeftPort)),LeftPWM,strcat('PWM',num2str(RightPort)),RightPWM};
else
    ForcedLEDStim = {};
end

% Softcode handler for iTrial == 1 in HomeCage to close training chamber door
CloseChamber = iff(iTrial == 1 && BpodSystem.Data.Custom.IsHomeCage, {'SoftCode', 30}, {});

%% Timers and conditions IDs
function TimerName = TimerName(TimerID)
    TimerName = sprintf('GlobalTimer%d',TimerID);
end
function TimerEventName = TimerEnd(TimerID)
    TimerEventName = sprintf('%s_End',TimerName(TimerID));
end
function OutputEvent = TimerTrig(TimerID)
    % Bpod2 emulator requires some strange formatting compared to the
    % actual real board running.
    EncTrigger = iff(BpodSystem.SystemSettings.IsVer2 && ...
                     BpodSystem.EmulatorMode, dec2bin(TimerID, 3), TimerID);
    OutputEvent = {'GlobalTimerTrig',EncTrigger};
end
% TODO: Make this work with Bpod v1 by taking taking state to transition to as 
% the second argument and returning no action if it's V1.
function ConditionName = Condition(ConditionID)
    ConditionName = sprintf('Condition%d',ConditionID);
end
IfTimerIsOff = @(x){Condition(x)}; % An alias for better redability
% This is the only condition not tied to a timer:
CondIDCenterPortIn = 1;
% Timers and their conditions:
TimerIDChoiceDeadLine = 1;
TimerIDFeedbackDelayCorrect = 2;
%CondIDFeedbackDelayCorrect = 2;
TimerIDFeedbackDelayPunish = 3;
%CondIDFeedbackDelayPunish = 3;
TimerIDIncorrectTimeout = 4;
CondIDIncorrectTimeout = 4;
TimerIDITI = 5;
ConditionIDITI = 5;

PCTimeout = TaskParameters.GUI.PCTimeout;
ITITime = iff(~PCTimeout,TaskParameters.GUI.ITI,MinDur);
%% Build state matrix
sma = NewStateMatrix();
sma = SetGlobalTimer(sma,TimerIDChoiceDeadLine,TaskParameters.GUI.ChoiceDeadLine);
sma = SetGlobalTimer(sma,TimerIDFeedbackDelayCorrect,...
                     iff(CurTrial.CatchTrial,Const.FEEDBACK_CATCH_MAX_SEC,...
                                             max(TaskParameters.GUI.FeedbackDelay, MinDur)));
%sma = SetCondition(sma,CondIDFeedbackDelayCorrect, TimerName(TimerIDFeedbackDelayCorrect), 0);
sma = SetGlobalTimer(sma,TimerIDFeedbackDelayPunish,...
                     iff(TaskParameters.GUI.CatchError,Const.FEEDBACK_CATCH_MAX_SEC,...
                                                       max(TaskParameters.GUI.FeedbackDelay,MinDur)));
%sma = SetCondition(sma,CondIDFeedbackDelayPunish, TimerName(TimerIDFeedbackDelayPunish), 0);
sma = SetGlobalTimer(sma,TimerIDIncorrectTimeout,...
                     iff(~PCTimeout,TaskParameters.GUI.TimeOutIncorrectChoice+ITITime,MinDur));
sma = SetCondition(sma,CondIDIncorrectTimeout,TimerName(TimerIDIncorrectTimeout),0);
sma = SetGlobalTimer(sma,TimerIDITI,ITITime);
sma = SetCondition(sma,ConditionIDITI,TimerName(TimerIDITI), 0);
sma = AddState(sma, 'Name', str(MatrixState.ITI_Signal),...
    'Timer',ITI_Signal_Duration,...
    'StateChangeConditions',{'Tup',str(MatrixState.WaitForCenterPoke)},...
    'OutputActions',ITI_Signal);
WaterForCenterPokeChanges = {CenterPortIn, str(MatrixState.PreStimReward)};
if BpodSystem.SystemSettings.IsVer2
    sma = SetCondition(sma, CondIDCenterPortIn, strcat('Port',num2str(CenterPort)), 1);
    WaterForCenterPokeChanges = [WaterForCenterPokeChanges,...
                                 {'Condition1', str(MatrixState.PreStimReward)}];
end
sma = AddState(sma, 'Name', str(MatrixState.WaitForCenterPoke),...
    'Timer', 0,...
    'StateChangeConditions', WaterForCenterPokeChanges,...
    'OutputActions', {strcat('PWM',num2str(CenterPort)),CenterPWM});
sma = AddState(sma, 'Name', str(MatrixState.PreStimReward),...
    'Timer', iff(TaskParameters.GUI.PreStimuDelayCntrReward,...
                 GetValveTimes(TaskParameters.GUI.PreStimuDelayCntrReward, CenterPort),MinDur),...
    'StateChangeConditions', {'Tup', str(MatrixState.TriggerWaitForStimulus)},...
    'OutputActions', iff(TaskParameters.GUI.PreStimuDelayCntrReward,{'ValveState',CenterValve},[]));
% The next method is useful to close the 2-photon shutter. It is enabled
% by setting Optogenetics StartState to this state and end state to ITI.
sma = AddState(sma, 'Name', str(MatrixState.TriggerWaitForStimulus),...
    'Timer', WireTTLDuration,...
    'StateChangeConditions', {CenterPortOut,str(MatrixState.StimDelayGrace),'Tup',str(MatrixState.WaitForStimulus)},...
    'OutputActions', [CloseChamber AirFlowStimDelayOff]);
sma = AddState(sma, 'Name', str(MatrixState.WaitForStimulus),...
    'Timer', max(0, TaskParameters.GUI.StimDelay - WireTTLDuration),...
    'StateChangeConditions', {CenterPortOut,str(MatrixState.StimDelayGrace),'Tup', str(MatrixState.stimulus_delivery)},...
    'OutputActions', AirFlowStimDelayOff);
sma = AddState(sma, 'Name', str(MatrixState.StimDelayGrace),...
    'Timer',TaskParameters.GUI.StimDelayGrace,...
    'StateChangeConditions',{'Tup',str(MatrixState.broke_fixation),CenterPortIn,str(MatrixState.TriggerWaitForStimulus)},...
    'OutputActions', AirFlowStimDelayOff);
sma = AddState(sma, 'Name', str(MatrixState.broke_fixation),...
    'Timer',iff(~PCTimeout, TaskParameters.GUI.TimeOutBrokeFixation, MinDur),...
    'StateChangeConditions',{'Tup',str(MatrixState.ITI)},...
    'OutputActions', ErrorFeedback);
sma = AddState(sma, 'Name', str(MatrixState.stimulus_delivery),...
    'Timer', max(MinDur,TaskParameters.GUI.MinSample-MinSampleBeepDuration-Timer_CPRD),...
    'StateChangeConditions', {CenterPortOut,str(MatrixState.early_withdrawal),'Tup',str(MatrixState.BeepMinSampling)},...
    'OutputActions', [StartStim AirFlowSamplingOff]);
sma = AddState(sma, 'Name', str(MatrixState.early_withdrawal),...
    'Timer',0,...
    'StateChangeConditions',{'Tup',str(MatrixState.timeOut_EarlyWithdrawal)},...
    'OutputActions', [StopStim AirFlowSamplingOn {'SoftCode',1}]);
sma = AddState(sma, 'Name', str(MatrixState.BeepMinSampling),...
    'Timer', MinSampleBeepDuration,...
    'StateChangeConditions', {CenterPortOut,str(MatrixState.TriggerWaitChoiceTimer),'Tup',str(MatrixState.CenterPortRewardDelivery)},...
    'OutputActions', [ContStim MinSampleBeep]);
sma = AddState(sma, 'Name', str(MatrixState.CenterPortRewardDelivery),...
    'Timer', Timer_CPRD,...
    'StateChangeConditions', {CenterPortOut,str(MatrixState.TriggerWaitChoiceTimer),'Tup',str(MatrixState.StimulusTime)},...
    'OutputActions', [ContStim RewardCenterPort]);
sma = AddState(sma, 'Name', str(MatrixState.StimulusTime),...
    'Timer', max(0, TaskParameters.GUI.StimulusTime-TaskParameters.GUI.MinSample-Timer_CPRD-MinSampleBeepDuration),...
    'StateChangeConditions', {CenterPortOut,str(MatrixState.TriggerWaitChoiceTimer),'Tup',str(MatrixState.WaitCenterPortOut)},...
    'OutputActions', ContStim);
% TODO: Stop stimulus is fired twice in case of center reward and then wait
% for choice. Fix it such that it'll be always fired once.
sma = AddState(sma, 'Name', str(MatrixState.TriggerWaitChoiceTimer),...
    'Timer',0,...
    'StateChangeConditions', {'Tup',str(MatrixState.WaitForChoice)},...
    'OutputActions',[WaitForDecisionStim ForcedLEDStim TimerTrig(TimerIDChoiceDeadLine)]);
sma = AddState(sma, 'Name', str(MatrixState.WaitCenterPortOut),...
    'Timer', 0,...
    'StateChangeConditions', [CenterPortOut,str(MatrixState.WaitForChoice),...
                              RewardIn,str(MatrixState.WaitForRewardStart),...
                              PunishIn, IncorrectConsequence,...
                              {TimerEnd(TimerIDChoiceDeadLine),str(MatrixState.timeOut_missed_choice)}],...
    'OutputActions', [WaitForDecisionStim ForcedLEDStim TimerTrig(TimerIDChoiceDeadLine)]);
sma = AddState(sma, 'Name', str(MatrixState.WaitForChoice),...
    'Timer',0,...
    'StateChangeConditions', [RewardIn,str(MatrixState.WaitForRewardStart),...
                              PunishIn, IncorrectConsequence,...
                              {TimerEnd(TimerIDChoiceDeadLine),str(MatrixState.timeOut_missed_choice)}],...
    'OutputActions',[WaitForDecisionStim ForcedLEDStim]);
sma = AddState(sma, 'Name',str(MatrixState.WaitForRewardStart),...
    'Timer',0,...
    'StateChangeConditions', {'Tup',str(MatrixState.WaitForReward)},...
    'OutputActions', [Wire1OutCorrect WaitFeedbackStim TimerTrig(TimerIDFeedbackDelayCorrect)]);
sma = AddState(sma, 'Name',str(MatrixState.WaitForReward),...
    'Timer',0,...
    'StateChangeConditions', {TimerEnd(TimerIDFeedbackDelayCorrect),str(MatrixState.Reward),...
                              ...%IfTimerIsOff(CondIDFeedbackDelayCorrect),str(MatrixState.Reward),...
                              RewardOut,str(MatrixState.RewardGrace)},...
    'OutputActions', [WaitFeedbackStim AirFlowRewardOff]);
sma = AddState(sma, 'Name',str(MatrixState.RewardGrace),...
    'Timer',TaskParameters.GUI.FeedbackDelayGrace,...
    'StateChangeConditions', {RewardIn,str(MatrixState.WaitForReward),...
                              'Tup',str(MatrixState.timeOut_SkippedFeedback),...
                              TimerEnd(TimerIDFeedbackDelayCorrect),str(MatrixState.timeOut_SkippedFeedback),...
                              CenterPortIn,str(MatrixState.timeOut_SkippedFeedback),...
                              PunishIn,str(MatrixState.timeOut_SkippedFeedback)},...
    'OutputActions', [WaitFeedbackStim AirFlowRewardOn]);
sma = AddState(sma, 'Name',str(MatrixState.Reward),...
    'Timer',RewardDur,...
    'StateChangeConditions', {'Tup',str(MatrixState.WaitRewardOut)},...
    'OutputActions', [WaitFeedbackStim RewardIfNotCatch]);
sma = AddState(sma, 'Name',str(MatrixState.WaitRewardOut),...
    'Timer',TaskParameters.GUI.WaitFinalPokeOutSec,...
    'StateChangeConditions', {'Tup',str(MatrixState.ext_ITI),...
                              RewardOut,str(MatrixState.ext_ITI)},...
    'OutputActions', [TimerTrig(TimerIDITI) WaitForPokeOutStim]);
sma = AddState(sma, 'Name',str(MatrixState.RegisterWrongWaitCorrect),...
    'Timer',0,...
    'StateChangeConditions', {'Tup',str(MatrixState.WaitForChoice)},...
    'OutputActions', WaitFeedbackStim);
sma = AddState(sma, 'Name',str(MatrixState.WaitForPunishStart),...
    'Timer',0,...
    'StateChangeConditions', {'Tup',str(MatrixState.WaitForPunish)},...
    'OutputActions',[Wire1OutError WaitFeedbackStim TimerTrig(TimerIDFeedbackDelayPunish)]);
sma = AddState(sma, 'Name',str(MatrixState.WaitForPunish),...
    'Timer',0,...
    'StateChangeConditions', {TimerEnd(TimerIDFeedbackDelayPunish),str(MatrixState.Punishment),...
                              ...%IfTimerIsOff(CondIDFeedbackDelayPunish),str(MatrixState.Punishment),...
                              PunishOut,str(MatrixState.PunishGrace)},...
    'OutputActions', [WaitFeedbackStim AirFlowRewardOff]);
sma = AddState(sma, 'Name',str(MatrixState.PunishGrace),...
    'Timer',TaskParameters.GUI.FeedbackDelayGrace,...
    'StateChangeConditions', {PunishIn,str(MatrixState.WaitForPunish),...
                              'Tup',str(MatrixState.timeOut_SkippedFeedback),...
                              TimerEnd(TimerIDFeedbackDelayPunish),str(MatrixState.timeOut_SkippedFeedback),...
                              CenterPortIn,str(MatrixState.timeOut_SkippedFeedback),...
                              RewardIn,str(MatrixState.timeOut_SkippedFeedback)},...
    'OutputActions', WaitFeedbackStim);
sma = AddState(sma, 'Name', str(MatrixState.Punishment),...
    'Timer',PunishmentDuration,...
    'StateChangeConditions',{'Tup',str(MatrixState.WaitPunishOut),PunishOut,str(MatrixState.timeOut_IncorrectChoice)},...
    'OutputActions',[IncorrectChoice_Signal WaitFeedbackStim AirFlowRewardOn]);
sma = AddState(sma, 'Name',str(MatrixState.WaitPunishOut),...
    'Timer',TaskParameters.GUI.WaitFinalPokeOutSec,...
    'StateChangeConditions', {'Tup',str(MatrixState.timeOut_IncorrectChoice),...
                              PunishOut,str(MatrixState.timeOut_IncorrectChoice)},...
    'OutputActions', [TimerTrig(TimerIDIncorrectTimeout) WaitForPokeOutStim]);
% This is a bit hacky, because we won't pass reward or ITI, TriggerITITimer
% will never be set, so as a result, when we reach ext_ITI,
% Condition(ConditionIDITI) will be True, so it will exit right away.
% In this way, the time spent inside the timeout_IncorrectChoice is both
% incorrect choice punishment + ITI 
sma = AddState(sma, 'Name',str(MatrixState.timeOut_IncorrectChoice),...
    'Timer',0,...
    'StateChangeConditions', {IfTimerIsOff(CondIDIncorrectTimeout),str(MatrixState.ext_ITI)},...
    'OutputActions', StopStim);
% We keep on sending softcode back to the computer because, at least on the
% emulator, sometimes when we send the soft-code, the bpod doesn't register it
% and we enter an infinite loop jumping betwee the next two states.
sma = AddState(sma, 'Name', str(MatrixState.timeOut_EarlyWithdrawal),...
    'Timer',LEDErrorRate,...
    'StateChangeConditions',{'SoftCode1',str(MatrixState.ITI),'Tup',str(MatrixState.timeOut_EarlyWithdrawalFlashOn)},...
    'OutputActions',[StopStim ErrorFeedback {'SoftCode',2}]);
sma = AddState(sma, 'Name', str(MatrixState.timeOut_EarlyWithdrawalFlashOn),...
    'Timer',LEDErrorRate,...
    'StateChangeConditions',{'SoftCode1',str(MatrixState.ITI),'Tup',str(MatrixState.timeOut_EarlyWithdrawal)},...
    'OutputActions',[StopStim ErrorFeedback,{'SoftCode',2,strcat('PWM',num2str(LeftPort)),LeftPWM,strcat('PWM',num2str(RightPort)),RightPWM}]);
sma = AddState(sma, 'Name', str(MatrixState.timeOut_SkippedFeedback),...
    'Timer',iff(~PCTimeout,TaskParameters.GUI.TimeOutSkippedFeedback,MinDur),...
    'StateChangeConditions',{'Tup',str(MatrixState.ITI)},...
    'OutputActions',[StopStim SkippedFeedbackSignal]); % TODO: See how to get around this if PCTimeout
sma = AddState(sma, 'Name', str(MatrixState.timeOut_missed_choice),...
    'Timer',iff(~PCTimeout,TaskParameters.GUI.TimeOutMissedChoice,MinDur),...
    'StateChangeConditions',{'Tup',str(MatrixState.ITI)},...
    'OutputActions',[StopStim ErrorFeedback]);
sma = AddState(sma, 'Name', str(MatrixState.ITI),...
    'Timer',WireTTLDuration,...
    'StateChangeConditions',{'Tup',str(MatrixState.ext_ITI)},...
    'OutputActions', [TimerTrig(TimerIDITI) StopStim AirFlowRewardOn]);
sma = AddState(sma, 'Name', str(MatrixState.ext_ITI),...
    'Timer',iff(~PCTimeout,TaskParameters.GUI.ITI,MinDur),...
    'StateChangeConditions',{'Tup','exit',...
                             IfTimerIsOff(ConditionIDITI),'exit'},...
    'OutputActions', [StopStim AirFlowRewardOn]);

% If Optogenetics/2-Photon is enabled for a particular state, then we
% modify that gien state such that it would send a signal to arduino with
% the required offset delay to trigger the optogentics box.
% Note: To precisely track your optogentics signal, split the arduino
% output to the optogentics box and feed it as an input to Bpod input TTL,
% e.g Wire1. This way, the optogentics signal gets written as part of your
% data file. Don't forget to activate that input in the Bpod main config.
if CurTrial.OptoEnabled
    % Convert seconds to millis as we will send ints to Arduino
    OptoDelay = uint32(TaskParameters.GUI.OptoStartDelay*1000);
    OptoDelay = typecast(OptoDelay, 'int8');
    OptoTime  = uint32(TaskParameters.GUI.OptoMaxTime*1000);
    OptoTime = typecast(OptoTime, 'int8');
    if ~BpodSystem.EmulatorMode || isfield(...
                                 BpodSystem.PluginSerialPorts,'OptoSerial')
        fwrite(BpodSystem.PluginSerialPorts.OptoSerial, OptoDelay, 'int8');
        fwrite(BpodSystem.PluginSerialPorts.OptoSerial, OptoTime, 'int8');
    end
    OptoStartTTLPin = 3;
    OptoStopTTLPin = 4;
    % Next few lines are adaped from EditState.m
    if BpodSystem.SystemSettings.IsVer2
        OutputChannelNames = BpodSystem.StateMachineInfo.OutputChannelNames;
        OptoStartEventIdx = ...
            strcmp(strcat('Wire', num2str(OptoStartTTLPin)), OutputChannelNames);
        OptoStopEventIdx = ...
             strcmp(strcat('Wire', num2str(OptoStopTTLPin)), OutputChannelNames);
        Tuple = {str(TaskParameters.GUI.OptoStartState1) OptoStartEventIdx;
                 str(TaskParameters.GUI.OptoEndState1)   OptoStopEventIdx;
                 str(TaskParameters.GUI.OptoEndState2)   OptoStopEventIdx;
                 str(MatrixState.ext_ITI)                OptoStopEventIdx};
        for i = 1:length(Tuple)
            StateName = Tuple{i, 1};
            EventCode = Tuple{i, 2};
            TrgtStateNum = strcmp(StateName, sma.StateNames);
            sma.OutputMatrix(TrgtStateNum, EventCode) = 1;
        end
    else
        OptoStartTTLPin = 2.^(OptoStartTTLPin-1);
        OptoStopTTLPin = 2.^(OptoStopTTLPin-1);
        Tuple = {str(TaskParameters.GUI.OptoStartState1) OptoStartTTLPin;
                 str(TaskParameters.GUI.OptoEndState1)   OptoStopTTLPin;
                 str(TaskParameters.GUI.OptoEndState2)   OptoStopTTLPin;
                 str(MatrixState.ext_ITI)                OptoStopTTLPin};
        EventCode = strcmp('WireState', BpodSystem.OutputActionNames);
        for i = 1:length(Tuple)
            StateName = Tuple{i, 1};
            TTLPin = Tuple{i, 2};
            TrgtStateNum = strcmp(StateName, sma.StateNames);
            OrigTTLVal = sma.OutputMatrix(TrgtStateNum, EventCode);
            sma.OutputMatrix(TrgtStateNum, EventCode) = bitor(OrigTTLVal,...
                                                              TTLPin);
        end
    end
end
end
