$(function () {
    // ===============
    // = Routers
    // ===============
    App.Router = Backbone.Router.extend({
        routes: {
            'publishers(/:page_number)': 'publishers_listview',
            'genre/:genre(/:page_number)': 'filter_by_genre',
            'publisher/:publisher(/:page_number)': 'filter_by_publisher',
            'game/:request_slug': 'game', 
            '(:page_number)': 'index',  
        },

        index: function (page_number, genre, publisher, new_page_title) {   

            if (page_number == null || page_number == undefined) {
                page_number = 1; 
            }

            // set page_title if one is supplied
            if (new_page_title == null || new_page_title == undefined) {        
                page_title_model.set('title', 'Games List A-Z');
            }
            else {
                page_title_model.set('title', new_page_title);
            }

            // Scroll to the top of the page
            $(document).scrollTop(0); 
        
            // set our filters - okay if these are null as this is the default. 
            dosgames_collection.genre_filter = genre;       
            dosgames_collection.publisher_filter = publisher; 
            dosgames_collection.current_page = page_number;

            // render page title
            PageTitle = new App.Views.PageTitle({model: page_title_model});

            // render the list view
            DosGamesListView = new App.Views.DosGamesListView({page_size: DOSGAMES_LISTVIEW_MAX_PAGE_SIZE, collection: dosgames_collection});
            dosgames_collection.fetch(); // fetch new data off the server according to parameters, eg sorting, pagination
        },

        filter_by_genre: function(genre, page_number) {  
            new_page_title = 'Filter By Genre';

            if (genre_collection.fetched === true) {  // if we can use the genre's name in the title, we will. if not then use something generic
                genre_obj = genre_collection.find({slug: genre});
                genre_name = genre_obj.get('name');
                new_page_title = `${genre_name} Games`;
            } 

            this.index(page_number, genre, null, new_page_title);    // the code for filter by genre and publisher are identical, but the backbone routes get confused between them, so have create a simple wrapper
        },                                          

        filter_by_publisher: function(publisher, page_number) {
            new_page_title = 'Filter by publisher';

            if (publisher_collection.fetched === true) {  // if we can use the genre's name in the title, we will. if not then use something generic
                pub_obj = publisher_collection.find({slug: publisher});
                publisher_name = pub_obj.get('name');
                new_page_title = `Games By ${publisher_name}`;
            }

            this.index(page_number, null, publisher, new_page_title); 
        },        

        game: function (request_slug) {

            let dosgame_model = new App.Models.DosGame({slug: request_slug});
            dosgame_model.fetch();

            // Scroll to the top of the page
            $(document).scrollTop(0); 
            DosGamesDetailView = new App.Views.DosGamesDetailView({model: dosgame_model});
        },

        publishers_listview: function(page_number) {
            if (page_number != null && page_number != undefined) {      // our home page is the first page of the list view, see above we have two routes, one for index and one with a page number
                publisher_collection.current_page = page_number;
            }

            
            // render page title
            page_title_model.set('title', 'Publishers A-Z');
            PageTitle = new App.Views.PageTitle({model: page_title_model});

            // Scroll to the top of the page
            $(document).scrollTop(0); 

            PublisherListView = new App.Views.PublisherListView({page_size: PUBLISHER_LISTVIEW_MAX_PAGE_SIZE, collection: publisher_collection});
            publisher_collection.fetch(); 
        }, 
    });

    // set the max page sizes for pagination
    var DOSGAMES_LISTVIEW_MAX_PAGE_SIZE = 18;       // these numbers must match DRFs pagination
    var PUBLISHER_LISTVIEW_MAX_PAGE_SIZE = 20;

    // initialize our collection
    var dosgames_collection = new App.Collections.DosGames();
    var publisher_collection = new App.Collections.Publishers();
    var genre_collection = new App.Collections.Genres();
    genre_collection.fetch();

    // set up two events to set flags when publisher and genre collections have been fetched
    genre_collection.on('sync', function() {        
        genre_collection.fetched = true; 
    });

    publisher_collection.on('sync', function() {        
        publisher_collection.fetched = true; 
    });

    // create empty objects for our views
    var DosGamesListView = [];
    var DosGamesDetailView = [];
    var PublisherListView = [];
    var PageTitle = [];  
    var page_title_model = new App.Models.PageTitle();  // PageTitle view uses this model to store page titles

    $(document).ready(function() {      // only start the router once the document is ready to load 
        // put in place our routers
        var router = new App.Router();
        Backbone.history.start();
    });

    // draw our navigation bar
    var PageNavigation = new App.Views.PageNavigation({collection: genre_collection});

    //console.log('EOF');
});