#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thibaultneveu
# @Date:   2015-10-15 19:10:11
# @Last Modified by:   thibaultneveu
# @Last Modified time: 2015-10-15 22:16:47

import wit
import json
import threading

class SidneyEar():

	def __init__(self):
		self.wit = wit

	def listen(self, intent):
		self.wit.init()
		access_token = 'QCIHICB6WJ2O4A6FO6VSA4ZDG6L6ANPB'
		output = None
		response = self.wit.voice_query_auto(access_token)
		response = json.loads(response)
		try:
			for el in response["outcomes"]:
				if el["confidence"] > 0.3 and el["intent"] in intent:
					output = el["intent"]
		except Exception as e:
			print e
		self.wit.close()
		return output

	def listen_for_ever(self, intent):
		output = self.listen(intent)
		if output in intent:
			return output
		else:
			return self.listen(intent)

if __name__ == "__main__":
	sidney_ear = SidneyEar()
	print sidney_ear.listen_for_ever(["hello", "turn_on_light"])