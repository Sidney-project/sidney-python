#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thibaultneveu
# @Date:   2015-10-12 18:16:40
# @Last Modified by:   thibaultneveu
# @Last Modified time: 2015-10-15 23:35:07
s
import angus.cloud
import os
import sys
import threading
import subprocess
from random import randint
import time
import glob
import json
from socketIO_client import SocketIO, LoggingNamespace

class SidneyEyes():

	def __init__(self):
		self.conn = angus.connect()
		self.face_recognition = self.conn.services.get_service('face_recognition', version=1)
		self.people_list = {}
		self.set_people_list()
		self.search_in_load = -1
		print "__INIT__"
		self.socketIO = SocketIO('192.168.0.15', 3000, LoggingNamespace)
		self.socketIO.emit('aaa')
		self.socketIO.wait()

	def set_search_in_load(self, value):
		self.search_in_load = value

	def set_people_list(self):
		print "__SET PEOPLE LIST__"
		list_people = os.listdir('faces')
		for p in list_people:
			print "data receive for %s" %p
			list_faces = glob.glob("./faces/%s/*.jpeg" %p)
			self.people_list[p] = []
			for f in list_faces:
				self.people_list[p].append(self.conn.blobs.create(open(f)))		

	def set_interval(self, func, sec):
		def func_wrapper():
			set_interval(func, sec)
			func()
		t = threading.Timer(sec, func_wrapper)
		t.start()
		return t

	def simple_capture(self):
		number_id = randint(0,10000)
		capture_name = time.strftime("%d-%m-%Y-%H-%M-%S") + "_" + str(number_id) + ".jpeg"
		os.system("streamer -f jpeg -s 1000 -o /home/pi/sidney-python/cap/%s" %capture_name)
		return ("/home/pi/sidney-python/cap/%s" %capture_name)

	def _analyse_time(self, capture, callback):
		print "__new thread to analyse captue__"
		try:
			job = self.face_recognition.process({'image': open(capture), "album" : self.people_list})
			callback(json.dumps(job.result, indent=4))
		except Exception as e:
			print "Request fail"
			callback(None)

	def analyse(self, capture, callback):
		t = threading.Timer(3, self._analyse_time, [capture, callback])
		t.start()

	def _learn_faces_thread(self, name):
		t = 1
		os.system("streamer -f jpeg -s 1000 -o /home/pi/sidney-python/faces/%s/faces_1.jpeg" %name)
		time.sleep(t)
		os.system("streamer -f jpeg -s 1000 -o /home/pi/sidney-python/faces/%s/faces_2.jpeg" %name)
		time.sleep(t)
		os.system("streamer -f jpeg -s 1000 -o /home/pi/sidney-python/faces/%s/faces_3.jpeg" %name)
		time.sleep(t)
		os.system("streamer -f jpeg -s 1000 -o /home/pi/sidney-python/faces/%s/faces_4.jpeg" %name)
		time.sleep(t)
		os.system("streamer -f jpeg -s 1000 -o /home/pi/sidney-python/faces/%s/faces_5.jpeg" %name)
		self.set_people_list()

	def learn_faces(self, name):
		t = threading.Timer(1, self._learn_faces_thread, [name])
		t.start()

	def _search_faces_know_thread(self):
		print "__SEARCHING FOR FACES___"
		capture = sidney.simple_capture()
		name = self.analyse(capture, analyse_done)
		print name

	def search_faces_know(self):
		self.search_in_load = self.search_in_load + 1
		def func_wrapper():
			self._search_faces_know_thread()
			self.search_faces_know()
		t = threading.Timer(1, func_wrapper)
		if self.search_in_load > 15:
			self.search_in_load = -1
			return None
		else:
			t.start()
		return t

def analyse_done(data):
	if data is None:
		print "Unknow this faces -> Request Fail"
		return None
	try:
		data = json.loads(data)
		rel_name = ""
		rel_confidence = 0
		for dt in data["faces"]:
			for name in dt["names"]:
				if float(name["confidence"]) > rel_confidence and float(name["confidence"]) > 0.5:
					rel_confidence = float(name["confidence"])
					rel_name = name["key"]
		if name == "":
			print "Unknow this faces -> bad confidence" 
			return None
		else:
			print rel_name
			print rel_confidence
			return rel_name
	except Exception as e:
		print "Error to catch faces, error : %s" %e
		return None

if __name__ == "__main__":
	sidney = SidneyEyes()
	if len(sys.argv) == 2:
		sidney._learn_faces_thread(sys.argv[1])
	else:
		print "lol"
		#sidney.search_faces_know()




















