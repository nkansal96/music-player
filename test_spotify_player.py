import pytest
import time

from exceptions import *
from spotify_player import *
from test_common import CLIOptions

class TestSpotifyPlayer(object):
	def setup(self):
		self.opts = CLIOptions()
		self.player = self.opts.player
	
	def test_spotify_player_invalid_auth(self):
		with pytest.raises(InvalidAuth):
			p = SpotifyPlayer("bad", "auth")

	# a valid song and artist query should return without failure
	def test_play_song(self):
		assert self.player.play_song('hello', 'adele')
		time.sleep(1.0)
		self.player.pause()

	# a valid song and artist query should return without failure
	def test_play_song_without_artist(self):
		assert self.player.play_song('hello', '')
		time.sleep(1.0)
		self.player.pause()

	# an invalid song query should raise a custom NotFound exception
	def test_play_song_invalid(self):
		with pytest.raises(NotFound) as e:
			self.player.play_song('qwertyasdfgzxcvb', 'asdfghjwertyx')

	# a valid artist query should return without failure
	def test_play_artist(self):
		assert self.player.play_artist('bruno mars')
		time.sleep(1.0)
		self.player.pause()

	# an invalid artist query should raise a custom NotFound exception
	def test_play_artist_invalid(self):
		with pytest.raises(NotFound) as e:
			self.player.play_artist('askdjflkajf')

	# self.player.pause should not cause a runtime error
	def test_pause(self):
		self.player.pause()

	# self.player.resume should not cause a runtime error
	def test_resume(self):
		self.player.resume()
		