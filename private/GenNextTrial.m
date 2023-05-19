function [NextTrial, GUI, CurTimer] = GenNextTrial(NextTrial, NextTrialIdx,...
            GUI, PrimaryExpType, SecExpType, CurTimer, NextTrialBlockNum)
NextTrial.TrialNumber = NextTrialIdx;
% Tracks the amount of water the animal received up tp this point
% TODO: Check if RewardReceivedTotal is needed and calculate it using
% CalcRewObtained() function.
NextTrial.RewardReceivedTotal = 0; % We will updated later
NextTrial.RewardMagnitude = GUI.RewardAmount*[1,1];
NextTrial.CenterPortRewAmount = GUI.CenterPortRewAmount;
NextTrial.PreStimCntrReward = GUI.PreStimuDelayCntrReward;
% Block number assignment requires No computation, but centralizes all
% trial generation information in one place
NextTrial.BlockNum = NextTrialBlockNum;

tic;
% Secondary Experiment DV can be none or another value.
if NextTrial.SecExpIsUsed %rand() < GUI.SecExpUseProb
    [NextTrial, SecStimulusOmega] = GenSecExp(NextTrial, SecExpType,...
        GUI.SecExpStimIntensity, NextTrial.SecExpDirIsInversed, GUI.OmegaTable);
    if NextTrial.SecExpIsUsedAlone %rand() < GUI.SecExpProbUseAloneProb
        % DV will be set to NaN in the next step. Stimulus Omega will be
        % set below as appropriate
        PrimaryExpType = ExperimentType.NoStimulus;
        % Mark that in next trial that we were not using the original
        % MinSampling.
        if GUI.SecExpAloneMinSample
            GUI.PrimaryOriginalMinSample = GUI.MinSample;
            GUI.MinSample = GUI.SecExpAloneMinSample;
        else
            % Mark that we didn't change the original minimum sampling
            GUI.PrimaryOriginalMinSample = NaN;
        end
    end
else
    NextTrial.SecDV = NaN;
    % Mark that we didn't change the original minimum sampling
    GUI.PrimaryOriginalMinSample = NaN;
end
if PrimaryExpType == ExperimentType.NoStimulus
    NextTrial.StimulusOmega = round(NextTrial.StimulusOmega);
end
[NextTrial, DV] = CalcTrialDV(NextTrial, PrimaryExpType,...
                              NextTrial.StimulusOmega);
% cross-modality difficulty for plotting
%  0 <= (left - right) / (left + right) <= 1
NextTrial.DV = DV;
CurTimer.customSecDV = toc; tic;

% Set current stimulus for next trial
GUI.CurrentStim = StimDirStr(PrimaryExpType, NextTrial.DV, SecExpType,...
                             NextTrial.SecDV, NextTrial.LeftRewarded);
%determine if optogentics trial
OptoEnabled = rand(1,1) <  GUI.OptoProb;
if NextTrialIdx < GUI.StartEasyTrials
    OptoEnabled = false;
end
NextTrial.OptoEnabled = OptoEnabled;
GUI.IsOptoTrial = iff(OptoEnabled, 'true', 'false');

% Determine if Forced LED trial:
if GUI.PortLEDtoCueReward
    NextTrial.ForcedLEDTrial = rand(1,1) < GUI.PercentForcedLEDTrial;
else
    NextTrial.ForcedLEDTrial = false;
end
% Calculate RDK pulses. Ideally, I would calculate this in CalcDV() function,
% but I would have to pass a lot of GUI parameters to make this work.
RDKCohr = nan;
if PrimaryExpType == ExperimentType.RandomDots
    RDKCohr = abs(NextTrial.DV);
elseif ~isnan(NextTrial.SecDV) && SecExpType == ExperimentType.RandomDots
    RDKCohr = abs(NextTrial.SecDV);
end
if ~isnan(RDKCohr)
    % Create either a positive or negative pulse coherence
    if rand() >= 0.5 
      % pulseCohr is +ve, so make sure that we have enough coherence to add.
      PulseCohr = min(GUI.dotsPulseCohr/100, 1 -RDKCohr);
    else
      % pulseCohr is -ve, so make sure that we have enough coherence to
      % subtract.
      PulseCohr = max(GUI.dotsPulseCohr/-100, -RDKCohr);
    end
    % Now check if we should actually use the pulse coherence
    if rand() < GUI.dotsPulseProb && PulseCohr
        NextTrial.DotsPulseCoherence = PulseCohr;
        % For a pulse to start and finish, it borrows and lends coherences from
        % the other sides. For a coherence to start
        if GUI.dotsPulseOffset_Neg1Rnd == -1
            st = max(GUI.MinSample, GUI.StimulusTime);
            NextTrial.DotsPulseStart = rand() * (st - GUI.dotLifetimeSecs);
        else
            NextTrial.DotsPulseStart = GUI.dotsPulseOffset_Neg1Rnd;
        end
        NextTrial.DotsPulseDur = GUI.dotsPulseMinDur;
    else
        NextTrial.DotsPulseCoherence = nan; % It should be already nan by default
    end
end
if ~isnan(NextTrial.DotsPulseCoherence) && NextTrial.DotsPulseCoherence
    GUI.LastPulse = sprintf('P=%s%d%% S=%.2fsec T=%d',...
        iff(NextTrial.DotsPulseCoherence < 0, '-', '+'),...
            round(abs(NextTrial.DotsPulseCoherence*100)),...
            NextTrial.DotsPulseStart,...
        NextTrial.TrialNumber);
else
    GUI.LastPulse  = sprintf('Not Used - Trial Num=%d', NextTrial.TrialNumber);
end
CurTimer.customCatchNForceLed = toc;

end
