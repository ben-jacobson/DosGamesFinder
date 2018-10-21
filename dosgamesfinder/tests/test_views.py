from django.test import TestCase
from django.urls import reverse

from .base import create_test_publisher, create_test_dosgame

HTTP_OK = 200
HTTP_NOT_ALLOWED = 405

class LayoutAndStylingTest(TestCase):
    def test_static_files_have_been_passed_to_browser(self):
        ''' 
        Unit Test - Test that the JS script tags and CSS href tags have been rendered in the browser 
        '''
        expected_lines = [
            '<link rel="stylesheet" href="/static/css/bootstrap.min.css" />',
            '<link rel="stylesheet" href="/static/css/main.css" />',        
            '<script src="/static/vendor_js/jquery-3.2.1.slim.min.js" type="text/javascript"></script>',
            '<script src="/static/vendor_js/underscore-min.js" type="text/javascript"></script>',
            '<script src="/static/vendor_js/backbone-min.js" type="text/javascript"></script>',
            '<script src="/static/vendor_js/popper.min.js" type="text/javascript"></script>',
            '<script src="/static/vendor_js/bootstrap.min.js" type="text/javascript"></script>',
            '<script src="/static/app_js/config.js" type="text/javascript"></script>',
            '<script src="/static/app_js/models.js" type="text/javascript"></script>',
            '<script src="/static/app_js/collections.js" type="text/javascript"></script>',
            '<script src="/static/app_js/views.js" type="text/javascript"></script>',
            '<script src="/static/app_js/routers.js" type="text/javascript"></script>',
        ]
        response = self.client.get(reverse('home'))

        # each and every one of these lines should appear in the response HTML
        for line in expected_lines:
            self.assertContains(response, line)

class ListViewPermissionsTests(TestCase):
    '''
    Unit Tests - Testing the ListView API endpoints, check that the various HTTP request methods return expected response codes
    '''
    def test_can_send_get_request_to_endpoint(self):
        response = self.client.get(reverse('DosGamesListView'))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_head_request_to_endpoint(self):
        response = self.client.head(reverse('DosGamesListView'))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_options_request_to_endpoint(self):
        response = self.client.options(reverse('DosGamesListView'))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_cannot_send_put_request_to_endpoint(self):
        response = self.client.put(reverse('DosGamesListView'))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_post_request_to_endpoint(self):
        response = self.client.post(reverse('DosGamesListView'))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
    
    def test_cannot_send_delete_request_to_endpoint(self):
        response = self.client.delete(reverse('DosGamesListView'))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_patch_request_to_endpoint(self):
        response = self.client.patch(reverse('DosGamesListView'))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
       
class DetailViewPermissionTests(TestCase):
    '''
    Unit Tests - Testing the DetailView API endpoints, check that the various HTTP request methods return expected response codes
    '''
    def setUp(self):
        # for these tests, we'll need a test dosgame in the database
        self.test_publisher = create_test_publisher()
        self.test_dosgame = create_test_dosgame(publisher=self.test_publisher)
        self.test_dosgame_id = {'pk': self.test_dosgame.id}

    def test_can_send_get_request_to_endpoint(self):
        response = self.client.get(reverse('DosGamesDetailView', kwargs=self.test_dosgame_id))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_head_request_to_endpoint(self):
        response = self.client.head(reverse('DosGamesDetailView', kwargs=self.test_dosgame_id))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_options_request_to_endpoint(self):
        response = self.client.options(reverse('DosGamesDetailView', kwargs=self.test_dosgame_id))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_cannot_send_put_request_to_endpoint(self):
        response = self.client.put(reverse('DosGamesDetailView', kwargs=self.test_dosgame_id))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_post_request_to_endpoint(self):
        response = self.client.post(reverse('DosGamesDetailView', kwargs=self.test_dosgame_id))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
    
    def test_cannot_send_delete_request_to_endpoint(self):
        response = self.client.delete(reverse('DosGamesDetailView', kwargs=self.test_dosgame_id))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_patch_request_to_endpoint(self):
        response = self.client.patch(reverse('DosGamesDetailView', kwargs=self.test_dosgame_id))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
               
