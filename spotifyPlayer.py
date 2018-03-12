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

		# self.currSongID = 1
		self.queue = []
		self.mixer = mixer.init()

		self.currFileName = ""
		# self.tempDir = "mp3FilesTemp"
		# if not os.path.exists(self.tempDir):
		# 	os.makedirs(self.tempDir)

		credentials = oauth2.SpotifyClientCredentials(
			client_id=spotify_client_id,
			client_secret=spotify_client_secret)

		token = credentials.get_access_token()
		if not token:
			print("Could not get token")
			sys.exit()

		self.sp = spotipy.Spotify(auth=token)


	def __del__(self):
		if Path(self.currFileName).is_file():
			os.remove(self.currFileName)


	def __search_track(self, name="", artist="", inputLimit=1):
		numQueued = 0
		searchQuery = name + " " + artist
		result = self.sp.search(searchQuery, limit=inputLimit, type="track", market="US")
		for x in range(inputLimit):
			if len(result["tracks"]["items"]) == 0:
				print("Unable to find a match to the search query")
				return 0
			preview_url = result["tracks"]["items"][x]["preview_url"]
			if preview_url != None:
				self.queue.insert(0, preview_url)
				numQueued += 1
		print(numQueued)
		return numQueued


	def __search_playlist(self, name):
		numQueued = 0
		searchResult = self.sp.search(name, limit=1, type="playlist", market="US")
		if len(searchResult["playlists"]["items"]) == 0:
			print("Unable to find a match to the search query")
			return 0
		ownerId = searchResult["playlists"]["items"][0]["owner"]["id"]
		playlistId = searchResult["playlists"]["items"][0]["id"]

		playlistResult = self.sp.user_playlist_tracks(ownerId, playlist_id=playlistId, fields="items(track(name,preview_url))", limit=20, market="US")
		if len(playlistResult["items"]) == 0:
			print("Unable to find a match to the search query")
			return 0
		for track in reversed(playlistResult["items"]):		# reversed to preserve order
			preview_url = track["track"]["preview_url"]
			if preview_url != None:
				self.queue.insert(0, preview_url)
				numQueued += 1
		return numQueued


	def __download_mp3(self, url):
		# Make sure existing tempfile removed first
		if Path(self.currFileName).is_file():
			os.remove(self.currFileName)
		self.currFileName, headers = urllib.request.urlretrieve(url)


	"""
	Attempts to download song.
	After 10 seconds after a song starts playing, begin to check if song still playing.
	If song not playing, delete its tempfile and move on to next song.
	If song is not able to be downloaded/played within 10 seconds, move on to next song 
	"""
	def __play_mp3(self, url):
		self.__download_mp3(url)

		def playMP3():
			mixer.music.load(self.currFileName)
			mixer.music.play()	# play() default arg is 1

		# Removes the MP3 file once song is done playing
		def checkPlayStatus():
			while pygame.mixer.music.get_busy():
				pass
			if Path(self.currFileName).is_file():
				os.remove(self.currFileName)
			self.play_next()

		threading.Thread(target=playMP3).start()
		# Added sleep to account for music busy check in checkPlayStatus happening before music starts playing
		time.sleep(10)
		threading.Thread(target=checkPlayStatus).start()
		return True


	"""
	Searches for the requested song
	If found, plays the song and removes it from the queue
	"""
	def play_song(self, name, artist):
		if self.__search_track(name=name, artist=artist) != 1:
			return False
		self.__play_mp3(self.queue.pop(0))
		return True


	"""
	Pops the current song from the queue
	Plays the next song (now top of the queue)
	"""
	def play_next(self):
		if len(self.queue) == 0:
			print("No songs in the queue")
			return False
		self.__play_mp3(self.queue.pop(0))
		return True


	# Searches for up to 20 songs by the specified artist
	def play_artist(self, artist):
		self.__search_track(artist=artist, inputLimit=20)
		self.play_next()
		return True


	# Searches for up to 20 songs by the specified artist
	def play_playlist(self, playlist):
		self.__search_playlist(playlist)
		self.play_next()
		return True

