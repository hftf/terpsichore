#!/usr/bin/env python2

import argparse
import numpy as np
import numpy.fft as fft
import operator
import signals as sig
import sys
import wave

def fourier(wave, fr):
    return zip([x * fr for x in fft.fftfreq(len(wave)) if x > 0], np.absolute(fft.rfft(wave).real[1:]))

NOTES = ['a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#']

FREQS = [440 * np.power(2, x/12.) for x in range(-24, 14)]

def freq2note(f):
    l = np.log(f / 440.) / np.log(np.power(2, 1/12.))
    n = np.int(np.round(l))
    note = NOTES[np.mod(n, 12)]
    octave = np.int(np.floor((n + 9) / 12. + 4))
    cents = np.round(100 * (l - n))
    return (note, octave, n)

SAMPLESIZE = 2200

def handle_note(n, start, dur):
    (note, octave, off) = n
    print('{} ({}) from {} for {}s'.format(note, octave, start, dur))

class Transcriber:
    def __init__(self, framerate, add_note):
        self.framerate = framerate
        self.add_note = add_note
        self.buffer = np.array([], dtype=np.int16)
        self.samplestart = 0
        self.playing = {}
        self.current = {}

    def process(self, data):
        np.concatenate((self.buffer, data))
        while self.samplestart + SAMPLESIZE < len(data):
            sample = data[self.samplestart:self.samplestart+SAMPLESIZE]

            spectrum = []
            for f in FREQS:
                fr = f * 2 * np.pi / self.framerate
                cs = sample * np.cos(np.arange(len(sample)) * fr)
                ss = sample * np.sin(np.arange(len(sample)) * fr)
                spectrum.append((f,np.power(np.sum(cs), 2) + np.power(np.sum(ss), 2)))
            spectrum = sorted(spectrum, key=operator.itemgetter(1), reverse=True)
            strong = [s[0] for s in spectrum if s[1] > spectrum[0][1]/16]

            """
            freqs = np.array([x * self.framerate
                              for x in fft.fftfreq(len(sample)) if x > 0])
            spectrum = np.absolute(fft.rfft(sample).real[1:])

            maxes = sig.argrelmax(spectrum, order=4, axis=0)[0]
            maxes = sorted(maxes, key=lambda i:spectrum[i], reverse=True)
            top = [m for m in maxes if spectrum[m] > spectrum[maxes][0]/2.]

            notes = [freq2note(freqs[i]) for i in top]
            extra = [freq2note(freqs[i]) for i in maxes]
            """

            top = [s[0] for s in spectrum if s[1] > spectrum[0][1]/4]
            notes = [freq2note(s) for s in top[:1]]
            extra = notes

            kill = [] # List of notes to forget permanently

            # Kill off harmonics (will harm chords)

            for note in self.playing:
                if not note in extra:
                    if self.playing[note]['end'] is None:
                        self.playing[note]['end'] = self.samplestart
                    end = self.playing[note]['end']
                    if end - self.playing[note]['start'] < SAMPLESIZE * 4:
                        kill.append(note)
                    elif self.samplestart - end > SAMPLESIZE:
                        dur = float(self.playing[note]['end'] - self.playing[note]['start'])/framerate
                        self.add_note(note, self.samplestart / float(self.framerate) - dur, dur)
                        kill.append(note)

            for k in kill:
                del(self.playing[k])

            for note in set(notes):
                if note in self.playing:
                    pass
                else:
                    self.playing[note] = { 'start': self.samplestart,
                                           'end': None}
            
            # Advance
            self.samplestart += SAMPLESIZE/2

"""
            # Send and kill ended notes
            kill = []
            for note in self.current:
                if not note in notes:
                    dur = self.current[note] / self.framerate
                    if dur > 0.05:
                        self.add_note(note, self.samplestart / float(self.framerate) - dur, dur)
                    kill.append(note)
            for k in kill:
                del(self.current[k])

            # Register new notes
            for note in set(notes):
                if note in self.current:
                    self.current[note] += SAMPLESIZE/2.
                else:
                    self.current[note] = 0.
                    """


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

    transcriber = Transcriber(framerate, handle_note)
    transcriber.process(data)
