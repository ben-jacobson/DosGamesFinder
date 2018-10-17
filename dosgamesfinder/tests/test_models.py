from django.test import TestCase
from .base import create_test_publisher, create_test_screenshot, create_test_dosgame, create_breaker_string#, create_test_game_and_publisher_package
from dosgamesfinder.models import Publisher, DosGame, Screenshot

from django.core.exceptions import ValidationError
from django.db import IntegrityError, DataError

class ModelTests(TestCase): 
    def test_create_publisher(self):
        '''
        Unit Test - Ensure that publisher objects are being saved to the db. 
        '''        
        test_publisher = create_test_publisher()
        self.assertIn(test_publisher, [p for p in Publisher.objects.all()])
        self.assertEquals(test_publisher.name, Publisher.objects.get(name=test_publisher.name).name)

    def test_create_dosgame(self):
        '''
        Unit Test - Ensure that dosgame objects are being saved to the db. 
        '''             
        test_publisher = create_test_publisher() # can't create a game without assigning a publisher
        test_dosgame = create_test_dosgame(publisher=test_publisher)
        self.assertEquals(test_dosgame, DosGame.objects.get(title=test_dosgame.title))

    def test_create_screenshot(self):
        '''
        Unit Test - Ensure that screenshot objects are being saved to the db. 
        '''             
        test_publisher = create_test_publisher() # can't create a game without assigning a publisher
        test_dosgame = create_test_dosgame(publisher=test_publisher)
        test_screenshot = create_test_screenshot(game=test_dosgame)
        self.assertEquals([test_screenshot], [s for s in Screenshot.objects.all()])

    def test_cannot_create_game_without_publisher(self):
        '''
        Unit Test - Ensure that you aren't able to create game objects without a publisher. 
        '''        
        # attempt to create a game without a publisher. Can't use helper function, since that function does it correctly
        test_dosgame = DosGame(
            title="The game with no publisher",
            genre="Puzzle",
            description="This game has no publisher. Was it ever released? Did it even get made? ",
            date_releated=1991,
            user_rating=1,
        )

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_dosgame.full_clean()

        with self.assertRaises(IntegrityError): 
            test_dosgame.save()

    def test_cannot_create_screenshot_without_game(self):
        '''
        Unit Test - Ensure that you aren't able to create screenshot objects without games. 
        '''
        # attempt to create a screenshot without a game. Can't use helper function, since that function does it correctly
        test_screenshot = Screenshot(
            img_src='https://via.placeholder.com/320x200',
            img_width=320,
            img_height=200,
        )

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_screenshot.full_clean()

        with self.assertRaises(IntegrityError): 
            test_screenshot.save()


    def test_many_to_one_relationship_between_game_and_screenshot(self):
        '''
        Unit Test - Create a game, assign it some screenshots, check that the db relationships work as expected. 
        '''
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
        '''
        Unit Test - Create a publisher, assign it a game, check that the db relationships work as expected. 
        '''
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
        Unit Test - Check that default ordering of all game items is A-Z
        '''
        test_publisher = create_test_publisher()
        a = create_test_dosgame(publisher=test_publisher, title='a')
        b = create_test_dosgame(publisher=test_publisher, title='b')
        c = create_test_dosgame(publisher=test_publisher, title='c')
        
        test_db_ordering = DosGame.objects.all()
        self.assertEqual([a, b, c], [g for g in test_db_ordering])

    def test_default_ordering_of_publishers(self):
        '''
        Unit Test - check that default ordering of all publishers is A-Z
        '''
        a = create_test_publisher(name='a')
        b = create_test_publisher(name='b')
        c = create_test_publisher(name='c')
        
        test_db_ordering = Publisher.objects.all()
        self.assertEqual([a, b, c], [g for g in test_db_ordering])

    def test_max_length_of_publisher_fields(self):
        '''
        Unit Test - This test knows the minimum and maximum length of the publisher field and tests that assertions are being raised correctly
        '''

        # check that the right assertions are being raised
        with self.assertRaises(DataError): 
            create_test_publisher(name=create_breaker_string(129))

    def test_max_length_of_dosgame_fields(self):
        '''
        Unit Test - This test knows the minimum and maximum length of the dosgame field and tests that assertions are being raised correctly
        '''
        # start by creating a big string likely to break the limits of the model. In this case 256 characters long will be sufficient
        test_breaker_string = create_breaker_string(256)

        # Test the dosgame.title length
        with self.assertRaises(DataError): 
            create_test_dosgame(publisher=create_test_publisher(), title=test_breaker_string, genre=test_breaker_string)

    def test_max_length_of_screenshot_fields(self):
        '''
        Unit Test - This test knows the minimum and maximum length of the screenshot fields and tests that assertions are being raised correctly
        '''
        # start by creating a big string likely to break the limits of the model. In this case 256 characters long will be sufficient
        test_breaker_string = create_breaker_string(256)
        test_publisher = create_test_publisher()
        test_dosgame = create_test_dosgame(publisher=test_publisher)

        # Test the dosgame.title length
        with self.assertRaises(DataError): 
            create_test_screenshot(game=test_dosgame, img_src=test_breaker_string)

    def test_publisher_name_is_unique(self):
        '''
        Unit Test - Ensure that the publishers name is unique in the database
        '''
        # create and save the first publisher
        create_test_publisher(name='test')
        
        # does it raise an Integrity error? 
        with self.assertRaises(IntegrityError): 
            create_test_publisher(name='test')

    def test_publisher_returns_name_string(self):
        '''
        Unit Test - Ensure that the publisher returns it's name when calling the models name() method
        '''
        pass

    def test_dosgame_returns_name_string(self):
        '''
        Unit Test - Ensure that the dosgame returns it's name when calling the models name() method
        '''
        pass

    def test_screenshot_return_src_string(self):
        '''
        Unit Test - Ensure that the screenshot returns it's src when calling the models name() method
        '''
        pass