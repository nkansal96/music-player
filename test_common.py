import time, os
import auroraapi as aurora

from spotify_player import SpotifyPlayer

class CLIOptions(object):
	def __init__(self):
		self.app_id=os.environ['APP_ID']
		self.app_token=os.environ['APP_TOKEN']
		self.device_id=None
		self.spotify_client_id=os.environ['SPOTIFY_CLIENT_ID']
		self.spotify_client_secret=os.environ['SPOTIFY_CLIENT_SECRET']
		self.silence_len=0.3
		self.trigger_word='box'

		aurora.config.app_id    = self.app_id
		aurora.config.app_token = self.app_token
		aurora.config.device_id = self.device_id

		self.player = SpotifyPlayer(self.spotify_client_id, self.spotify_client_secret)