#!/usr/bin/env python3

import terpsichore

class UploadFile():
	def __init__(self, file=None):
		self.file = file
		try:
			self.wave = wave.open(self.file)
		except:
			raise Exception("could not read a wave file")
		if self.file != None:
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
 
		self.transcriber = Transcriber(self.framerate, handle_note)
		self.transcriber.process(self.data)
