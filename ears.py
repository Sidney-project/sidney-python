#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thibaultneveu
# @Date:   2015-10-15 19:10:11
# @Last Modified by:   thibaultneveu
# @Last Modified time: 2015-10-16 22:45:34

import wit
import json
import threading
from socketIO_client import SocketIO, LoggingNamespace

class SidneyEars():

	def __init__(self):
		self.wit = wit
		print "__INIT__"
		self.socketIO = SocketIO('192.168.0.15', 3000, LoggingNamespace)
		self.socketIO.on('services/ears/listen_for_ever', self.event_listen_for_ever)
		self.socketIO.wait()

	def event_listen_for_ever(self, *args):
		args = list(args)
		list_intent = []
		for el in args:
			list_intent.append(str(el))
		output = self.listen(list_intent[0])
		print output
		if output is not None:
			#self.socketIO.emit("services/ears/listen_for_ever_response", {"status" : 200})
			return output
		else:
			return self.listen(args)

	def listen(self, intent):
		self.wit.init()
		access_token = 'QCIHICB6WJ2O4A6FO6VSA4ZDG6L6ANPB'
		output = None
		response = self.wit.voice_query_auto(access_token)
		response = json.loads(response)
		try:
			for el in response["outcomes"]:
				print "ANALYSE"
				print el["confidence"]
				print el["intent"]
				print "END ANALYSE"
				print intent
				if el["intent"] in intent:
					print "IS INSIDE"
				if el["confidence"] > 0.2 and el["intent"] in intent:
					print "TOUT EST BON VALEUR SETTER"
					output = el["intent"]
		except Exception as e:
			print e
		self.wit.close()
		return output

if __name__ == "__main__":
	sidney_ear = SidneyEars()
	#sidney_ear.event_listen_for_ever(["hello", "turn_on_light"])












