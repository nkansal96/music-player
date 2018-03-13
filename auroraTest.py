import pytest
import time
import argparse
import auroraapi as aurora
from auroraapi.interpret import Interpret

from aurora import *

class CLIOptions():
	def __init__(self):
		self.app_id='ceb5d7c34056489150660ec5ebcc1c5f'
		self.app_token='6NWvZigglXLlmA4aD1k0iJctnNYigyG'
		self.device_id=None
		self.spotify_client_id='9714ff73fa2f4b0b947ef433da16656c'
		self.spotify_client_secret='a79a370dff33474c85f0c639e9df9eba'
		self.silence_len=0.3
		self.trigger_word='box'

	def update_trigger_word(trigger_word):
		self.trigger_word = trigger_word

class TestStartPlayer(object):
	def setup(self):
		self.opts = CLIOptions()

		aurora.config.app_id    = self.opts.app_id
		aurora.config.app_token = self.opts.app_token
		aurora.config.device_id = self.opts.device_id

		self.player = SpotifyPlayer(self.opts.spotify_client_id, self.opts.spotify_client_secret)

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
		assert not process_command(self.player, i)

	def test_process_command_entity_NA(self):
		i = Interpret({
				"text": "play the song",
				"intent": "play_song",
				"entities": {}
			})
		assert not process_command(self.player, i)
