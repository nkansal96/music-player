import pytest
import time, os
import argparse
import auroraapi as aurora
from auroraapi.interpret import Interpret

from aurora import *
from exceptions import *

class CLIOptions(object):
	def __init__(self):
		self.app_id=''
		self.app_token=''
		self.device_id=None
		self.spotify_client_id=''
		self.spotify_client_secret=''
		self.silence_len=0.3
		self.trigger_word='box'

	def setup(self):
		self.opts = CLIOptions()
		self.opts.app_id = os.environ['APP_ID']
		self.opts.app_token = os.environ['APP_TOKEN']
		self.opts.spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']
		self.opts.spotify_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']

		aurora.config.app_id    = self.opts.app_id
		aurora.config.app_token = self.opts.app_token
		aurora.config.device_id = self.opts.device_id

		self.player = SpotifyPlayer(self.opts.spotify_client_id, self.opts.spotify_client_secret)

	def update_trigger_word(trigger_word):
		self.trigger_word = trigger_word

class TestStartPlayer(object):
	def setup(self):
		CLIOptions.setup(self);

	def test_process_command(self):
		i = Interpret({
				"text": "play the song hello by adele",
		 		"intent": "play_song",
		 	 	"entities": {
		 	    	"artist": "adele",
		 	    	"song": "hello"
		 	  	}
		 	})
		assert process_command(self.player, i)
		time.sleep(0.1)

	def test_process_command_intent_not_found(self):
		i = Interpret({
				"text": "set a timer for 10 minutes",
				"intent": "set_timer",
				"entities": {
					"duration": "10 minutes"
				}
			})
		assert None == process_command(self.player, i)

	def test_process_command_entity_NA(self):
		i = Interpret({
				"text": "play the song",
				"intent": "play_song",
				"entities": {}
			})
		assert None == process_command(self.player, i)

class TestSpotifyPlayer(object):
	def setup(self):
		CLIOptions.setup(self)

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
		