from django.test import TestCase
from django.urls import reverse

from .base import create_test_publisher, create_test_genre, create_test_dosgame, test_objects_mixin

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
            '<script src="/static/vendor_js/jquery-3.3.1.min.js" type="text/javascript"></script>',
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

class SerializerListViewTests(test_objects_mixin, TestCase):
    def test_dosgame_listview_returns_list(self):
        a = create_test_dosgame(title='abracadabra', publisher=self.test_publisher, genre=self.test_genre)
        b = create_test_dosgame(title='beetlejuice', publisher=self.test_publisher, genre=self.test_genre)
        c = create_test_dosgame(title='commodore', publisher=self.test_publisher, genre=self.test_genre)

        response = self.client.get(reverse('DosGamesListView'))
        self.assertContains(response, a.title)
        self.assertContains(response, b.title)
        self.assertContains(response, c.title)

    def test_publisher_listview_returns_list(self):
        a = create_test_publisher(name='abracadabra')
        b = create_test_publisher(name='beetlejuice')
        c = create_test_publisher(name='commodore')

        response = self.client.get(reverse('PublisherListView'))
        self.assertContains(response, a.name)
        self.assertContains(response, b.name)
        self.assertContains(response, c.name)   

    def test_genre_listview_returns_list(self):
        a = create_test_genre(name='abracadabra')
        b = create_test_genre(name='beetlejuice')
        c = create_test_genre(name='commodore')

        response = self.client.get(reverse('GenreListView'))
        self.assertContains(response, a.name)
        self.assertContains(response, b.name)
        self.assertContains(response, c.name)              

class SerializerDetailViewTests(test_objects_mixin, TestCase):
    def test_dosgame_detailview_returns_only_specific_object(self):
        a = create_test_dosgame(title='abracadabra', publisher=self.test_publisher, genre=self.test_genre)
        b = create_test_dosgame(title='beetlejuice', publisher=self.test_publisher, genre=self.test_genre)
        c = create_test_dosgame(title='commodore', publisher=self.test_publisher, genre=self.test_genre)

        response = self.client.get(reverse('DosGamesDetailView', kwargs={'slug': b.slug}))
        self.assertNotContains(response, a.title)
        self.assertContains(response, b.title)
        self.assertNotContains(response, c.title)

    def test_publisher_detailview_returns_only_specific_object(self):
        a = create_test_publisher(name='abracadabra')
        b = create_test_publisher(name='beetlejuice')
        c = create_test_publisher(name='commodore')

        response = self.client.get(reverse('PublisherDetailView', kwargs={'slug': b.slug}))
        self.assertNotContains(response, a.name)
        self.assertContains(response, b.name)
        self.assertNotContains(response, c.name)

    def test_genre_detailview_returns_only_specific_object(self):
        a = create_test_genre(name='abracadabra')
        b = create_test_genre(name='beetlejuice')
        c = create_test_genre(name='commodore')

        response = self.client.get(reverse('GenreDetailView', kwargs={'slug': b.slug}))
        self.assertNotContains(response, a.name)
        self.assertContains(response, b.name)
        self.assertNotContains(response, c.name)        


class DosGameListViewPermissionsTests(TestCase):
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
       
class DosGameDetailViewPermissionTests(TestCase):
    '''
    Unit Tests - Testing the DetailView API endpoints, check that the various HTTP request methods return expected response codes
    '''
    def setUp(self):
        # for these tests, we'll need a test dosgame in the database
        self.test_publisher = create_test_publisher()
        self.test_genre = create_test_genre()
        self.test_dosgame = create_test_dosgame(publisher=self.test_publisher, genre=self.test_genre)
        self.test_dosgame_id = {'slug': self.test_dosgame.slug}

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
               
