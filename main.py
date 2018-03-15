import argparse
from collections import defaultdict

import auroraapi as aurora
from auroraapi.text import *
from auroraapi.speech import *

from spotify_player import SpotifyPlayer
from exceptions import *
from utils import *

def play_song(player, entities):
	return player.play_song(entities["song"], entities["artist"])

def play_artist(player, entities):
	return player.play_artist(entities["artist"])

def play_playlist(player, entities):
	return player.play_playlist(entities["playlist"])

def play_next(player, entities):
	player.play_next()
	return True

def pause(player, entities):
	player.pause()
	return True

def resume(player, entities):
	player.resume()
	return True

def set_volume(player, entities):
	return player.volume(int(entities["volume"]))

CMD_MAP = {
	"play_song":     { "fn": play_song,     "required": ["song"] },
	"play_artist":   { "fn": play_artist,   "required": ["artist"] },
	"play_playlist": { "fn": play_playlist, "required": ["playlist"] },
	"play_next":     { "fn": play_next,     "required": [] },
	"turn_off":      { "fn": pause,         "required": [] },
	"pause":         { "fn": pause,         "required": [] },
	"resume":        { "fn": resume,        "required": [] },
	"volume":        { "fn": set_volume,    "required": ["volume"] },	
}

def process_command(player, command):
	print(command.intent, command.entities)
	try:
		cmd = CMD_MAP[command.intent]
		if not all(x in command.entities for x in cmd["required"]):
			raise ValueError()
		return cmd["fn"](player, defaultdict(str, command.entities))
	except EmptyQueue:
		pass
	except NotFound as nf:
		text = Text("I couldn't find the {} {}".format(nf.type, nf.query))
		print(text.text)
		t.speech().audio.play()
	except ValueError:
		print("Required entities not provided: {{ intent: {}, entities: {} }}".format(command.intent, command.entities))
	except:
		print("Could not parse: {{ intent: {}, entities: {} }}".format(command.intent, command.entities))
	return None

def start_player(opts):
	player = SpotifyPlayer(opts.spotify_client_id, opts.spotify_client_secret)
	print("Ready")
	for text in continuously_listen_and_transcribe(length=1.5):
		if opts.trigger_word.lower() in text.text.lower():
			with duck(player, 5):
				print("Awaiting command...")
				s = listen(silence_len=opts.silence_len)
				s.audio.play()
				text = s.text()
				if len(text.text) > 0: 
					print(text.text)
					process_command(player, text.interpret())
		print("Ready")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--app_id", action="store", help="the Aurora app ID", type=str, required=True)
	parser.add_argument("--app_token", action="store", help="the Aurora app token", type=str, required=True)
	parser.add_argument("--device_id", action="store", help="the unique ID for this device", type=str, default=None)
	parser.add_argument("--spotify_client_id", action="store", help="The Spotify client ID", type=str, required=True)
	parser.add_argument("--spotify_client_secret", action="store", help="The Spotify client secret", type=str, required=True)
	parser.add_argument("--trigger_word", action="store", help="the trigger word for commands", type=str, default="box")
	parser.add_argument("--silence_len", action="store", help="the amount of silence (seconds)", type=float, default=0.3)

	opts = parser.parse_args()

	aurora.config.app_id    = opts.app_id
	aurora.config.app_token = opts.app_token
	aurora.config.device_id = opts.device_id

	start_player(opts)
	