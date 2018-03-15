import time, os

class CLIOptions(object):
	def __init__(self):
		self.app_id=os.environ['APP_ID']
		self.app_token=os.environ['APP_TOKEN']
		self.device_id=None
		self.spotify_client_id=os.environ['SPOTIFY_CLIENT_ID']
		self.spotify_client_secret=os.environ['SPOTIFY_CLIENT_SECRET']
		self.silence_len=0.3
		self.trigger_word='box'

		aurora.config.app_id    = self.opts.app_id
		aurora.config.app_token = self.opts.app_token
		aurora.config.device_id = self.opts.device_id

		self.player = SpotifyPlayer(self.opts.spotify_client_id, self.opts.spotify_client_secret)