# PC Configuration for Experimental Mouse2AFC Bpod Protocol
### Written for [Poirazi Lab](https://dendrites.gr/)
### See [HERE](https://sites.google.com/site/bpoddocumentation/home?authuser=0) for me info on the Bpod

## Workspace Enviroment Setup
1. MATLAB 2018a (or newer)
2. Install psychtoolbox library 
     - For Windows
       -  Go to http://psychtoolbox.org/download#Windows (they have detailed instructions)
       -  You download Psychtoolbox installer as written in Psychtoolbox-3; step 2
       -  Create a folder “toolbox” under `C:\`  and extract `DownloadPsychtoolbox.m` zip folder here (you should end up with `C:\toolbox\DownloadPsychtoolbox.m`)
       -  Download gStreamer as written in Psychtoolbox-3; step 3
       -  Download TortoiseSVN from here
       -  Run MATLAB as Administrator (you can go to `C:\Program Files\MATLAB\R2018a\bin` and right click to `matlab.exe` file
       -  In MATLAB command line:
            ```MATLAB
            >> cd('C:\toolbox\')
            >> DownloadPsychtoolbox('C:\toolbox')
            ```
          - A folder `Psychtoolbox` will be created under `C:\toolbox\`
      - For linux
        -  Go to http://psychtoolbox.org/download.html#Linux
        -  Their instructions should be enough
3. Install python (Suggested version == 3.7)
     - verify installation before proceeding
4. Install pip (https://phoenixnap.com/kb/install-pip-windows) (steps 1-3)
5. Copy and paste in command prompt to install the necesary libraries: 
```bash
pip install numpy scipy matplotlib pandas scikit-learn statsmodels colour click
```
6. If you'll do random dots experiments, then you'll need Psychopy as well
```bash
pip install Psychopy
```
8. Download/unzip the Bpod software (from wetlab drive: `software/Bpod_Gen2_live.zip`) under `C:`
9. Download/unzip the Bpod protocols/files (from wetlab drive: `software/BpodUser`) under `C:`
    - Replace the files in `BpodUser/Protocols/Mouse2AFC` with the files from this repo
    - This repo will have a more up to date version than the one in the `C:` drive
    - As of writing this the most up to date version is named `Mouse2AFC_2023_01_13`

10. Install [Arduino software](https://www.arduino.cc/en/software) for your OS

## MATLAB Configuration
Then open MATLAB → go to SetPath (in the environment panel)→ 
1. Import all files from `Bpod_Gen2_live`: click to add with subfolders and chose the `Bpod_Gen2_live` folder and `SAVE`
2. Import all files from toolbox (Psychtoolbox): click to add with subfolders and chose the `Psychtoolbox` folder and `SAVE`
       - NOTE: Move the folder `C:\toolbox\Psychtoolbox\PsychBasic\MatlabWindowsFilesR2007a\` before (up) the folder `C:\toolbox\Psychtoolbox\PsychBasic\`  and `SAVE`.
3. Import all files from `BpodUser/Protocols/Mouse2AFC/Definitions` folder and `SAVE`
     - As state previously, right now `Mouse2AFC` is named `Mouse2AFC_2023_01_13`
4. Import all files from `BpodUser/Settings_Bpod2` folder and `SAVE`
5. import all files from the `MATLAB` folder in this repo and `SAVE`

## Arduino Congifuration
Open Arduino software and 
1. Connect Arduino to PC using the programming port (not native port)
     - Use the programming port to upload to the arduino and native port when running Bpod
2. Go to tools --> board --> board manager and search `arduino due`
3. Select `Arduino Sam Boards(32-bits ARM Cortex-M3)` and install the package
4. Upload the files found [here](https://github.com/sanworks/Bpod_StateMachine_Firmware/tree/v22/Preconfigured/StateMachine-Bpod0_5) to the arduino

## Run Bpod in Matlab
1. Connect arduino to PC using the native port
2. Open MATLAB
3. Open arduino software
4. In tools, under Boards select the Native Port and under Port select the port (i.e. 'COM4' for Windows)
![image](https://github.com/HenryJFlynn/Mouse2AFC-matlab/assets/130571023/4288a586-ade8-4877-ba82-81358df4fa9f)

5. In MATLAB command line:
```MATLAB
Bpod('COM4')
```
To start Bpod



#### Required Changes For Linux Users
1. Mouse2AFC: Line 63
```MATLAB
createMMFile('c:\Bpoduser\', 'mmap_matlab_randomdot.dat', file_size);
```
Change `c:\Bpoduser\` to reflect your system path to `mmap_matlab_randomdot.dat`

2. BpodObject: Line 116

```MATLAB 
 obj.Path.LocalDir = 'C:\BpodUser'; %fullfile(obj.Path.ParentDir, 'BpodUser');
```
Delete `C:\BpodUser' and uncomment the rest of the line
 
  
#### These instructions are a revised version of the ones found here: https://github.com/HenryJFlynn/mouse2afc/issues/5
#### For any problems, first see https://github.com/HenryJFlynn/mouse2afc/issues/2 
