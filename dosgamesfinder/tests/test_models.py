from django.test import TestCase
from .base import create_test_publisher, create_test_screenshot, create_test_dosgame, create_test_download_location, create_breaker_string#, create_test_game_and_publisher_package
from dosgamesfinder.models import Publisher, DosGame, Screenshot, DownloadLocation

from django.core.exceptions import ValidationError
from django.db import IntegrityError, DataError

class DosGameModelTests(TestCase): 
    def test_create_dosgame(self):
        '''
        Unit Test - Ensure that dosgame objects are being saved to the db. 
        '''             
        test_publisher = create_test_publisher() # can't create a game without assigning a publisher
        test_dosgame = create_test_dosgame(publisher=test_publisher)
        self.assertEquals(test_dosgame, DosGame.objects.get(title=test_dosgame.title))

    def test_max_length_of_dosgame_fields(self):
        '''
        Unit Test - This test knows the minimum and maximum length of the dosgame field and tests that assertions are being raised correctly
        '''
        # start by creating a big string likely to break the limits of the model. In this case 256 characters long will be sufficient
        test_breaker_string = create_breaker_string(256)

        # Test the dosgame.title length
        with self.assertRaises(DataError): 
            create_test_dosgame(publisher=create_test_publisher(), title=test_breaker_string, genre=test_breaker_string)

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

    def test_name_method_returns_dosgame_name(self):
        '''
        Unit Test - Ensure that the dosgame returns it's name when calling the models __str__() method
        '''
        test_name = 'Adventures in Testingville'
        test_dosgame = create_test_dosgame(publisher=create_test_publisher(), title=test_name)
        self.assertEqual(test_name, test_dosgame.__str__())

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
        test_set_of_screenshots = test_dosgame_db.screenshots.all()
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
        self.assertIn(test_dosgame, Publisher.objects.get(name=test_publisher.name).dosgame_set.all())     

    def test_many_to_one_relationship_between_game_and_download_location(self):
        '''
        Unit Test - Create a game, assign it some download locations, check that the db relationships work as expected. 
        '''
        # create a publisher and a game
        test_publisher = create_test_publisher()
        test_dosgame = create_test_dosgame(publisher=test_publisher)

        # create two download locations for the game
        download1 = create_test_download_location(game=test_dosgame)
        download2 = create_test_download_location(game=test_dosgame)

        # and then test
        test_dosgame_db = DosGame.objects.get(title=test_dosgame.title)
        test_set_of_download_locations = test_dosgame_db.download_locations.all()
        self.assertEquals([download2, download1], [d for d in test_set_of_download_locations])

class ScreenshotModelTests(TestCase):
    def test_create_screenshot(self):
        '''
        Unit Test - Ensure that screenshot objects are being saved to the db. 
        '''             
        test_publisher = create_test_publisher() # can't create a game without assigning a publisher
        test_dosgame = create_test_dosgame(publisher=test_publisher)
        test_screenshot = create_test_screenshot(game=test_dosgame)
        self.assertEquals([test_screenshot], [s for s in Screenshot.objects.all()])

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

    def test_name_method_returns_screenshot_src(self):
        '''
        Unit Test - Ensure that the screenshot returns it's src when calling the models __str__() method
        '''
        test_img_src = 'https://via.placeholder.com/320x200'
        test_dosgame = create_test_dosgame(publisher=create_test_publisher())
        test_screenshot = create_test_screenshot(game=test_dosgame, img_src=test_img_src)
        self.assertEqual(test_img_src, test_screenshot.__str__())

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

