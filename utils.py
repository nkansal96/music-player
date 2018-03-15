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
		step = -self.step_size if self.target < self.original_vol else self.step_size
		target = self.target - 1 if self.target < self.original_vol else self.target + 1
		for i in range(self.original_vol, target, step):
			self.player.volume(i)
			time.sleep(self.step_interval)
		self.volume = self.player.player.volume
		return self

	def __exit__(self, type, value, traceback):
		step = -self.step_size if self.target > self.original_vol else self.step_size
		orig = self.original_vol - 1 if self.target > self.original_vol else self.original_vol + 1
		for i in range(self.target, orig, step):
			self.player.volume(i)
			time.sleep(self.step_interval)
