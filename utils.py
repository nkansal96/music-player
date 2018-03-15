import time

class duck(object):
	def __init__(self, player, target):
		self.player = player
		self.target = target
		self.step_size = 5
		self.step_interval = 0.03
		self.volume = player.player.volume
		self.original_vol = player.player.volume
	
	def __enter__(self):
		if self.target >= self.player.player.volume:
			return self
		for i in range(self.original_vol, self.target-1, -self.step_size):
			self.player.volume(i)
			time.sleep(self.step_interval)
		self.volume = self.player.player.volume
		return self

	def __exit__(self, type, value, traceback):
		for i in range(self.target, self.original_vol + 1, self.step_size):
			self.player.volume(i)
			time.sleep(self.step_interval)
