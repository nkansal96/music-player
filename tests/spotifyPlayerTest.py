import pytest
import time, os
import argparse
import auroraapi as aurora
from auroraapi.interpret import Interpret

from aurora import *
from exceptions import *
from common import CLIOptions

class TestSpotifyPlayer(object):
	def setup(self):
		self.opts = CLIOptions()
		self.player = self.opts.player

	# a valid song and artist query should return without failure
	def test_play_song(self):
		assert self.player.play_song('hello', 'adele')

	# a valid song and artist query should return without failure
	def test_play_song_without_artist(self):
		assert self.player.play_song('hello')

	# an invalid song query should raise a custom NotFound exception
	def test_play_song_invalid(self):
		with pytest.raises(NotFound) as e:
			self.player.play_song('qwertyasdfgzxcvb', 'asdfghjwertyx')

	# a valid artist query should return without failure
	def test_play_artist(self):
		assert self.player.play_artist('bruno mars')

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
		