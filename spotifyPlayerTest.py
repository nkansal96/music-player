import time
import settings

from spotifyPlayer import SpotifyPlayer

def main():
	p = SpotifyPlayer(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET)
	# p.play_song("Summer", "Marshmello")
	p.play_playlist("USA Top 50")
	# p.play_artist("Marshmello")
	while True:
		pass

if __name__ == "__main__":
	main()
