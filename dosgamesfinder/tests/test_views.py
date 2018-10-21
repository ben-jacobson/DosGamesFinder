from django.test import TestCase
#from .base import create_test_publisher, create_test_screenshot, create_test_dosgame, create_test_download_location, create_breaker_string#, create_test_game_and_publisher_package
#from dosgamesfinder.models import Publisher, DosGame, Screenshot, DownloadLocation

'''
Since our app doesn't have views per-se, instead we use this to test the functionality of our serializer
'''

class DosGameSerializerTests(TestCase): 
    def test_dosgames_data_returned_from_get_request(self):
        pass

    def test_listview_and_detailview_return_same_data(self):
        pass

    def test_related_screenshots_data_is_returned(self):
        pass

    def test_related_screenshots_data_excludes_id_and_game(self):
        pass

    def test_related_download_locations_data_is_returned(self):
        pass

    def test_related_download_locations_data_excludes_id_and_game(self):
        pass

    def test_related_publisher_data_is_returned(self):
        pass

    def test_content_type_returned_is_json(self):
        pass

    def test_dosgames_serializer_excludes_id(self):
        pass
      

class DosGamesSerializerPermissionsTests(TestCase):
    def test_can_send_get_request_to_endpoint(self):
        # assert that response code is 200
        pass

    def test_cannot_send_put_request_to_endpoint(self):
        pass

    def test_cannot_send_post_request_to_endpoint(self):
        pass
    
    def test_cannot_send_delete_request_to_endpoint(self):
        pass

    def test_cannot_send_patch_request_to_endpoint(self):
        pass

    def test_cannot_send_head_request_to_endpoint(self):
        pass

    def test_cannot_send_options_request_to_endpoint(self):
        pass
       