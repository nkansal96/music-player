import pytest
import exceptions

class TestExceptions(object):
	def test_invalid_auth(self):
		with pytest.raises(exceptions.InvalidAuth) as e:
			raise exceptions.InvalidAuth("message")
	
	def test_empty_queue(self):
		with pytest.raises(exceptions.EmptyQueue) as e:
			raise exceptions.EmptyQueue()
	
	def test_not_found(self):
		try:
			raise exceptions.NotFound(exceptions.NotFound.SONG, "test")
		except exceptions.NotFound as nf:
			assert nf.type == exceptions.NotFound.SONG
			assert nf.query == "test"
		except:
			assert False
		