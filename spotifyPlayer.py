import sys
import os
import signal
import time
import pprint
import json
import urllib.request
import pygame
import pathlib
import threading

from pygame import mixer
from pathlib import Path
from collections import deque

import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

class SpotifyPlayer:
	def __init__(self, spotify_client_id, spotify_client_secret):

		self.currSongID = 1
		self.queue = []
		self.mixer = mixer.init()

		self.currFileName = ""
		self.tempDir = "mp3FilesTemp"
		if not os.path.exists(self.tempDir):
			os.makedirs(self.tempDir)

		credentials = oauth2.SpotifyClientCredentials(
			client_id=spotify_client_id,
			client_secret=spotify_client_secret)

		token = credentials.get_access_token()
		if not token:
			print("Could not get token")
			sys.exit()

		self.sp = spotipy.Spotify(auth=token)


	def __del__(self):
		if (Path(self.currFileName).is_file()):
			os.remove(self.currFileName)
		os.rmdir(self.tempDir)


	def __search_track(self, name="", artist="", inputLimit=1):
		numQueued = 0
		searchQuery = name + " " + artist
		result = self.sp.search(searchQuery, limit=inputLimit, type="track", market="US")
		for x in range(inputLimit):
			preview_url = result["tracks"]["items"][x]["preview_url"]
			if (preview_url != None):
				self.queue.insert(0, preview_url)
				numQueued += 1
		return numQueued


	def __download_mp3(self, url):
		self.currFileName = "./" + self.tempDir + "/spotifyTemp" + str(self.currSongID) + ".mp3"
		urllib.request.urlretrieve(url, self.currFileName)
		self.currSongID += 1


	def __play_mp3(self, url):
		self.__download_mp3(url)

		def playMP3():
			mixer.music.load(self.currFileName)
			mixer.music.play(2)	# play() default arg is 1
			# For some reason, play() doens't work but does if it's argument is anything but 1
			# Currently plays for two iterations

		# Removes the MP3 file once song is done playing
		def checkPlayStatus():
			while pygame.mixer.music.get_busy():
				pass
			if (Path(self.currFileName).is_file()):
				os.remove(self.currFileName)
			self.play_next()

		threading.Thread(target=playMP3).start()
		# Added sleep to account for music busy check in checkPlayStatus happening before music starts playing
		time.sleep(5)
		threading.Thread(target=checkPlayStatus).start()
		return True


	"""
	Searches for the requested song
	If found, plays the song and removes it from the queue
	"""
	def play_song(self, name, artist):
		if (self.__search_track(name=name, artist=artist) != 1):
			return False
		self.__play_mp3(self.queue.pop(0))
		return True


	"""
	Pops the current song from the queue
	Plays the next song (now top of the queue)
	"""
	def play_next(self):
		if (len(self.queue) == 0):
			print("No songs in the queue")
			return False
		self.__play_mp3(self.queue.pop(0))
		return True


	"""
	Searches for 10 songs by the specified artist
	Clears the current queue
	Plays the first song
	"""
	def play_artist(self, artist):
		self.__search_track(artist=artist, inputLimit=10)
		self.play_next()
		return True


	def play_playlist(self, playlist):
		return True

