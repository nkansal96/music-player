class InvalidAuth(Exception):
	pass

class EmptyQueue(Exception):
	pass

"""
raise NotFound(NotFound.SONG, "Hello")
try:
	# Do something
except NotFound as nf:
	s = "Couldn't find the {} {}".format(nf.type, nf.query)
"""
class NotFound(Exception):
	SONG = "song"
	ARTIST = "artist"
	PLAYLIST = "playlist"

	def __init__(self, type, query):
		super().__init__()
		self.type = type
		self.query = query
