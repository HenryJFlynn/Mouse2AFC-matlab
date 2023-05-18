function [TrialsArr, TaskParamsGUIArr, TimersArr] = ...
                    CreateOrAppendDataArray_PredErr(NUM_TRIALS, TaskParameters_GUI)

SingleTrial = struct(...
...%% Standard values
...% Stores which lateral port the animal poked into (if any)
   'ChoiceLeft', NaN,...
...% Stores whether the animal poked into the correct port (if any)
   'ChoiceCorrect', NaN,...
...% Signals whether confidence was used in this trial. Set to false if
...% lateral ports choice timed-out (i.e, MissedChoice(i) is true), it also
...% should be set to false (but not due to a bug) if the animal poked the
...% a lateral port but didn't complete the feedback period (even with
...% using grace).
   'Feedback', true,...
...% How long the animal spent waiting for the reward (whether in correct
...% or in incorrect ports)
   'FeedbackTime', NaN,...
...% Signals whether the animal broke fixation during stimulus delay state
   'FixBroke', false,...
...% How long the animal remained fixated in center poke
   'FixDur', NaN,...
...% Signals whether the animal broke fixation during sampling but before
...% min-sampling ends
   'EarlyWithdrawal', false,...
   'MinSample', false,...
...% Signals whether the animal correctly finished min-sampling but failed
...% to poke any of the lateral ports within ChoiceDeadLine period
   'MissedChoice', false,...
...% How long between sample end and making a choice (timeout-choice trials
...% are excluded)
   'MT', NaN,...
...% How long the animal sampled. If RewardAfterMinSampling is enabled and
...% animal completed min sampling, then it's equal to MinSample time,
...% otherwise it's how long the animal remained fixated in center-port until
...% it either poked-out or the max allowed sampling time was reached.
   'ST', NaN,...
   'ReactionTime', NaN,...
   'StimulusOmega', NaN,...
   'DV', NaN,...
   'SecDV', NaN,...
   'SecExpIsUsed', NaN,...
   'SecExpIsUsedAlone', NaN,...
   'SecExpDirIsInversed', NaN,...
   'BlockId', NaN,...
...% Signals whether a reward was given to the animal (it also includes if
...% the animal poked into the correct reward port but poked out afterwards
...% and didn't receive a reward, due to 'RewardGrace' being counted as
...% reward).
   'Rewarded', false,...
   'LeftRewarded', NaN,...
...% Signals whether a center-port reward was given after min-sampling ends.
   'RewardAfterMinSampling', false,...
   'CatchTrial', false,...
   'OptoEnabled', false,...
   'LeftClickTrain', NaN,...
   'RightClickTrain', NaN,...
   'PreStimCntrReward', 0,...
   'LightIntensityLeft', NaN,...
   'LightIntensityRight', NaN,...
   'SoundIntensityLeft', NaN,...
   'SoundIntensityRight', NaN,...
   'DotsCoherence', NaN,...
...% RDK Pulses
   'DotsPulseCoherence', NaN,...
   'DotsPulseStart', NaN,...
   'DotsPulseDur', NaN,...
   'GratingOrientation', NaN,...
...% RewardMagnitude is an array of length 2
...% TODO: Use an array of 1 and just assign it to the rewarding port
   'RewardMagnitudeCorrect', TaskParameters_GUI.RewardAmountCorrect*[1,1],... 
   'RewardMagnitudeInCorrect', TaskParameters_GUI.RewardAmountInCorrect*[1,1],... 
   'CenterPortRewAmount', TaskParameters_GUI.CenterPortRewAmount,... % TaskParameters.GUI.CenterPortRewAmount;
...% Tracks the amount of water the animal received up tp this point
...% TODO: Check if RewardReceivedTotal is needed and calculate it using
...% CalcRewObtained() function.
   'RewardReceivedTotal', 0,...
   'TrialNumber', NaN,...
   'ForcedLEDTrial', false,...
...%% Exists also in GUI:
   'StimDelay', NaN,...
   'FeedbackDelay', NaN,...
   'RewardDelay', NaN,...
   'TrialStartSysTime', NaN,...
...%% For block-based experiments
   'BlockNum', NaN);

SingleTimer = struct(...
   'AppendData', NaN,...
   'BuildStateMatrix', NaN,...
   'calculateTimeout', NaN,...
   'customAdjustBias', NaN,...
   'customCalcBias', NaN,...
   'customCalcOmega', NaN,...
   'customCatchNForceLed', NaN,...
   'customExtractData', NaN,...
   'customFeedbackDelay', NaN,...
   'customFinializeUpdate', NaN,...
   'customGenNewTrials', NaN,...
   'customInitialize', NaN,...
   'customMinSampling', NaN,...
   'customPerfStrGen', NaN,...
   'customPrepNewTrials', NaN,...
   'customSecDV', NaN,...
   'customSendPhp', NaN,...
   'customStimDelay', NaN,...
   'HandlePause', NaN,...
   'SaveData', NaN,...
   'sendPlotData', NaN,...
   'SendStateMatrix', NaN,...
   'startNewIter', 0.0,...
   'SyncGUI', NaN,...
   'updateCustomDataFields', NaN,...
   'TrialTotalTime', NaN);

TrialsArr = repmat(SingleTrial, 1, NUM_TRIALS);
TimersArr = repmat(SingleTimer, 1, NUM_TRIALS);
TaskParamsGUIArr = repmat(TaskParameters_GUI, 1, NUM_TRIALS);
end
