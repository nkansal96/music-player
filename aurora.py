import auroraapi as aurora
import settings

from auroraapi.audio import AudioFile
from auroraapi.speech import Speech, continuously_listen_and_transcribe
from auroraapi.interpret import Interpret
from spotifyPlayer import SpotifyPlayer



aurora.config.app_id = "ceb5d7c34056489150660ec5ebcc1c5f"
aurora.config.app_token = "6NWvZigglXLlmA4aD1k0iJctnNYigyG"
trigger_word = ""

# valid_words = ["song", "artist", "volume"]
player = SpotifyPlayer(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET)
# valid_entities = lambda d: "object" in d and d["object"] in valid_words

def listen():

	for text in continuously_listen_and_transcribe(silence_len=0.5):

		if len(text.text) > 0:
			i = text.interpret()

			if i.intent == "play_song":
				if "song" not in i.entities:
					continue 
				title = i.entities["song"]
				if "artist" in i.entities:
					artist = i.entities["artist"]
				else:
					artist = ""
				player.play_song(title, artist)
				pass

			if i.intent == "play_artist":
				artist = i.entities["artist"]
				player.play_song("", artist)
				pass

			if i.intent == "play_playlist":
				pass

			if i.intent == "play_next":
				pass

			if i.intent == "pause":
				player.pause()
				pass

			if i.intent == "resume":
				player.resume()
				pass

			if i.intent == "volume":
				print(i.entities)
				if "volume" not in i.entities or not i.entities["volume"].isdigit():
					continue 
				volume = int(i.entities["volume"])
				player.volume(volume)


if __name__ == "__main__":
	listen()




