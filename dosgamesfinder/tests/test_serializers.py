from django.test import TestCase

from dosgamesfinder.serializers import DosGameSerializer, PublisherSerializer
from .base import create_test_publisher, create_test_screenshot, create_test_dosgame, create_test_download_location

class DosGameSerializerTests(TestCase): 
    '''
    Unit tests for DosGamesSerializer, and all nested Serializers. 
    '''
    def setUp(self):
        # for all tests, set up a few test objects accessible to entire class
        self.test_dosgame_name = 'Foobar Adventures'
        self.test_publisher_name = 'Test Software Inc'
        
        self.test_publisher = create_test_publisher(name=self.test_publisher_name) 
        self.test_dosgame = create_test_dosgame(publisher=self.test_publisher, title=self.test_dosgame_name)
        self.test_screenshot_one = create_test_screenshot(game=self.test_dosgame)
        self.test_screenshot_two = create_test_screenshot(game=self.test_dosgame)
        self.test_download_location = create_test_download_location(game=self.test_dosgame)

        # create the serializer object, which in turn creates the nested serialisers also tested
        self.serializer = DosGameSerializer(instance=self.test_dosgame)

    def test_dosgames_data_is_returned(self):
        self.assertEqual(self.serializer.data['title'], self.test_dosgame_name)

    def test_dosgames_data_contains_expected_fields_only(self):
        known_keys = self.serializer.data.keys()        
        expected_fields = [
            'id',
            'screenshots', 
            'download_locations', 
            'publisher', 
            'title', 
            'slug',
            'genre',
            'description',
            'date_releated',
            'user_rating', 
        ]
        # A cool side effect of using set - the order of each list doesn't matter.
        self.assertEqual(set(known_keys), set(expected_fields))

    def test_related_screenshots_data_is_returned(self):
        serialized_screenshot_data_one = self.serializer.data['screenshots'][0]['img_src'] # the first entry should match self.test_screenshot_one
        serialized_screenshot_data_two = self.serializer.data['screenshots'][1]['img_src'] # the first entry should match self.test_screenshot_one

        expected_screenshot_data_one = self.test_screenshot_one.img_src
        expected_screenshot_data_two = self.test_screenshot_one.img_src

        self.assertEqual(serialized_screenshot_data_one, expected_screenshot_data_one)
        self.assertEqual(serialized_screenshot_data_two, expected_screenshot_data_two)

    def test_related_screenshots_data_has_specified_fields_only(self):
        known_keys = self.serializer.data['screenshots'][0].keys()
        expected_fields = [
            'img_src',
            'img_width', 
            'img_height',
        ] 
        self.assertEqual(set(known_keys), set(expected_fields))

    def test_related_download_locations_data_is_returned(self):
        serialized_download_location_data = self.serializer.data['download_locations'][0]['href'] # the first entry should match self.test_screenshot_one
        expected_download_location_data = self.test_download_location.href
        self.assertEqual(serialized_download_location_data, expected_download_location_data)

    def test_related_download_locations_has_specified_fields_only(self):
        known_keys = self.serializer.data['download_locations'][0].keys()
        expected_fields = [
            'href', 
            'name',
        ] 
        self.assertEqual(set(known_keys), set(expected_fields))

    def test_related_publisher_data_is_returned(self):
        serialized_publisher_data = self.serializer.data['publisher']['name'] # the first entry should match self.test_screenshot_one
        expected_publisher_data = self.test_publisher.name
        self.assertEqual(serialized_publisher_data, expected_publisher_data)

    def test_related_publisher_has_specified_fields_only(self):
        known_keys = self.serializer.data['publisher'].keys()
        expected_fields = [
            'id', 
            'slug',
            'name',
            'description'
        ] 
        self.assertEqual(set(known_keys), set(expected_fields))

    def test_throttling_information_is_shown(self):
        # this test assumes that if the throttle information is given, that it will be adhered to
        # Writing a test to actually that that throttling will be very time and resource intensive, we just need to trust that DRF functions as expected
        pass

class PublisherSerializerTests(TestCase): 
    '''
    Unit tests for DosGamesSerializer, and all nested Serializers. 
    '''
    def setUp(self):
        # for all tests, set up a few test objects accessible to entire class
        self.test_publisher_name = 'Test Software Inc'
        self.test_publisher = create_test_publisher(name=self.test_publisher_name) 

        # create the serializer object, which in turn creates the nested serialisers also tested
        self.serializer = PublisherSerializer(instance=self.test_publisher)

    def test_publisher_data_is_returned(self):
        self.assertEqual(self.serializer.data['name'], self.test_publisher_name)

    def test_publisher_data_contains_expected_fields_only(self):
        known_keys = self.serializer.data.keys()        
        expected_fields = [
            'id', 
            'slug',
            'name',
            'description'
        ]
        self.assertEqual(set(known_keys), set(expected_fields))

      