# Mouse2AFC MATLAB Bpod Protocol
## Written for Poirazi Lab: https://dendrites.gr/
## See here for me info on the Bpod: https://sites.google.com/site/bpoddocumentation/home?authuser=0

### Workspace Enviroment Setup

What we need to set up in the PC for a functional behavioral Bpod system:
1. Matlab 2018a (or newer)
2. Install psychtoolbox library 
     - For Windows
       -  Go to http://psychtoolbox.org/download#Windows (they have detailed instructions)
       -  You download Psychtoolbox installer as written in Psychtoolbox-3; step 2
       -  Create a folder “toolbox” under `C:\`  and extract `DownloadPsychtoolbox.m` zip folder here (you should end up with `C:\toolbox\DownloadPsychtoolbox.m`)
       -  Download gStreamer as written in Psychtoolbox-3; step 3
       -  Download TortoiseSVN from here
       -  Run Matlab as Administrator (you can go to `C:\Program Files\MATLAB\R2018a\bin` and right click to `matlab.exe` file
       -  In matlab you code the following:
            ```MATLAB
            >> cd('C:\toolbox\')
            >> DownloadPsychtoolbox('C:\toolbox')
            ```
        - A folder Psychtoolbox will be created under C:\toolbox\.
      - For linux
        -  Go to http://psychtoolbox.org/download.html#Linux
        -  Their instructions should be enough
3. Install python (I use python 3.7, I think newer ones should work without a problem but I haven't tested) 
4. Install pip (https://phoenixnap.com/kb/install-pip-windows)
5. Copy and paste to install the necesary libraries: 
```python
pip install numpy scipy matplotlib pandas scikit-learn statsmodels colour click
```
6. If you'll do RDK, then you'll need Psychopy as well
```python
pip install Psychopy
```
8. Download the Bpod software (from wetlab drive: `software/Bpod_Gen2_live.zip`) under `C:`
9. Download the Bpod protocols/files (from wetlab drive: `software/BpodUser`) under `C:`
    - Replace the files in `BpodUser/Protocols/Mouse2AFC` with the files from this repo
    - This repo will have a more up to date version than the one in the `C:` drive

10. Install Arduino software (https://www.arduino.cc/en/software)

Then open matlab → go to SetPath (in the environment panel)→ 
1. import all files from `Bpod_Gen2_live`: click to add with subfolders and chose the `Bpod_Gen2_live` folder and SAVE
2. import all files from toolbox (Psychtoolbox): click to add with subfolders and chose the `Psychtoolbox` folder and SAVE
3. import all files from `BpodUser/Protocols/Mouse2AFC/Definitions` folder and SAVE
4. import all files from `BpodUser/Settings_Bpod2` folder and SAVE
5. import all files from the `MATLAB` folder in this repo 

Open Arduino software and upload the files from here: https://github.com/sanworks/Bpod_StateMachine_Firmware/tree/v22/Preconfigured/StateMachine-Bpod0_5

#### These instructions are a revised version of the ones found here: https://github.com/HenryJFlynn/mouse2afc/issues/5
#### For any problem see https://github.com/HenryJFlynn/mouse2afc/issues/2 
