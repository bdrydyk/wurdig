from wurdig.tests import *

class TestPageController(TestController):

    def test_home(self):
        response = self.app.get(url(controller='page', action='home'))
        # Test response...
        
    def test_view(self):
        response = self.app.get(url(controller='page', action='view', path='about'))
        # assert hasattr(response, 'cache') is True
        assert 'About me and this site' in response
        assert '<h3>ElseWhere</h3>' in response
        assert 'REQUEST_METHOD' in response.req.environ
        
    def test_view_404_missing_path(self):
        response = self.app.get(url(controller='page', action='view'), status=404)
        
    def test_view_404_invalid_path(self):
        response = self.app.get(url(controller='page', action='view', path='foobar'), status=404)