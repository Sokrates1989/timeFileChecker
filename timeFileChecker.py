## Client that sends status messages to statechecker server.
## Use object.start() to call run method .

# Make this client work on its own Thread.
from threading import Thread
# To make Thread sleep.
import time
# For making POST / GET requests.
import requests
# For file operations with operating system.
import os
# For getting config.
import json
# For detecting, if config is array.
import collections.abc

# Own modules import.
import sys
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "utils"))


# For creating files.
import fileUtils

# Get config.
config_file_pathAndName = os.path.join(os.path.dirname(__file__), "config.txt")
config_file = open(config_file_pathAndName)
config_array = json.load(config_file)

class TimeFileChecker(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.daemon = True
		self.running = True
		
		# Create timeFile.
		self.timefile = os.path.join(os.path.dirname(__file__), "timefile.txt")
		fileUtils.createFileIfNotExists(self.timefile)

		# Ensure state is sent often enough and amount minutes is positive.
		writeTimeFileEveryXSeconds = int(os.getenv('writeTimeFileEveryXSeconds', config_array["writeTimeFileEveryXSeconds"]))
		if not writeTimeFileEveryXSeconds:
			writeTimeFileEveryXSeconds = 60
		if writeTimeFileEveryXSeconds < 1:
			writeTimeFileEveryXSeconds = 1
		self.writeTimeFileEveryXSeconds = writeTimeFileEveryXSeconds 


	def run(self):
		while self.running:
			self.writeCurrentTimeToFile()
			time.sleep(self.writeTimeFileEveryXSeconds)

	def stop(self):
		self.running = False


	def writeCurrentTimeToFile(self):
		# Get the current time in seconds since the epoch
		current_time = time.time()

		# Write the current time to the file (overwrite)
		with open(self.timefile, "w") as file:
			file.write(str(current_time))

