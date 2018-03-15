import threading

import mplayer
from exceptions import *

import spotipy
import spotipy.oauth2 as oauth2

class SpotifyPlayer:
	def __init__(self, spotify_client_id, spotify_client_secret):
		self.queue = []
		self.player = mplayer.MPlayer()
		self.play_thread = None

		credentials = oauth2.SpotifyClientCredentials(
			client_id=spotify_client_id,
			client_secret=spotify_client_secret,
		)

		token = credentials.get_access_token()
		if not token:
			raise InvalidAuth()

		self.sp = spotipy.Spotify(auth=token)
	
	def __del__(self):
		self.queue.clear()
		self.player.stop()
	
	def _queue_tracks(self, tracks):
		"""
		Queue the given tracks
		"""
		self.queue.extend(map(lambda t: t["preview_url"], tracks))

	def _search_track(self, name="", artist="", trackLimit=1):
		"""
		Search for a track by name and artist
		"""
		searchQuery = "{} {}".format(name, artist).strip()
		result = []
		offset = 0

		while True:
			response = self.sp.search(searchQuery, limit=50, offset=offset, type="track", market="US")
			result.extend(_filter_tracks(response["tracks"]["items"]))
			offset += 50
			if len(result) >= trackLimit or response["tracks"]["next"] == None:
				break
		return result[:trackLimit]

	def _search_playlist(self, name):
		"""
		Search for a playlist and return its tracks
		"""
		# first find a playlist matching the given name
		searchResponse = self.sp.search(name, limit=1, type="playlist", market="US")
		playlists = searchResponse["playlists"]["items"]
		if len(playlists) == 0:
			return []
		ownerId = playlists[0]["owner"]["id"]
		playlistId = playlists[0]["id"]
		result = []
		offset = 0
		
		# then get a list of all of the songs in the playlist
		while True:
			response = self.sp.user_playlist_tracks(ownerId, playlist_id=playlistId, fields="items(track(name,artists(name),preview_url)),next", limit=50, offset=offset, market="US")
			result.extend(_filter_tracks(map(lambda i: i["track"], response["items"])))
			offset += 50
			if response["next"] == None:
				break
		return result

	def _start_player(self):
		"""
		Starts the player thread.
		It iterates through the entire queue and plays each song.
		"""
		if self.play_thread == None or not self.play_thread.is_alive():
			def play():
				while len(self.queue) > 0:
					self.player.play_url(self.queue.pop(0))
			self.play_thread = threading.Thread(target=play)
			self.play_thread.start()

	def play_song(self, name, artist):
		"""
		Plays a particular song given both a track name and track artist
		"""
		tracks = self._search_track(name=name, artist=artist)
		if len(tracks) == 0:
			raise NotFound(NotFound.SONG, "{} by {}".format(name, artist))
		self.queue.clear()
		self._queue_tracks(tracks)
		self.play_next()
		return name

	def play_next(self):
		"""
		If there are songs in the queue, this method will stop plaing the current one,
		which causes the play thread to move to the next song.
		"""
		if len(self.queue) == 0:
			return
		self.player.stop()
		self._start_player()

	def play_artist(self, artist):
		"""
		Given the name of an artist, `artist`, search for it, clear the queue, and
		queue all tracks. This method will immediately start playing the songs.
		"""
		tracks = self._search_track(artist=artist, trackLimit=50)
		if len(tracks) == 0:
			raise NotFound(NotFound.ARTIST, artist)
		self.queue.clear()
		self._queue_tracks(tracks)
		self.play_next()
		return artist

	def play_playlist(self, playlist):
		"""
		Given the name of a playlist, `playlist`, search for it, clear the queue, and
		queue all tracks. This method will immediately start playing the songs.
		"""
		tracks = self._search_playlist(playlist)
		if len(tracks) == 0:
			raise NotFound(NotFound.PLAYLIST, playlist)
		self.queue.clear()
		self._queue_tracks(tracks)
		self.play_next()
		return playlist

	def pause(self):
		""" Pause playback """
		self.player.pause()

	def resume(self):
		""" Resume playback """
		self.player.resume()

	def volume(self, value):
		"""
		Sets the volume to `value`, which should be between 0 and 100. If any other
		value is provided, the value is confined to the interval [0, 100].
		"""
		vol = max(0, min(100, value))
		self.player.set_volume(vol)
		return vol

def _filter_tracks(tracks):
	"""
	Given a list of spotify Track objects, filter out the ones that do not have
	a `preview_url` and return a list of objects with only the relevant fields
	(name, artists, preview_url)
	"""
	# get all tracks that have a preview URL
	tracks = filter(lambda track: track["preview_url"] != None, tracks)
	# return an array of tracks with only the "name", "artists", and "preview_url" properties
	return map(lambda track: {
		"name": track["name"],
		# get a list of all artist names
		"artists": map(lambda artist: artist["name"], track["artists"]),
		"preview_url": track["preview_url"],
	}, tracks)