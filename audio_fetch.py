#!/usr/bin/env python3

import sys

class UploadFile():
	def __init__(self, file=None):
		self.file = file
		if self.file != None:
			self.parse()
