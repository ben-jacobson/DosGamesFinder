from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.conf import settings

from .base import create_test_publisher, create_test_genre, create_test_dosgame, create_test_screenshot, create_test_download_location, test_objects_mixin

from dosgamesfinder.views import MAX_DOSGAME_RESULTS_LISTVIEW, MAX_PUBLISHER_RESULTS_LISTVIEW

HTTP_OK = 200
HTTP_NOT_ALLOWED = 405
HTTP_NOT_FOUND = 404

class LayoutAndStylingTest(TestCase):
    def test_static_files_have_been_passed_to_browser(self):
        ''' 
        Unit Test - Test that the JS script tags and CSS href tags have been rendered in the browser 
        '''
        expected_lines = [
            '<link rel="stylesheet" href="/static/css/bootstrap.min.css" />',
            '<link rel="stylesheet" href="/static/css/main.css" />',        
            '<script src="/static/vendor_js/jquery-3.3.1.min.js" type="text/javascript"></script>',
            '<script src="/static/vendor_js/popper.min.js" type="text/javascript"></script>',
            '<script src="/static/vendor_js/bootstrap.min.js" type="text/javascript"></script>',
        ]
        response = self.client.get(reverse('dosgame_listview'))

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

    def test_dosgame_listview_with_genre_filter_returns_list(self):     # test using the optional genre argument
        action_genre = create_test_genre(name='Action')
        shooter_genre = create_test_genre(name='Shooter')

        a = create_test_dosgame(title='abracadabra', publisher=self.test_publisher, genre=action_genre)
        b = create_test_dosgame(title='beetlejuice', publisher=self.test_publisher, genre=shooter_genre)
        c = create_test_dosgame(title='commodore', publisher=self.test_publisher, genre=action_genre)

        response = self.client.get(reverse('DosGamesListView') + '?genre=action') # also tests that our filtering is case insensitive
        self.assertContains(response, a.title)
        self.assertNotContains(response, b.title)
        self.assertContains(response, c.title)

    def test_dosgame_listview_with_publisher_filter_returns_list(self): # test using the optional publisher argument
        test_publisher_one = create_test_publisher(name='Publisher One')
        test_publisher_two = create_test_publisher(name='Publisher Two')
        test_publisher_one_slug = test_publisher_one.slug
        test_publisher_two_slug = test_publisher_two.slug

        action_genre = create_test_genre(name='Action')
        shooter_genre = create_test_genre(name='Shooter')
        action_slug = action_genre.slug
        shooter_slug = shooter_genre.slug

        a = create_test_dosgame(title='abracadabra', publisher=test_publisher_one, genre=action_genre)
        b = create_test_dosgame(title='beetlejuice', publisher=test_publisher_two, genre=action_genre)
        c = create_test_dosgame(title='commodore', publisher=test_publisher_one, genre=shooter_genre)

        # action games from publisher_one should equal A only
        response = self.client.get(reverse('DosGamesListView') + f'?publisher={test_publisher_one_slug}&genre={action_slug}') # also tests that our filtering is case insensitive
        self.assertContains(response, a.title)
        self.assertNotContains(response, b.title)
        self.assertNotContains(response, c.title)

        # action games from publisher_two should equal B only
        response = self.client.get(reverse('DosGamesListView') + f'?publisher={test_publisher_two_slug}&genre={action_slug}') # also tests that our filtering is case insensitive
        self.assertNotContains(response, a.title)
        self.assertContains(response, b.title)
        self.assertNotContains(response, c.title)

        # shooter games from publisher_one should return C only - for the sake of these next two tests, we'll reverse the query string
        response = self.client.get(reverse('DosGamesListView') + f'?genre={shooter_slug}&publisher={test_publisher_one_slug}') # also tests that our filtering is case insensitive
        self.assertNotContains(response, a.title)
        self.assertNotContains(response, b.title)
        self.assertContains(response, c.title)

        # shooter games from publisher_two should return no results
        response = self.client.get(reverse('DosGamesListView') + f'?genre={shooter_slug}&publisher={test_publisher_two_slug}') # also tests that our filtering is case insensitive
        self.assertNotContains(response, a.title)
        self.assertNotContains(response, b.title)
        self.assertNotContains(response, c.title)

    def test_dosgame_listview_with_publisher_and_genre_filter_returns_list(self):   # test using both of the optional publisher and genre filters + test the opposite direction
        test_publisher_one = create_test_publisher(name='Publisher One')
        test_publisher_two = create_test_publisher(name='Publisher Two')
        test_pub_slug = test_publisher_one.slug

        a = create_test_dosgame(title='abracadabra', publisher=test_publisher_one, genre=self.test_genre)
        b = create_test_dosgame(title='beetlejuice', publisher=test_publisher_two, genre=self.test_genre)
        c = create_test_dosgame(title='commodore', publisher=test_publisher_one, genre=self.test_genre)

        response = self.client.get(reverse('DosGamesListView') + f'?publisher={test_pub_slug}') 
        self.assertContains(response, a.title)
        self.assertNotContains(response, b.title)
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
       
