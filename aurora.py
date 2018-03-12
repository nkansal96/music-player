import auroraapi as aurora
from auroraapi.audio import AudioFile
from auroraapi.speech import Speech, continuously_listen

import spotifyPlayer as player

aurora.config.app_id = "ceb5d7c34056489150660ec5ebcc1c5f"
aurora.config.app_token = "6NWvZigglXLlmA4aD1k0iJctnNYigyG"
trigger_word = ""

valid_words = ["song", "artist", "volume"]
# valid_entities = lambda d: "object" in d and d["object"] in valid_words

def listen():

	for speech in continuously_listen(silence_len=1):
		text = speech.text()
		print(text.text)

		if len(text.text) > 0:
			i = text.interpret()
			print(i.intent)

			if i.intent == "play_song" :
				title = i.entities["song"]
				print(title)
				if "artist" in i.entities:
					artist = i.entities["artist"]
				else:
					artist = ""
				player.play_song(title, artist)

			if i.intent == "play_artist" and valid_entities(i.entities):
				artist = i.entities["artist"]
				player.play_song("", artist)
				pass

			if i.intent == "play_playlist" and valid_entities(i.entities):
				pass

			if i.intent == "play_next" and valid_entities(i.entities):
				pass

			if i.intent == "pause" and valid_entities(i.entities):
				player.pause()

			if i.intent == "resume" and valid_entities(i.entities):
				player.resume()

			if i.intent == "volume" and valid_entities(i.entities):
				volume = i.entities["volume"] #need to cast this as int
				player.volume(volume)


if __name__ == "__main__":
	listen()




