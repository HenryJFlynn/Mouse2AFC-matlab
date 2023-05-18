% Clear the workspace and the screen

% Setup PTB with some default values
PsychDefaultSetup(2);


% Set the screen number to the external secondary monitor if there is one
% connected
screenNumber = max(Screen('Screens'));

% Define black, white and grey
white = WhiteIndex(screenNumber);
grey = white / 2;

% Skip sync tests for demo purposes only
Screen('Preference', 'SkipSyncTests', 1);

% Open the screen
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, 0, [], 32, 2,...
    [], [],  kPsychNeed32BPCFloat);

screenDistCm = 12;
screenWidthCm = 20;

% TODO: Remove kbcheck from the DrawDots() function
dotsParams.mainDirection = 270;  %degrees (clockwise from straight up) for the main stimulus
dotsParams.coherence = 0.9; % The ratio of total dots that will match the main direction
dotsParams.apertureSize = [110, 90]; % size of rectangular aperture [w,h] in degrees
% Use 20% of the screen size
circleArea = (pi*((dotsParams.apertureSize(1)/2).^2)); % assume apertureSize is the diameter
dotsParams.nDots = round(circleArea * 0.05);
%dotsParams.nDots = 300;     % total number of dots
dotsParams.color = [255,255,255];  % color of the dots
dotsParams.size = 2;              % size of dots in degrees
dotsParams.center = [0,0];         % center of the field of dots (x,y)
dotsParams.speed = 25;      %degrees/second
dotsParams.duration = 20;  %seconds
dotsParams.lifetime = 1;  %lifetime of each dot sec

DrawDots(window, windowRect, screenDistCm, screenWidthCm, dotsParams);

Screen('CloseAll');