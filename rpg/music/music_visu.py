import matplotlib.pyplot as plt
import numpy as np
import wave

file = './music/pip_song.wav'

with wave.open(file,'r') as wav_file:
    fs = wav_file.getframerate()
    data = np.frombuffer(wav_file.readframes(-1), dtype=np.int16)
    left, right = data[0::2], data[1::2]


    Time_left=np.linspace(0, len(left)/fs, num=len(left))
    Time_right=np.linspace(0, len(right)/fs, num=len(right))

    plt.figure(1)
    plt.plot(Time_left,left)
    plt.plot(Time_right,right)

    plt.show()