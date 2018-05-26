import sys
import matplotlib.pyplot as plot
from scipy.io import wavfile
import peakdetect

def flatten(input):
    new_list = []
    for i in input:
        for j in i:
            new_list.append(j)
    return new_list

samplingFrequency, signalData = wavfile.read('twinkle.wav')
plot.title('Spectrogram')
spectrum, freqs, t, im = plot.specgram(signalData[:, 0],Fs=samplingFrequency)
print(freqs)
#_max, _min = peakdetect.peakdetect(spectrum, lookahead=300, delta=0.3)
#print(_max)
plot.xlabel('Time')
plot.ylabel('Frequency')
#plot.show()
