import auroraapi as auroraapi
from auroraapi.audio import AudioFile
from auroraapi.speech import Speech, continuously_listen

import spotifyPlayer as player

import 

aurora.config.add_id = ""
aurora.config.app_token = ""
trigger_word = ""

def listen():

	for speech in continuously_listen(silence_len=1):
		text = speech.text()
		print(text.text)

		if trigger_word in text.text:
			i = text.interpret()
			print(i.intent)

			if i.intent == "play_song":
				title = i.entities["song"]
				if "artist" in i.entities:
					artist = i.entities["artist"]
				else:
					artist = ""
				player.play_song(title, artist)

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

			if i.intent == "resume":
				player.resume()

			if i.intent == "volume":
				volume = i.entities["volume"] #need to cast this as int
				player.volume(volume)







