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

            if (new_page_title == null || new_page_title == undefined) {
                page_title_model.set('title', 'Games List A-Z');
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
            genre_obj = new App.Models.Genre({genre_selected: genre});
            genre_obj.fetch();

            genre_obj.on('sync', function() { 
                page_title_model.set('title', `${genre_obj.get('name')} Games`);
            });

            this.index(page_number, genre, null, 'Filter By Genre');    // the code for filter by genre and publisher are identical, but the backbone routes get confused between them, so have create a simple wrapper
        },                                          

        filter_by_publisher: function(publisher, page_number) {
            pub_obj = new App.Models.Publisher({publisher_selected: publisher});
            pub_obj.fetch();

            pub_obj.on('sync', function() { 
                page_title_model.set('title', `Games by ${pub_obj.get('name')}`);
            });

            this.index(page_number, null, publisher, 'Filter By Publisher'); 
        },        

        game: function (request_slug) {

            var dosgame_model = new App.Models.DosGame({slug: request_slug});
            dosgame_model.fetch();

            // Scroll to the top of the page
            $(document).scrollTop(0); 
            DosGamesDetailView = new App.Views.DosGamesDetailView({model: dosgame_model});
        },

        publishers_listview: function(page_number) {
            if (page_number != null && page_number != undefined) {      // our home page is the first page of the list view, see above we have two routes, one for index and one with a page number
                publisher_collection.current_page = page_number;
            }

            // Scroll to the top of the page
            $(document).scrollTop(0); 

            // render page title
            page_title_model.set('title', 'Publishers A-Z');
            PageTitle = new App.Views.PageTitle({model: page_title_model});

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

    // do an initial fetch
    genre_collection.fetch();
    publisher_collection.fetch();

    // create empty objects for our views
    var DosGamesListView = {};
    var DosGamesDetailView = {};
    var PublisherListView = {};
    var PageTitle = {};  
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