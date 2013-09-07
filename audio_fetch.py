#!/usr/bin/env python3

import sys
import terpsichore
import wave
import numpy as np
from StringIO import StringIO

class UploadFile():
	def __init__(self, f):
		self.f = StringIO(f)
                self.wave = wave.open(self.f)
                self.parse()

	def parse(self):
 		if self.wave.getnchannels() != 1:
 			print("Too many channels!")
 			sys.exit(1)
		if self.wave.getsampwidth() != 2:
			print("Bad sample width!")
			sys.exit(1)
		self.framerate = self.wave.getframerate()
		self.data = np.fromstring(self.wave.readframes(self.wave.getnframes()), dtype=np.int16)
		self.wave.close()
 
		self.transcriber = terpsichore.Transcriber(self.framerate, handle_note)
		self.transcriber.process(self.data)
