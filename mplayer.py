import subprocess

class MPlayer(object):
	def __init__(self):
		self.cmd = None
		self.playing = False
		self.paused = False
		self.volume = 50

	def __del__(self):
		self.stop()

	def play_url(self, url):
		url = url.replace("https://", "http://", 1)
		self.stop()
		self.volume = 50
		self.playing = True
		self.paused = False
		self.cmd = subprocess.Popen(["mplayer", "-quiet", "-volume", "50", url], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		self.cmd.wait()
		self.playing = False
		self.cmd = None
	
	def set_volume(self, vol):
		if self.cmd == None:
			return
		key = b"9" if vol < self.volume else b"0"
		while abs(self.volume - vol) >= 3:
			self.cmd.stdin.write(key)
			self.cmd.stdin.flush()
			self.volume += -3 if key == b"9" else 3

	def pause(self):
		if self.cmd == None:
			return
		if not self.paused:
			self.cmd.stdin.write(b"p")
			self.cmd.stdin.flush()
			self.paused = True
	
	def resume(self):
		if self.cmd == None:
			return
		if self.paused:
			self.cmd.stdin.write(b"p")
			self.cmd.stdin.flush()
			self.paused = False

	def stop(self):
		if self.cmd != None:
			self.cmd.kill()
			self.cmd = None
		self.playing = False
		self.paused = False
