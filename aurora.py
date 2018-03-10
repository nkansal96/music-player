import auroraapi as auroraapi
from auroraapi.audio import AudioFile
from auroraapi.speech import Speech, continuously_listen

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

				pass

			if i.intent == "play_artist":
				pass

			if i.intent == "play_playlist":
				pass

			if i.intent == "play_next":
				pass

			if i.intent == "pause":
				pass

			if i.intent == "resume":
				pass

			if i.intent == "volume":
				pass

			if i.intent == "weather":
				loc = i.entities["location"]
				






