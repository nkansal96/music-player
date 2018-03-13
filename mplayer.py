import subprocess, asyncio, time, select

class MPlayer(object):
	def __init__(self):
		self.paused = False
		self.cmd = subprocess.Popen(["mplayer", "-slave", "-quiet", "-idle"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

	def __del__(self):
		self.cmd.kill()

	def play_url(self, url):
		# TODO: replace https:// with http://
		self.cmd.stdin.write(bytes("loadfile {}\n".format(url), "utf-8"))
		self.cmd.stdin.flush()
	
	def set_volume(self, vol):
		self.cmd.stdin.write(bytes("volume {} 1\n".format(vol), "utf-8"))
		self.cmd.stdin.flush()

	def pause(self):
		if not self.paused:
			self.cmd.stdin.write(b"pause\n")
			self.cmd.stdin.flush()
			self.paused = True
	
	def resume(self):
		if self.paused:
			self.cmd.stdin.write(b"pause\n")
			self.cmd.stdin.flush()
			self.paused = False

	def playing(self):
		self.cmd.stdin.write(b"get_time_pos\n")
		self.cmd.stdin.flush()

		p = select.poll()
		p.register(self.cmd.stdout, select.POLLIN)
		now = time.time()
		data = ""

		while (time.time() - now < 1.0):
			pr = p.poll(0)
			if pr:
				data += str(self.cmd.stdout.readline())
		return "ANS_TIME_POSITION" in data