class DosGameDetailViewPermissionTests(test_objects_mixin, TestCase):
    '''
    Unit Tests - Testing the DetailView API endpoints, check that the various HTTP request methods return expected response codes
    '''
    def test_cannot_access_dosgame_detailview_via_pk(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse('DosGamesDetailView', kwargs={'pk': self.test_dosgame.id}))

    def test_can_send_get_request_to_endpoint(self):
        response = self.client.get(reverse('DosGamesDetailView', kwargs=self.test_dosgame_slug))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_head_request_to_endpoint(self):
        response = self.client.head(reverse('DosGamesDetailView', kwargs=self.test_dosgame_slug))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_options_request_to_endpoint(self):
        response = self.client.options(reverse('DosGamesDetailView', kwargs=self.test_dosgame_slug))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_cannot_send_put_request_to_endpoint(self):
        response = self.client.put(reverse('DosGamesDetailView', kwargs=self.test_dosgame_slug))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_post_request_to_endpoint(self):
        response = self.client.post(reverse('DosGamesDetailView', kwargs=self.test_dosgame_slug))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
    
    def test_cannot_send_delete_request_to_endpoint(self):
        response = self.client.delete(reverse('DosGamesDetailView', kwargs=self.test_dosgame_slug))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_patch_request_to_endpoint(self):
        response = self.client.patch(reverse('DosGamesDetailView', kwargs=self.test_dosgame_slug))
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
       
class PublisherDetailViewPermissionTests(test_objects_mixin, TestCase):
    '''
    Unit Tests - Testing the DetailView API endpoints, check that the various HTTP request methods return expected response codes
    '''
    def test_cannot_access_publisher_detailview_via_pk(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse('PublisherDetailView', kwargs={'pk': self.test_publisher.id}))

    def test_can_send_get_request_to_endpoint(self):
        response = self.client.get(reverse('PublisherDetailView', kwargs=self.test_publisher_slug))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_head_request_to_endpoint(self):
        response = self.client.head(reverse('PublisherDetailView', kwargs=self.test_publisher_slug))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_options_request_to_endpoint(self):
        response = self.client.options(reverse('PublisherDetailView', kwargs=self.test_publisher_slug))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_cannot_send_put_request_to_endpoint(self):
        response = self.client.put(reverse('PublisherDetailView', kwargs=self.test_publisher_slug))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_post_request_to_endpoint(self):
        response = self.client.post(reverse('PublisherDetailView', kwargs=self.test_publisher_slug))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
    
    def test_cannot_send_delete_request_to_endpoint(self):
        response = self.client.delete(reverse('PublisherDetailView', kwargs=self.test_publisher_slug))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_patch_request_to_endpoint(self):
        response = self.client.patch(reverse('PublisherDetailView', kwargs=self.test_publisher_slug))
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
       
class GenreDetailViewPermissionTests(test_objects_mixin, TestCase):
    '''
    Unit Tests - Testing the DetailView API endpoints, check that the various HTTP request methods return expected response codes
    '''
    def test_cannot_access_genre_detailview_via_pk(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse('GenreDetailView', kwargs={'pk': self.test_genre.id}))

    def test_can_send_get_request_to_endpoint(self):
        response = self.client.get(reverse('GenreDetailView', kwargs=self.test_genre_slug))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_head_request_to_endpoint(self):
        response = self.client.head(reverse('GenreDetailView', kwargs=self.test_genre_slug))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_can_send_options_request_to_endpoint(self):
        response = self.client.options(reverse('GenreDetailView', kwargs=self.test_genre_slug))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_cannot_send_put_request_to_endpoint(self):
        response = self.client.put(reverse('GenreDetailView', kwargs=self.test_genre_slug))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_post_request_to_endpoint(self):
        response = self.client.post(reverse('GenreDetailView', kwargs=self.test_genre_slug))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
    
    def test_cannot_send_delete_request_to_endpoint(self):
        response = self.client.delete(reverse('GenreDetailView', kwargs=self.test_genre_slug))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)

    def test_cannot_send_patch_request_to_endpoint(self):
        response = self.client.patch(reverse('GenreDetailView', kwargs=self.test_genre_slug))
        self.assertEqual(response.status_code, HTTP_NOT_ALLOWED)
               
