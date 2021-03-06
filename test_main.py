import time
from auroraapi.interpret import Interpret

from main import *
from test_common import CLIOptions

class TestStartPlayer(object):
	def setup(self):
		opts = CLIOptions()
		self.player = opts.player

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
		self.player.player.stop()

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