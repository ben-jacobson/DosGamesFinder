from dosgamesfinder.models import DosGame, Publisher, Screenshot
 
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
                        title='FooBar Adventures', 
                        genre='Action', 
                        description='FooBar Adventures is a 1991 classic Dos game', 
                        date_releated='1991', 
                        user_rating=4):
    '''
    Test Helper Function - Creates a test dosgame object and saves to test db. Returns the dosgame object
    '''
    test_dosgame = DosGame(
        title=title,
        genre=genre,
        description=description,
        date_releated=date_releated,
        user_rating=user_rating,
        publisher=publisher,
    )
    test_dosgame.save()
    return test_dosgame

def create_breaker_string(length):
    test_breaker_string = ''

    for _ in range(256):       # using the _ as an iterator lets you remain anonymous.
        test_breaker_string += '.'

    return test_breaker_string    

'''def create_test_game_and_publisher_package( publisher_name='Test Software',
                                            title='FooBar Adventures', 
                                            genre='Action', 
                                            description='FooBar Adventures is a 1991 classic Dos game', 
                                            date_releated='1991', 
                                            user_rating=4,
                                            img_src='https://via.placeholder.com/320x200', 
                                            img_width=320, 
                                            img_height=200):

    '/''
    #Test Helper Function - Creates a publisher object, a dosgame and a screenshot object for testing purposes. Returns only the Dosgame
    '/''
    test_publisher = create_test_publisher(name=publisher_name)
    test_dosgame = create_test_dosgame(publisher=test_publisher, title=title, genre=genre, description=description, date_releated=date_releated, user_rating=user_rating)
    create_test_screenshot(game=test_dosgame, img_src=img_src, img_width=img_width, img_height=img_height)    
    return test_dosgame'''