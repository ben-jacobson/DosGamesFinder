from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from datetime import datetime
#from django.utils import timezone
from dosgamesfinder.tests.base import create_test_publisher, create_test_genre, create_test_dosgame, create_test_screenshot, create_test_download_location
#from time import sleep

MAX_WAIT = 10 # 10 second max wait

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(MAX_WAIT)
        self.browser.set_page_load_timeout(MAX_WAIT)

        # create 2 test genres
        self.test_action_genre = create_test_genre(name='action')
        self.test_adventure_genre = create_test_genre(name='adventure')

        # create 2 test publishers
        self.test_publisher_test_soft = create_test_publisher(name='Test Soft Inc')
        self.test_publisher_foobar_games = create_test_publisher(name='Foo Bar Entertainment')
              
        # create 6 test dosgames.
        self.test_dosgame_a = create_test_dosgame(title='Abracadabra', publisher=self.test_publisher_test_soft, genre=self.test_action_genre)
        self.test_dosgame_b = create_test_dosgame(title='Beetlejuice', publisher=self.test_publisher_test_soft, genre=self.test_action_genre)
        self.test_dosgame_c = create_test_dosgame(title='Commandant Ki', publisher=self.test_publisher_test_soft, genre=self.test_adventure_genre)
        self.test_dosgame_d = create_test_dosgame(title='Dodecahedron', publisher=self.test_publisher_foobar_games, genre=self.test_adventure_genre)
        self.test_dosgame_e = create_test_dosgame(title='Explorer Dora', publisher=self.test_publisher_foobar_games, genre=self.test_action_genre)
        self.test_dosgame_f = create_test_dosgame(title='Fortune Finder', publisher=self.test_publisher_foobar_games, genre=self.test_action_genre)

        # create a test screenshot for each game
        self.test_screenshot_a = create_test_screenshot(game=self.test_dosgame_a)
        self.test_screenshot_b = create_test_screenshot(game=self.test_dosgame_b)
        self.test_screenshot_c = create_test_screenshot(game=self.test_dosgame_c)
        self.test_screenshot_d = create_test_screenshot(game=self.test_dosgame_d)
        self.test_screenshot_e = create_test_screenshot(game=self.test_dosgame_e)
        self.test_screenshot_f = create_test_screenshot(game=self.test_dosgame_f)

        # create a test download location for each game
        self.test_download_location_a = create_test_download_location(game=self.test_dosgame_a)
        self.test_download_location_b = create_test_download_location(game=self.test_dosgame_b)
        self.test_download_location_c = create_test_download_location(game=self.test_dosgame_c)        
        self.test_download_location_d = create_test_download_location(game=self.test_dosgame_d)
        self.test_download_location_e = create_test_download_location(game=self.test_dosgame_e)
        self.test_download_location_f = create_test_download_location(game=self.test_dosgame_f)

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # user visits the home page
        self.browser.get(self.live_server_url)

        # user notices that there are rows of game cards, 3 columns to the row
        game_cards_row = self.browser.find_element_by_class_name('games-list-row')
        self.assertEqual(3, len(game_cards_row.find_elements_by_class_name('game-listview')))

class HomePageTests(FunctionalTest):
    def test_visit_home_page_and_test_genre_dropdown(self):
        # ensure that the genre dropdown menu works
        self.fail('finish the test')

    def test_visit_home_page_and_visit_game_page(self):
        # ensure that you can click on a game from the home page

        # check that you can click the link
        # check that you can click on the image
        self.fail('finish the test')

    def test_game_card_links_to_genre(self):
        # ensure that the game cards have working link to a genre filter from the home page
        self.fail('finish the test')

    def test_game_card_links_to_publisher_filter(self):
        # ensure that the game cards have working link to a publisher filter from the home page
        self.fail('finish the test')

    def test_visit_home_page_pagination(self):
        # check that you can click on next page
        # check that you can click on a page number
        # check that you can click on prev page 
        self.fail('finish the test')

    def test_visit_home_page_and_visit_publisher_page(self):
        # does the right title appear? 
        # do the right publishers appear?
        self.fail('finish the test')
    
    def test_visit_home_page_and_filter_by_genre(self):
        # does the right title appear
        # do the right games appear? 
        self.fail('finish the test')

class GamePageTests(FunctionalTest):
    def test_visit_game_page_and_test_screenshots(self): 
        # when you visit a game page directly, do the screenshots appear? 
        self.fail('finish the test')

    def test_visit_game_page_and_download_game(self): 
        # when you visit a game page directly, do download_links_appear? 
        self.fail('finish the test')

    def test_visit_game_page_logo_and_all_games_returns_to_homepage(self):
        # when on a game page, can you click on game logo and go back to home page?
        # when on a game page, can you click on 'all games'
        self.fail('finish the test')

class PublisherPageTests(FunctionalTest):
    def test_visit_publisher_page_and_select_a_publisher_filter(self):
        # visit publisher page, click a publisher, do the right games appear? 
        self.fail('finish the test')
