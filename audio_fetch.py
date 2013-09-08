#!/usr/bin/env python3

import sys
import terpsichore
from terpsichore import handle_note
import wave
import numpy as np
from StringIO import StringIO

class TerpsWrap():
    def __init__(self, f):
        self.f = StringIO(f)
        self.wave = wave.open(self.f)
        self.notes = []
        self.parse()

    def parse(self):
        if self.wave.getnchannels() != 1:
            print("Too many channels! ", self.wave.getnchannels())
            sys.exit(1)
        if self.wave.getsampwidth() != 2:
            print("Bad sample width! ", self.wave.getsampwidth())
            sys.exit(1)
        self.framerate = self.wave.getframerate()
        self.data = np.fromstring(self.wave.readframes(self.wave.getnframes()), dtype=np.int16)
        self.wave.close()
 
        self.transcriber = terpsichore.Transcriber(self.framerate, self.add_note)
        self.transcriber.process(self.data)

    def add_note(self, n, start, dur):
        (note, octave, off) = n
        self.notes.append('{} ([]) from {} for {}s'.format(note, octave, start, dur))
