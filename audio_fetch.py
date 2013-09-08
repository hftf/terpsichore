#!/usr/bin/env python3

import sys
import terpsichore
from terpsichore import handle_note
import wave
import numpy as np
from StringIO import StringIO
import unicodedata

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
 
        self.transcriber = terpsichore.Transcriber(self.framerate, self.note_adder)
        self.transcriber.process(self.data)

    def note_adder(self, token, n, start, length):
        return lambda n, start, length, _: notes[token].append((n, start, length))
