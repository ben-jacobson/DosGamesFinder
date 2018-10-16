from dosgamesfinder.models import DosGame, Publisher, Screenshot
 
def create_test_publisher(name='Test Software'):    
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
                        user_rating=4,):
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