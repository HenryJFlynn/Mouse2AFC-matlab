from mmap import mmap
import time
import sys
import numpy as np

#from common.definitions import DrawStimType
from common.loadSerializedData import loadSerializedData


def closeEvent():
  sys.exit(0)


# def setup():
#   from common.createMMFile import createMMFile
#   FILE_SIZE = 512*1024 # 512 kb mem-mapped file
#   mm_file = createMMFile(r"c:\Bpoduser\mmap_matlab_audstim.dat", FILE_SIZE)
#   return mm_file

def main():
  import numpy as np
  from scipy.io import wavfile
  samplerate, data = wavfile.read("aud_samples/tone.wav")
  assert data.ndim == 2, f"Found {data.shape} channels rather than 2-channel "\
                          "stereo wave file"
  # Convert data to the format psychtoolbox expects
  data = data.astype(np.float64)
  data[:,0] /= -data[:,0].max()
  data[:,1] /= data[:,1].max()

  new_wav = np.zeros(data.shape, dtype=data.dtype)
  from psychtoolbox import audio
  stream = audio.Stream(freq=samplerate, channels=2)
  import time
  time.sleep(5)
  print("5 passed")
  stream.stop()
  time.sleep(4)
  # mm_file = setup()
  # 0 = Stop running
  # 1 = Load new stim info
  # 2 = Start running or keep running
  cur_cmd = 0
  while True:
    new_wav[:] = data[:] # Copy the data for the next trial
    while cur_cmd == 0:
      time.sleep(0.01) # Sleep until the next command
      # checkClose(wins_ptrs)
      cur_cmd = np.frombuffer(mm_file[:4], dtype=np.uint32)[0]
    # Load the the drawing parameters
    _, soundParams = loadSerializedData(mm_file, 4)
    # Modify the sound stimulus as needed
    DV = soundParams.DV
    if DV < 0: # Stimulus is to the left
      # Attenuate the right channel
      new_wav[:,1] *= (1-np.abs(DV))
    else:
      new_wav[:,0] *= (1-DV)
    stream.fill_buffer(data)

    timeout = time.time() + 3*60
    while cur_cmd == 1 and time.time() < timeout: # Wait for the run command
      time.sleep(0.002)
      cur_cmd = np.frombuffer(mm_file[:4], dtype=np.uint32)[0]

    if cur_cmd == 2:
      stream.start(repetitions=0)
      timeout = time.time() + 3*60
      while cur_cmd == 2 and time.time() < timeout:
        cur_cmd = np.frombuffer(mm_file[:4], dtype=np.uint32)[0]
      stream.stop()

if __name__ == "__main__":
  main()



'''Tests
#%%
import numpy as np
dvs = [-1, -0.6, -0.2, 0, 0.2, 0.4, 0.6, 1]
for dv in dvs:
  print("DV:", dv, "has", (1-np.abs(dv))*100, "on the other side")
#%%
'''