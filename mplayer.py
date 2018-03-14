import subprocess, asyncio, time, select, threading

class MPlayer(object):
	def __init__(self):
		self.cmd = None
		self.playing = False
		self.paused = False
		self.volume = 25

	def __del__(self):
		self.stop()

	def play_url(self, url):
		if self.cmd != None:
			self.cmd.kill()
			self.cmd = None

		formattedUrl = url.replace("https://", "http://", 1)
		def create_player():
			self.playing = True
			self.paused = False
			self.volume = 25
			self.cmd = subprocess.Popen(["mplayer", "-quiet", formattedUrl], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
			self.cmd.wait()
			self.playing = False

		threading.Thread(target=create_player).start()
		# self.cmd.stdin.write(bytes("loadfile {}\n".format(url), "utf-8"))
		# self.cmd.stdin.flush()
	
	def set_volume(self, vol):
		key = b"9" if vol < self.volume else b"0"
		while abs(self.volume - vol) > 3:
			self.cmd.stdin.write(key)
			self.cmd.stdin.flush()
			self.volume += -3 if key == b"9" else 3

	def pause(self):
		if not self.paused:
			self.cmd.stdin.write(b"p")
			self.cmd.stdin.flush()
			self.paused = True
	
	def resume(self):
		if self.paused:
			self.cmd.stdin.write(b"p")
			self.cmd.stdin.flush()
			self.paused = False

	def stop(self):
		if self.cmd != None:
			self.cmd.kill()

# def main():
# 	p = MPlayer()
# 	p.play_url("http://p.scdn.co/mp3-preview/99b833cf96a8b56040859443d8688a2e322c6667?cid=8897482848704f2a8f8d7c79726a70d4")
# 	time.sleep(3)
# 	p.pause()
# 	time.sleep(3)
# 	p.resume()
# 	p.play_url("http://p.scdn.co/mp3-preview/b39f0ae16451e7aca47dec309ea7d55aad607b8e?cid=8897482848704f2a8f8d7c79726a70d4")
# 	time.sleep(3)

# if __name__ == "__main__":
# 	main()
