import time
import settings

from spotifyPlayer import SpotifyPlayer

def main():
	p = SpotifyPlayer(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET)
	p.play_song("Summer", "Marshmello")
	# while True:
	# 	pass
	p.volume(100)
	time.sleep(5)
	p.pause()
	time.sleep(5)
	p.volume(30)
	p.resume()
	time.sleep(5)

if __name__ == "__main__":
	main()