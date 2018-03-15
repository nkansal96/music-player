import time
import settings

from spotify_player import SpotifyPlayer

def main():
	p = SpotifyPlayer(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET)

	# play three songs from a playlist
	p.play_playlist("USA Top 50")
	i = 0
	while i < 3:
		time.sleep(6)
		p.play_next()
		i += 1
	
	# play three songs from an artist
	p.play_artist("adele")
	i = 0
	while i < 3:
		time.sleep(6)
		p.play_next()
		i += 1

	# play a single song
	p.play_song("Summer", "Marshmello")
	time.sleep(5)

	# pause the song
	p.pause()
	time.sleep(3)

	# resume the song
	p.resume()
	time.sleep(3)

	# make it quiet
	p.volume(10)
	time.sleep(3)

	# make it loud
	p.volume(100)
	time.sleep(3)

if __name__ == "__main__":
	main()
