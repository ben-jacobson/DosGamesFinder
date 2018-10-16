from django.test import TestCase
from .base import create_test_publisher, create_test_screenshot, create_test_dosgame
from dosgamesfinder.models import Publisher, DosGame, Screenshot

class ModelTests(TestCase): 
    def test_create_publisher(self):
        test_publisher = create_test_publisher()
        self.assertIn(test_publisher, [p for p in Publisher.objects.all()])
        self.assertEquals(test_publisher.name, Publisher.objects.get(name=test_publisher.name).name)

    def test_create_dosgame(self):
        test_publisher = create_test_publisher() # can't create a game without assigning a publisher
        test_dosgame = create_test_dosgame(publisher=test_publisher)
        self.assertEquals(test_dosgame, DosGame.objects.get(title=test_dosgame.title))

    def test_create_screenshot(self):
        test_publisher = create_test_publisher() # can't create a game without assigning a publisher
        test_dosgame = create_test_dosgame(publisher=test_publisher)
        test_screenshot = create_test_screenshot(game=test_dosgame)
        self.assertEquals([test_screenshot], [s for s in Screenshot.objects.all()])

    def test_cannot_create_game_without_publisher(self):
        pass

    def test_cannot_create_screenshot_without_game(self):
        pass

    def test_many_to_one_relationship_between_game_and_screenshot(self):
        # create a publisher and a game
        test_publisher = create_test_publisher()
        test_dosgame = create_test_dosgame(publisher=test_publisher)

        # create two screenshots for the game
        screenshot1 = create_test_screenshot(game=test_dosgame)
        screenshot2 = create_test_screenshot(game=test_dosgame)

        # and then test
        test_dosgame_db = DosGame.objects.get(title=test_dosgame.title)
        test_set_of_screenshots = test_dosgame_db.screenshot_set.all()
        self.assertEquals([screenshot2, screenshot1], [s for s in test_set_of_screenshots])

    def test_many_to_one_relationship_between_game_and_publisher(self):
        # create a publisher and a game
        test_publisher = create_test_publisher()
        test_dosgame = create_test_dosgame(publisher=test_publisher)

        # create two screenshots for the game
        create_test_screenshot(game=test_dosgame)
        create_test_screenshot(game=test_dosgame)

        # and then test
        self.assertIn(test_dosgame, Publisher.objects.get(name=test_publisher.name).dosgame_set.all()
)                   
    def test_default_ordering_of_games(self):
        '''
        Test that default ordering of all game items is A-Z
        '''
        pass
    
    def test_default_ordering_of_publishers(self):
        '''
        Test that default ordering of all publishers is A-Z
        '''
        pass

    def test_min_max_of_fields(self):
        '''
        This test knows the minimum and maximum length of each field and tests
        '''
        pass

    def test_publisher_name_unique(self):
        pass
    
    def test_game_name_unique(self):
        pass

