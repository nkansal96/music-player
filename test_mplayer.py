import time, threading
from mplayer import *

class TestMPlayer(object):
	def setup(self):
		self.mplayer = MPlayer()
		self.url = "https://archive.org/download/testmp3testfile/mpthreetest.mp3"

	def test_play_bad_url(self):
		start = time.time()
		self.mplayer.play_url("http://badurl")
		end = time.time()
		assert not self.mplayer.playing
		assert not self.mplayer.paused
		assert end - start < 1.0
	
	def test_play_good_url(self):
		t = threading.Thread(target=self.mplayer.play_url, args=(self.url,))
		assert not self.mplayer.playing
		assert not self.mplayer.paused
		t.start()
		time.sleep(1.0)
		assert self.mplayer.playing
		assert not self.mplayer.paused
		self.mplayer.stop()
		t.join()

	def test_increase_volume(self):
		t = threading.Thread(target=self.mplayer.play_url, args=(self.url,))
		t.start()
		time.sleep(1.0)
		assert self.mplayer.volume == 50
		self.mplayer.set_volume(74)
		assert self.mplayer.volume == 74
		self.mplayer.stop()
		t.join()

	def test_decrease_volume(self):
		t = threading.Thread(target=self.mplayer.play_url, args=(self.url,))
		t.start()
		time.sleep(1.0)
		assert self.mplayer.volume == 50
		self.mplayer.set_volume(2)
		assert self.mplayer.volume == 2
		self.mplayer.stop()
		t.join()

	def test_volume_stopped(self):
		# should not do anything
		assert self.mplayer.volume == 50
		self.mplayer.set_volume(20)
		assert self.mplayer.volume == 50

	def test_pause_stopped(self):
		# should do nothing
		assert not self.mplayer.paused
		self.mplayer.pause()
		assert not self.mplayer.paused
	
	def test_resume_stopped(self):
		# should do nothing
		assert not self.mplayer.paused
		self.mplayer.pause()
		assert not self.mplayer.paused
	
	def test_stop_stopped(self):
		# should do nothing
		assert not self.mplayer.playing
		self.mplayer.stop()
		assert not self.mplayer.playing

	def test_pause_playing(self):
		t = threading.Thread(target=self.mplayer.play_url, args=(self.url,))
		t.start()
		time.sleep(1.0)
		assert self.mplayer.playing
		assert not self.mplayer.paused
		self.mplayer.pause()
		assert self.mplayer.playing
		assert self.mplayer.paused
		self.mplayer.stop()
		t.join()

	def test_resume_playing(self):
		t = threading.Thread(target=self.mplayer.play_url, args=(self.url,))
		t.start()
		time.sleep(1.0)
		assert self.mplayer.playing
		assert not self.mplayer.paused
		self.mplayer.pause()
		assert self.mplayer.playing
		assert self.mplayer.paused
		self.mplayer.resume()
		assert self.mplayer.playing
		assert not self.mplayer.paused
		self.mplayer.stop()
		t.join()

	def test_stop_playing(self):
		t = threading.Thread(target=self.mplayer.play_url, args=(self.url,))
		assert not self.mplayer.playing
		assert not self.mplayer.paused
		t.start()
		time.sleep(1.0)
		assert self.mplayer.playing
		assert not self.mplayer.paused
		self.mplayer.stop()
		assert not self.mplayer.playing
		assert not self.mplayer.paused
		assert not self.mplayer.cmd
		t.join()
	