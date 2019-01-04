from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from .base import create_test_publisher, create_test_genre, create_test_dosgame, create_test_screenshot, create_test_download_location, test_objects_mixin

from dosgamesfinder.views import MAX_DOSGAME_RESULTS_LISTVIEW, MAX_PUBLISHER_RESULTS_LISTVIEW

HTTP_OK = 200
HTTP_NOT_ALLOWED = 405
HTTP_NOT_FOUND = 404

class LayoutAndStylingTest(test_objects_mixin, TestCase):
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

    def test_context_processor_returns_genre_for_dropdown_menu(self):
        response = self.client.get(reverse('dosgame_listview'))
        self.assertContains(response, self.test_genre.name)
             
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

    def test_listview_genre_filtering(self):
        test_genre_one = create_test_genre(name='Shooter')
        test_genre_two = create_test_genre(name='Beat Em Up')
        test_shooter_game_one = create_test_dosgame(publisher=self.test_publisher, genre=test_genre_one, title='Shooter game A')
        test_shooter_game_two = create_test_dosgame(publisher=self.test_publisher, genre=test_genre_one, title='Shooter game B')
        test_beatemup_game_one = create_test_dosgame(publisher=self.test_publisher, genre=test_genre_two, title='Beat em up game A')
        test_beatemup_game_two = create_test_dosgame(publisher=self.test_publisher, genre=test_genre_two, title='Beat em up game B')

        response = self.client.get(reverse('genre_filter', kwargs={'slug': test_genre_one.slug}))
        self.assertContains(response, test_shooter_game_one.title)
        self.assertContains(response, test_shooter_game_two.title)
        self.assertNotContains(response, test_beatemup_game_one.title)
        self.assertNotContains(response, test_beatemup_game_two.title)

        response = self.client.get(reverse('genre_filter', kwargs={'slug': test_genre_two.slug}))
        self.assertNotContains(response, test_shooter_game_one.title)
        self.assertNotContains(response, test_shooter_game_two.title)
        self.assertContains(response, test_beatemup_game_one.title)
        self.assertContains(response, test_beatemup_game_two.title)

    def test_listview_publisher_filtering(self):
        test_publisher_one = create_test_publisher(name='Pub One')
        test_publisher_two = create_test_publisher(name='Pub Two')
        test_pubone_game_one = create_test_dosgame(publisher=test_publisher_one, genre=self.test_genre, title='Game A')
        test_pubone_game_two = create_test_dosgame(publisher=test_publisher_one, genre=self.test_genre, title='Game B')
        test_pubtwo_game_one = create_test_dosgame(publisher=test_publisher_two, genre=self.test_genre, title='Game C')
        test_pubtwo_game_two = create_test_dosgame(publisher=test_publisher_two, genre=self.test_genre, title='Game D')

        response = self.client.get(reverse('publisher_filter', kwargs={'slug': test_publisher_one.slug}))
        self.assertContains(response, test_pubone_game_one.title)
        self.assertContains(response, test_pubone_game_two.title)
        self.assertNotContains(response, test_pubtwo_game_one.title)
        self.assertNotContains(response, test_pubtwo_game_two.title)

        response = self.client.get(reverse('publisher_filter', kwargs={'slug': test_publisher_two.slug}))
        self.assertNotContains(response, test_pubone_game_one.title)
        self.assertNotContains(response, test_pubone_game_two.title)
        self.assertContains(response, test_pubtwo_game_one.title)
        self.assertContains(response, test_pubtwo_game_two.title)

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

class SearchBarTests(test_objects_mixin, TestCase):
    # the search bar view makes use of the dosgame listview, there are only a small number of tests here so as to not duplicate any existing tests
    def test_response_code(self):
        response = self.client.get(reverse('search_listview', kwargs={'query': 'FooBar'}))
        self.assertEqual(response.status_code, HTTP_OK)

    def test_view_uses_template(self):
        response = self.client.get(reverse('search_listview', kwargs={'query': 'FooBar'}))
        self.assertTemplateUsed(response, 'dosgame_listview.html')     

    def test_search_results(self):
        # create a few additional games to test that search results are working correctly
        response = self.client.get(reverse('search_listview', kwargs={'query': 'FooBar'}))
        self.assertContains(response, self.test_dosgame.title)
        self.fail('finish the test')

    def test_search_results_provides_no_results_message(self):
        self.fail('finish the test')

    def test_context_object_list_is_passed_to_template(self):
        #response = self.client.get(reverse('publisher_listview'))
        # test that the publisher context objects appears and contains our test publisher
        #self.assertIn(self.test_publisher, response.context['publishers']) 
        self.fail('finish the test') 

    def test_query_set_returns_paginated_results(self):
        # we already have one test object, for this test, we'll create another 30, so as to test that pagination only returns the first 10 results or so. 
        #for i in range(30):
        #    create_test_publisher(name=str(i))

        #response = self.client.get(reverse('publisher_listview'))
        #results_on_page = len(response.context['publishers'])
        #self.assertEqual(results_on_page, MAX_PUBLISHER_RESULTS_LISTVIEW)       
        self.fail('finish the test')