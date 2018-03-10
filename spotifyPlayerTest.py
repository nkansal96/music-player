from spotifyPlayer import SpotifyPlayer
import settings

def main():
	p = SpotifyPlayer(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET)
	p.play_song("Summer", "Marshmello")
	while True:
		pass

if __name__ == "__main__":
	main()