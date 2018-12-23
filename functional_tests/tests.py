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
        self.fail('finish the test')