# first set up a few django system requirements
import os
import django
import json

def return_publisher_object(name, description):
    '''
    Searches for the requested publisher object and returns it.
    If empty, will assign this to a publisher object called 'unknown'.
    If not found, will create a new publisher object.
    '''
    pass
    if name is '':
        #print('Publisher cannot be blank, assigning to unknown')
        name = 'Unknown'

    try: 
        #print (f'searching for publisher: {name}')
        pub = Publisher.objects.get(name=name)
    except Publisher.DoesNotExist: 
        #print (f'{name} not found, creating')
        pub = Publisher(name=name, description=description)
        pub.save()

    return pub

def return_genre_object(name):
    '''
    Searches for the requested genre object and returns it.
    If empty, will assign this to a genre object called 'unknown'.
    If not found, will create a new genre object.
    '''
    if name is '':
        #print('Genre cannot be blank, assigning to unknown')
        name = 'Unknown'

    try: 
        #print (f'searching for genre: {name}')
        genre = Genre.objects.get(name=name)
    except Genre.DoesNotExist: 
        #print (f'{name} not found, creating')
        genre = Genre(name=name)
        genre.save()

    return genre

def return_dosgame_object(title, genre, long_description, year_released, publisher, user_rating=5):
    '''
    Searches for the requested DosGame object and returns it.
    If empty, will assign this to a genre object called 'unknown'.
    If not found, will create a new genre object.
    '''
    try: 
        #print (f'searching for genre: {name}')
        dosgame = DosGame.objects.get(title=title)
    except DosGame.DoesNotExist: 
        #print (f'{name} not found, creating')
        dosgame = DosGame(
            title=title, 
            genre=genre, 
            long_description=long_description, 
            year_released=year_released, 
            publisher=publisher,
            user_rating=user_rating
        )
        dosgame.save()
        dosgame.full_clean()

    return dosgame

def create_screenshots(dosgame, screenshot_list):
    '''
    Create screenshot objects for a specific game
    If the game doesn't exist, return False
    If the game exists but has screenshots already, return False
    '''
    try: 
        dg = DosGame.objects.get(title=dosgame.title) 
    except DosGame.DoesNotExist:    # if the game doesn't exist, terminate
        return False
 
    if not dg.screenshots.all():  # if no screenshots exist in the object, then we create it
        for screen in screenshot_list:
            screenshot_obj = Screenshot(img_src=screen, img_width=320, img_height=200, game=dg)
            screenshot_obj.save()
    else:   # if screenshots exist, then we quit
        return False

def create_download_locations(dosgame, download_location_href):
    '''
    Create download location objects for a specific game
    If the game doesn't exist, return False
    If the game exists but has download locations already, return False
    '''
    try: 
        dg = DosGame.objects.get(title=dosgame.title) 
    except DosGame.DoesNotExist:    # if the game doesn't exist, terminate
        return False
 
    if not dg.download_locations.all():  # if no screenshots exist in the object, then we create it
        missing_fwd_corrected_dl_location = '/' + download_location_href
        download_location = DownloadLocation(name='Shareware version', href=missing_fwd_corrected_dl_location, game=dg)
        download_location.save()
    else:   # if download location exist, then we quit
        return False

# set up some initial django stuff so that we can run this as a standalone script
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restapp.settings")
    django.setup()

    from dosgamesfinder.models import Publisher, DosGame, Genre, Screenshot, DownloadLocation

    # open the file and import the JSON data, outputs as a list of dict() objects
    with open(file='initial_dbase.json', mode='r') as file_handle:
        json_data = json.load(file_handle)

    # loop through each list entry, each is a dict and use the data to create database entries
    for game_data in json_data:
        # create the publisher if it doesn't already exist
        publisher = return_publisher_object(name=game_data['publisher'], description='')

        # create the genre if it doesn't already exist
        genre = return_genre_object(name=game_data['genre'])

        # create the dosgame itself and assign the publisher and genre
        dosgame = return_dosgame_object(
            title=game_data['title'],
            genre=genre,
            long_description=game_data['description'],
            year_released=game_data['year_released'],
            publisher=publisher,
        )

        # create the screenshot objects, assiging these to the game itself
        create_screenshots(dosgame=dosgame, screenshot_list=game_data['screenshots'])

        # create the download location objects, assigning these to the game itself
        create_download_locations(dosgame=dosgame, download_location_href=game_data['download_url'])

    # test the results
    for dl in DownloadLocation.objects.all():
        print(f'Game: {dl.game}, Href: {dl.href}')


'''
# A quick script for clearing the entire database.

from dosgamesfinder.models import DosGame, Publisher, Screenshot, DownloadLocation

for dg in DosGame.objects.all():
    dg.delete()

for p in Publisher.objects.all():
    p.delete()

for s in Screenshot.objects.all():
    s.delete()

for dl in DownloadLocation.objects.all():
    dl.delete()

'''