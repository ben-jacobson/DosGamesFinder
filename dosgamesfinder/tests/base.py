from dosgamesfinder.models import DosGame, Publisher, Genre, Screenshot, DownloadLocation

def create_test_publisher(name='Test Software'):    
    '''
    Test Helper Function - Creates a test publisher object and saves to test db. Returns the publisher object
    '''     
    test_publisher = Publisher(
        name=name, 
        description='Founded in 2025 - Pretty good software company'
    )
    test_publisher.save()
    return test_publisher

def create_test_genre(name='Adventure'):    
    '''
    Test Helper Function - Creates a test genre object and saves to test db. Returns the genre object
    '''     
    test_genre = Genre(
        name=name, 
    )
    test_genre.save()
    return test_genre    

def create_test_screenshot( game, 
                            img_src='https://via.placeholder.com/320x200', 
                            img_width=320, 
                            img_height=200):
    '''
    Test Helper Function - Creates a test screenshot object and saves to test db. Returns the screenshot object
    '''                            
    test_screenshot = Screenshot(
        img_src=img_src,
        img_width=img_width,
        img_height=img_height,
        game=game,
    )
    test_screenshot.save()
    return test_screenshot

def create_test_dosgame(publisher, 
                        genre,
                        title='FooBar Adventures', 
                        long_description='FooBar Adventures is a 1991 classic Dos game', 
                        year_released='1991', 
                        user_rating=4,
                        thumbnail_src='www.google.com'):
    '''
    Test Helper Function - Creates a test dosgame object and saves to test db. Returns the dosgame object
    '''
    test_dosgame = DosGame(
        title=title,
        genre=genre,
        long_description=long_description,
        year_released=year_released,
        user_rating=user_rating,
        publisher=publisher,
        thumbnail_src=thumbnail_src
    )
    test_dosgame.save()
    return test_dosgame

def create_test_download_location(  game, 
                                    href='http://www.google.com', 
                                    name='GOG'):
    '''
    Helper Function - create a test download location and save to db. Returns the object
    '''
    test_download_location = DownloadLocation(
        game=game,
        href=href,
        name=name
    )
    test_download_location.save()
    return test_download_location

def create_breaker_string(length):
    test_breaker_string = ''

    for _ in range(length):       # using the _ as an iterator lets you remain anonymous.
        test_breaker_string += '.'

    return test_breaker_string    

class test_objects_mixin():
    '''
    A lot of these test classes have the same setUp method, created a quick mixin for DRY purposes
    '''
    def setUp(self):
        self.test_publisher = create_test_publisher()
        self.test_genre = create_test_genre()
        self.test_dosgame = create_test_dosgame(publisher=self.test_publisher, genre=self.test_genre)
        
        self.test_dosgame_slug = {'slug': self.test_dosgame.slug}
        self.test_publisher_slug = {'slug': self.test_publisher.slug}    
        self.test_genre_slug = {'slug': self.test_genre.slug}
    

