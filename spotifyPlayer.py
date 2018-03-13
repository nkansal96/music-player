import sys
import os
import signal
import time
import pprint
import json
import urllib.request
import pathlib
import threading
import pprint
import mplayer

from pathlib import Path
from exceptions import *

import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

"""
[ Play control thread ]
  ^
  |
[ Play status thread ]
  ^
  |
[ SpotifyPlayer thread ]
"""

class SpotifyPlayer:
	def __init__(self, spotify_client_id, spotify_client_secret):
		self.queue = []
		self.currFileName = ""
		self.playMP3Thread = None

		self.player = mplayer.MPlayer()

		credentials = oauth2.SpotifyClientCredentials(
			client_id=spotify_client_id,
			client_secret=spotify_client_secret)

		token = credentials.get_access_token()
		if not token:
			raise InvalidAuth()

		self.sp = spotipy.Spotify(auth=token)


	def __del__(self):
		if Path(self.currFileName).is_file():
			os.remove(self.currFileName)


	def _queue_tracks(self, tracks):
		numQueued = 0
		for track in tracks:
			if track["preview_url"] != None:
				self.queue.append(track["preview_url"])
				numQueued += 1
		return numQueued


	def _search_track(self, name="", artist="", inputLimit=1):
		searchQuery = name + " " + artist
		result = []
		offset = 0

		while True:
			response = self.sp.search(searchQuery, limit=inputLimit, offset=offset, type="track", market="US")
			for track in response["tracks"]["items"]:
				preview_url = track["preview_url"]
				if preview_url != None:
					trackInfo = {}
					artists = []

					name = track["name"]

					for artist in track["artists"]:
						artists.append(artist["name"])

					trackInfo = { "name": name, "artists": artists, "preview_url": preview_url }
					result.append(trackInfo)
			offset += inputLimit
			if response["tracks"]["next"] == None:
				break
		return result


	def _search_playlist(self, name, inputLimit):
		result = []
		offset = 0

		searchResponse = self.sp.search(name, limit=1, type="playlist", market="US")
		if len(searchResponse["playlists"]["items"]) == 0:
			return result
		ownerId = searchResponse["playlists"]["items"][0]["owner"]["id"]
		playlistId = searchResponse["playlists"]["items"][0]["id"]
		playlistName = searchResponse["playlists"]["items"][0]["name"]

		while True:
			playlistResponse = self.sp.user_playlist_tracks(ownerId, playlist_id=playlistId, fields="items(track(name,artists(name),preview_url)),next", limit=inputLimit, offset=offset, market="US")
			for track in playlistResponse["items"]:
				preview_url = track["track"]["preview_url"]
				if preview_url != None:
					trackInfo = {}
					artists = []

					name = track["track"]["name"]

					for artist in track["track"]["artists"]:
						artists.append(artist["name"])

					trackInfo = { "name": name, "artists": artists, "preview_url": preview_url, "playlist": playlistName }
					result.append(trackInfo)
			offset += inputLimit
			if playlistResponse["next"] == None:
				break
		return result


	def _download_mp3(self, url):
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
	def _play_mp3(self, url):
		# self.__download_mp3(url)

		def playMP3():
			self.player.play_url(url)

		def checkPlayStatus():
			print("Playing status (outside while loop): " + str(self.player.playing()))
			while self.player.playing():
				print("Playing status: " + str(self.player.playing()))
				pass
			self.play_next()

		def playThread():
			self.playMP3Thread = threading.Thread(target=playMP3)
			self.playMP3Thread.start()
			# Added sleep to account for music busy check in checkPlayStatus happening before music starts playing
			time.sleep(5)
			threading.Thread(target=checkPlayStatus).start()

		threading.Thread(target=playThread).start()
		return True


	def play_song(self, name, artist):
		track = self._search_track(name=name, artist=artist)		# [{name,artist,url}]
		if len(track) == 0:
			raise NotFound(NotFound.SONG, "{} by {}".format(name, artist))
		self.queue.clear()
		self._queue_tracks(track)
		self.play_next()
		return track


	# Pops song from top of queue and plays it
	def play_next(self):
		if len(self.queue) == 0:
			raise EmptyQueue()
		if self.playMP3Thread != None:
			pass
			# TODO: kill thread
		self._play_mp3(self.queue.pop(0))


	# Searches for up to 20 songs by the specified artist
	def play_artist(self, artist):
		tracks = self._search_track(artist=artist, inputLimit=20)
		if len(tracks) == 0:
			raise NotFound(NotFound.ARTIST, "{}".format(artist))
		self.queue.clear()
		self._queue_tracks(tracks)
		self.play_next()
		return artist


	# Searches for up to 20 songs by the specified artist
	def play_playlist(self, playlist):
		tracks = self._search_playlist(playlist, 20)
		if len(tracks) == 0:
			raise NotFound(NotFound.PLAYLIST, "{}".format(playlist))
		self.queue.clear()
		self._queue_tracks(tracks)
		self.play_next()
		return playlist


	def pause(self):
		self.player.pause()

	def resume(self):
		self.player.resume()

	# TODO: verify this is correct
	def volume(self, value):
		# vol = max(0, min(100, value)) / 100
		self.player.set_volume(value)