class PublisherModelTests(TestCase):
    def test_create_publisher(self):
        '''
        Unit Test - Ensure that publisher objects are being saved to the db. 
        '''        
        test_publisher = create_test_publisher()
        self.assertIn(test_publisher, [p for p in Publisher.objects.all()])
        self.assertEquals(test_publisher.name, Publisher.objects.get(name=test_publisher.name).name)

    def test_max_length_of_publisher_fields(self):
        '''
        Unit Test - This test knows the minimum and maximum length of the publisher field and tests that assertions are being raised correctly
        '''

        # check that the right assertions are being raised
        with self.assertRaises(DataError): 
            create_test_publisher(name=create_breaker_string(129))

    def test_default_ordering_of_publishers(self):
        '''
        Unit Test - check that default ordering of all publishers is A-Z
        '''
        a = create_test_publisher(name='a')
        b = create_test_publisher(name='b')
        c = create_test_publisher(name='c')
        
        test_db_ordering = Publisher.objects.all()
        self.assertEqual([a, b, c], [g for g in test_db_ordering])

    def test_name_method_returns_publisher_name(self):
        '''
        Unit Test - Ensure that the publisher returns it's name when calling the models name() method
        '''
        test_name = 'Test Software'
        test_publisher = create_test_publisher(name=test_name)
        self.assertEqual(test_name, test_publisher.__str__())

    def test_publisher_name_is_unique(self):
        '''
        Unit Test - Ensure that the publishers name is unique in the database
        '''
        # create and save the first publisher
        create_test_publisher(name='test')
        
        # does it raise an Integrity error? 
        with self.assertRaises(IntegrityError): 
            create_test_publisher(name='test')

class DownloadLocationModelTests(TestCase):
    def test_create_download_location(self):
        '''
        Unit Test - Ensure that download location objects are being saved to the db. 
        '''             
        test_publisher = create_test_publisher() # can't create a game without assigning a publisher
        test_dosgame = create_test_dosgame(publisher=test_publisher)
        test_download_location = create_test_download_location(game=test_dosgame)
        self.assertEquals([test_download_location], [s for s in DownloadLocation.objects.all()])

    def test_max_length_of_download_location_href(self):
        '''
        Unit Test - This test knows the minimum and maximum length of the screenshot fields and tests that assertions are being raised correctly
        '''
        # start by creating a big string likely to break the limits of the model. In this case 256 characters long will be sufficient
        test_breaker_string = create_breaker_string(128)
        test_publisher = create_test_publisher()
        test_dosgame = create_test_dosgame(publisher=test_publisher)

        # Test the dosgame.title length
        with self.assertRaises(DataError): 
            create_test_download_location(game=test_dosgame, href=test_breaker_string)
    
    def test_default_ordering_of_download_locations(self):
        '''
        Unit Test - Check that default ordering of all download locations is A-Z
        '''
        test_dosgame = create_test_dosgame(publisher=create_test_publisher())
        a = create_test_download_location(game=test_dosgame, name='a')
        b = create_test_download_location(game=test_dosgame, name='b')
        c = create_test_download_location(game=test_dosgame, name='c')
        
        test_db_ordering = DownloadLocation.objects.all()
        self.assertEqual([a, b, c], [d for d in test_db_ordering])

    def test_name_method_returns_download_location_name(self):
        '''
        Unit Test - Ensure that the download location returns it's src when calling the models __str__() method
        '''
        test_download_location_name = 'GOG'
        test_dosgame = create_test_dosgame(publisher=create_test_publisher())
        test_download_location = create_test_download_location(game=test_dosgame, name=test_download_location_name)
        self.assertEqual(test_download_location_name, test_download_location.__str__())

    '''def test_unicode_method_returns_serialized_object(self):
        '/''
        Unit Test - In our app, we're using REST API serializers which rely on the model __unicode__ method to return a representation of the object
        '/''
        test_href = 'asdf'
        test_name = 'asdfasdf'

        test_game = create_test_dosgame(publisher=create_test_publisher())
        test_download_location = create_test_download_location(game=test_game, href=test_href, name=test_name)
        test_expected_output = {
            'href': test_href,
            'name': test_name
        }
        self.assertEqual(test_expected_output, test_download_location.__unicode__())'''

    def test_cannot_create_download_location_without_game(self):
        '''
        Unit Test - Ensure that you aren't able to create download location objects without a game. 
        '''
        # attempt to create a download location without a game. Can't use helper function, since that function does it correctly
        test_download_location = DownloadLocation(
            href="www.google.com",
            name="GOG"
        )

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_download_location.full_clean()

        with self.assertRaises(IntegrityError): 
            test_download_location.save()






                    










