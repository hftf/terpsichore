#!/usr/bin/env python3

import argparse
import numpy as np
import numpy.fft as fft
import operator
import sys
import wave

import matplotlib.pyplot as plt

def fourier(wave, fr):
    return zip([x * fr for x in fft.fftfreq(len(wave)) if x > 0], np.absolute(fft.rfft(wave).real[1:]))

NOTES = ['a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#']

def freq2note(f):
    l = np.log(f / 440) / np.log(np.power(2, 1/12))
    n = np.int(np.round(l))
    note = NOTES[np.mod(n, 12)]
    octave = np.int(n / 12) + 4
    cents = np.round(100 * (l - n))
    return (note, octave, n)

class Transcriber:
    def __init__(self, framerate, add_note):
        self.framerate = framerate
        self.add_note = add_note
        self.buffer = np.array([], dtype=np.int16)

    def process(self, data):
        numpy.concatenate(self.buffer, data)

def note(n):
    print(n)

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
    framerate = wav.getframerate()
    data = np.fromstring(wav.readframes(wav.getnframes()), dtype=np.int16)
    wav.close()

    transcriber = Transcriber(framerate, note)
    transcriber.process(data)

"""
    samplesize = 4400
    samplestart = 0
    current = {}
    while samplestart + samplesize < len(data):
        sample = data[samplestart:samplestart+samplesize]
        f = sorted(fourier(sample, fr), key=operator.itemgetter(1), reverse=True)
        cs = [(freq2note(x[0]), x[1]) for x in f[:10] if x[1] > 10]
        cs = [x for x in cs if x[1] > cs[0][1] / 2]

        notes = [c[0] for c in cs]
        kill = []

        for note in current:
            if not note in notes:
                dur = current[note] * samplesize/2 / fr
                if dur > 0.8:
                    print('{} {}'.format(note, dur))
                kill.append(note)
        for k in kill:
            del(current[k])
        for note in notes:
            if note in current:
                current[note] = current[note] + 1
            else:
                current[note] = 1
        samplestart += samplesize/2
"""
"""
        f = list(fourier(sample, fr))
        plt.plot([x[0] for x in f], [x[1] for x in f])
        plt.xlim([0, 1000])
        plt.show()
        plt.cla()
        plt.clf()
        plt.close()
"""
"""
        ns = [n[2] for n in notes]
        for x in range(-30, 30):
            if x in ns:
                sys.stdout.write(NOTES[x%12][-1])
            else:
                sys.stdout.write(' ')
        sys.stdout.write('\n')
"""



"""
        f = list(fourier(sample, samplesize))
        plt.plot([x[0] for x in f], [x[1] for x in f])
        plt.xlim([0, 1200])
        #plt.show()
        """

