class InvalidAuth(Exception):
	def __init__(self, message):
		super().__init__(message)

class EmptyQueue(Exception):
	def __init__(self):
		super().__init__("You tried to call play on an empty queue")

class NotFound(Exception):
	SONG = "song"
	ARTIST = "artist"
	PLAYLIST = "playlist"

	def __init__(self, type, query):
		super().__init__("Could not find {} {}".format(type, query))
		self.type = type
		self.query = query