class PublisherListViewPermissionsTests(TestCase):
    '''
    Unit Tests - Testing the ListView API endpoints, check that the various HTTP request methods return expected response codes
    '''
    def test_can_send_get_request_to_endpoint(self):
        response = self.client.get(reverse('PublisherListView'))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_head_request_to_endpoint(self):
        response = self.client.head(reverse('PublisherListView'))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_options_request_to_endpoint(self):
        response = self.client.options(reverse('PublisherListView'))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_cannot_send_put_request_to_endpoint(self):
        response = self.client.put(reverse('PublisherListView'))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_post_request_to_endpoint(self):
        response = self.client.post(reverse('PublisherListView'))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
    
    def test_cannot_send_delete_request_to_endpoint(self):
        response = self.client.delete(reverse('PublisherListView'))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_patch_request_to_endpoint(self):
        response = self.client.patch(reverse('PublisherListView'))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
       
class PublisherDetailViewPermissionTests(TestCase):
    '''
    Unit Tests - Testing the DetailView API endpoints, check that the various HTTP request methods return expected response codes
    '''
    def setUp(self):
        # for these tests, we'll need a test dosgame in the database
        self.test_publisher = create_test_publisher()
        self.test_publisher_id = {'slug': self.test_publisher.slug}

    def test_can_send_get_request_to_endpoint(self):
        response = self.client.get(reverse('PublisherDetailView', kwargs=self.test_publisher_id))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_head_request_to_endpoint(self):
        response = self.client.head(reverse('PublisherDetailView', kwargs=self.test_publisher_id))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_options_request_to_endpoint(self):
        response = self.client.options(reverse('PublisherDetailView', kwargs=self.test_publisher_id))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_cannot_send_put_request_to_endpoint(self):
        response = self.client.put(reverse('PublisherDetailView', kwargs=self.test_publisher_id))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_post_request_to_endpoint(self):
        response = self.client.post(reverse('PublisherDetailView', kwargs=self.test_publisher_id))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
    
    def test_cannot_send_delete_request_to_endpoint(self):
        response = self.client.delete(reverse('PublisherDetailView', kwargs=self.test_publisher_id))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_patch_request_to_endpoint(self):
        response = self.client.patch(reverse('PublisherDetailView', kwargs=self.test_publisher_id))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
               
class GenreListViewPermissionsTests(TestCase):
    '''
    Unit Tests - Testing the ListView API endpoints, check that the various HTTP request methods return expected response codes
    '''
    def test_can_send_get_request_to_endpoint(self):
        response = self.client.get(reverse('GenreListView'))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_head_request_to_endpoint(self):
        response = self.client.head(reverse('GenreListView'))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_options_request_to_endpoint(self):
        response = self.client.options(reverse('GenreListView'))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_cannot_send_put_request_to_endpoint(self):
        response = self.client.put(reverse('GenreListView'))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_post_request_to_endpoint(self):
        response = self.client.post(reverse('GenreListView'))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
    
    def test_cannot_send_delete_request_to_endpoint(self):
        response = self.client.delete(reverse('GenreListView'))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_patch_request_to_endpoint(self):
        response = self.client.patch(reverse('GenreListView'))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
       
class GenreDetailViewPermissionTests(TestCase):
    '''
    Unit Tests - Testing the DetailView API endpoints, check that the various HTTP request methods return expected response codes
    '''
    def setUp(self):
        # for these tests, we'll need a test dosgame in the database
        self.test_genre = create_test_genre()
        self.test_genre_id = {'slug': self.test_genre.slug}

    def test_can_send_get_request_to_endpoint(self):
        response = self.client.get(reverse('GenreDetailView', kwargs=self.test_genre_id))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_head_request_to_endpoint(self):
        response = self.client.head(reverse('GenreDetailView', kwargs=self.test_genre_id))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_options_request_to_endpoint(self):
        response = self.client.options(reverse('GenreDetailView', kwargs=self.test_genre_id))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_cannot_send_put_request_to_endpoint(self):
        response = self.client.put(reverse('GenreDetailView', kwargs=self.test_genre_id))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_post_request_to_endpoint(self):
        response = self.client.post(reverse('GenreDetailView', kwargs=self.test_genre_id))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
    
    def test_cannot_send_delete_request_to_endpoint(self):
        response = self.client.delete(reverse('GenreDetailView', kwargs=self.test_genre_id))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_patch_request_to_endpoint(self):
        response = self.client.patch(reverse('GenreDetailView', kwargs=self.test_genre_id))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
               