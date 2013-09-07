#!/usr/bin/env python3

import argparse
import numpy as np
import numpy.fft as fft
import operator
import sys
import wave

import matplotlib.pyplot as plt

def fourier(wave):
    return zip([x for x in fft.fftfreq(len(wave)) if x >= 0], np.absolute(fft.rfft(wave).real))

#x = [np.sin(x * np.pi / 4) for x in np.arange(1,1000)]

#http://docs.python.org/3.1/library/wave.html

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('wav', type=str, help='audio file')
    args = parser.parse_args()

    # Read the WAV file
    wav = wave.open(args.wav)
    if wav.getnchannels() != 1:
        print("Too many channels!")
        sys.exit(1)
    if wav.getsampwidth() != 2:
        print("Bad sample width!")
        sys.exit(1)
    fr = wav.getframerate()
    data = np.fromstring(wav.readframes(10000), dtype=np.int16)
    wav.close()

    #print(wav.readframes(40000))

    f = sorted(fourier(data), key=operator.itemgetter(1), reverse=True)
    print([x[0] * 40000 for x in f][:80])

"""
    SAMPLE_RATE = 44100
    data = np.sin(5000 * 2 * np.pi * np.arange(40000) / 40001)

    f = list(fourier(data))
    plt.plot([x[0] for x in f], [x[1] for x in f])
    plt.show()
    f = sorted(fourier(data), key=operator.itemgetter(1), reverse=True)
    print([x[0] * 40000 for x in f][:80])
    """
