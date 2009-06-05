from wurdig.tests import *

class TestMovieController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='movie', action='index'))
        # Test response...