class DosGamesListViewTests(test_objects_mixin, TestCase):
    def test_response_code(self):
        response = self.client.get(reverse('dosgame_listview'))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_view_uses_template(self):
        response = self.client.get(reverse('dosgame_listview'))
        self.assertTemplateUsed(response, 'dosgame_listview.html')        

    def test_context_object_list_is_passed_to_template(self):
        response = self.client.get(reverse('dosgame_listview'))
        # test that page title appears in context         
        self.assertEqual(response.context['page_title'], 'Games List A-Z') 
        # test that the dosgames_list context objects appears and contains our test game
        self.assertIn(self.test_dosgame, response.context['dosgames_list'])   

    def test_query_set_returns_paginated_results(self):
        # we already have one test object, for this test, we'll create another 30, so as to test that pagination only returns the first 18 results. 
        for i in range(30):
            create_test_dosgame(title=str(i), publisher=self.test_publisher, genre=self.test_genre)

        response = self.client.get(reverse('dosgame_listview'))
        results_on_page = len(response.context['dosgames_list'])
        self.assertEqual(results_on_page, MAX_DOSGAME_RESULTS_LISTVIEW)

    def test_dosgame_list_rendered(self):
        # we already have one test object, for this test, we'll create another 2, so as to test that pagination only returns the first 18 results. 
        for i in range(2):
            create_test_dosgame(title=str(i), publisher=self.test_publisher, genre=self.test_genre)

        response = self.client.get(reverse('dosgame_listview'))
        self.assertContains(response, '0')    
        self.assertContains(response, '1')        
        self.assertContains(response, 'FooBar Adventures')        

    def test_listview_pagination_renders(self):
        pagination_string = '<nav aria-label="Page Numbers">'

        # first test how the page renders with only a few items, not enough to exceed MAX_DOSGAME_RESULTS_LISTVIEW
        response = self.client.get(reverse('dosgame_listview'))
        self.assertNotContains(response, pagination_string)        

        # pagination only needs to appear when the amount of results exceed MAX_DOSGAME_RESULTS_LISTVIEW
        for i in range(40):
            create_test_dosgame(title=str(i), publisher=self.test_publisher, genre=self.test_genre)

        response = self.client.get(reverse('dosgame_listview'))
        self.assertContains(response, pagination_string)        


class DosGamesDetailViewTests(test_objects_mixin, TestCase):
    def test_response_code(self):
        test_slug = self.test_dosgame.slug
        response = self.client.get(reverse('dosgame_detailview', kwargs={'slug': test_slug}))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_view_uses_template(self):
        test_slug = self.test_dosgame.slug
        response = self.client.get(reverse('dosgame_detailview', kwargs={'slug': test_slug}))
        self.assertTemplateUsed(response, 'dosgame_detailview.html') 

    def test_context_object_list_is_passed_to_template(self):
        test_slug = self.test_dosgame.slug
        response = self.client.get(reverse('dosgame_detailview', kwargs={'slug': test_slug}))
        # test that the context objects appears and contains our test game
        self.assertEqual(self.test_dosgame, response.context['dosgame'])   

    def test_message_rendered_when_no_download_locations(self):
        test_slug = self.test_dosgame.slug
        response = self.client.get(reverse('dosgame_detailview', kwargs={'slug': test_slug}))
        self.assertContains(response, "Sorry, we don't have links for this game yet. Please check back later.")        

    def test_download_locations_rendered(self):
        test_slug = self.test_dosgame.slug
        test_download_location = create_test_download_location(game=self.test_dosgame)
        response = self.client.get(reverse('dosgame_detailview', kwargs={'slug': test_slug}))
        self.assertContains(response, f'<a href=\'{settings.MEDIA_URL}{test_download_location.href}')     

    def test_thumbnail_rendered_when_no_screenshots(self):
        test_slug = self.test_dosgame.slug
        response = self.client.get(reverse('dosgame_detailview', kwargs={'slug': test_slug}))
        self.assertContains(response, f'{self.test_dosgame.title} screenshot')
        self.assertContains(response, f'src="{settings.MEDIA_URL}{self.test_dosgame.thumbnail_src}')     

    def test_screenshot_rendering(self):
        test_slug = self.test_dosgame.slug
        create_test_screenshot(game=self.test_dosgame)
        response = self.client.get(reverse('dosgame_detailview', kwargs={'slug': test_slug}))
        self.assertContains(response, f'{self.test_dosgame.title} screenshot')
        screenshot_src = self.test_dosgame.screenshots.all().first()
        self.assertContains(response, f'src="{settings.MEDIA_URL}{screenshot_src}')     

class PublisherListViewTests(test_objects_mixin, TestCase):
    def test_response_code(self):
        response = self.client.get(reverse('publisher_listview'))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_view_uses_template(self):
        response = self.client.get(reverse('publisher_listview'))
        self.assertTemplateUsed(response, 'publisher_listview.html') 

    def test_context_object_list_is_passed_to_template(self):
        response = self.client.get(reverse('publisher_listview'))
        # test that the publisher context objects appears and contains our test publisher
        self.assertIn(self.test_publisher, response.context['publishers'])   

    def test_query_set_returns_paginated_results(self):
        # we already have one test object, for this test, we'll create another 30, so as to test that pagination only returns the first 10 results or so. 
        for i in range(30):
            create_test_publisher(name=str(i))

        response = self.client.get(reverse('publisher_listview'))
        results_on_page = len(response.context['publishers'])
        self.assertEqual(results_on_page, MAX_PUBLISHER_RESULTS_LISTVIEW)        

    def test_publisher_list_rendered(self):
        # we already have one test object, for this test, we'll create another 30, so as to test that pagination only returns the first 10 results or so. 
        for i in range(5):
            create_test_publisher(name=str(i))

        response = self.client.get(reverse('publisher_listview'))
        self.assertContains(response, 'Test Software')

        for i in range(5):
            self.assertContains(response, str(i))
