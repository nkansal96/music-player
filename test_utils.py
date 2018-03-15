import time
import utils
from test_common import CLIOptions

class TestDuck(object):
	def setup(self):
		opts = CLIOptions()
		self.player = opts.player
	
	def test_duck_not_playing(self):
		# this should not affect the volume
		ov = self.player.player.volume
		with utils.duck(self.player, 20) as d:
			assert d.volume == d.original_vol
			assert d.original_vol == self.player.player.volume
			assert ov == self.player.player.volume
		assert self.player.player.volume == ov
	
	def test_duck_playing(self):
		self.player.play_song("hello", "adele")
		time.sleep(2.0)
		ov = self.player.player.volume
		with utils.duck(self.player, 5) as d:
			assert d.volume == 5
			assert self.player.player.volume == 5
			time.sleep(1.0)
		assert self.player.player.volume == ov
		time.sleep(1.0)
		self.player.player.stop()
