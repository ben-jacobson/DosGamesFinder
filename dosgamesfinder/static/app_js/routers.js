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

        index: function (page_number, genre, publisher) {   
            // if genre or publisher isn't populated, it will come in as null, which the collection methods expect
            if (page_number == null || page_number == undefined) {
                page_number = 1; 
            }

            $(document).scrollTop(0); // Scroll to the top of the page

            // set our filters - okay if these are null as this is the default. 
            dosgames_collection.genre_filter = genre;       
            dosgames_collection.publisher_filter = publisher; 
            dosgames_collection.current_page = page_number;

            let DosGamesListView = new App.Views.DosGamesListView({page_size: DOSGAMES_LISTVIEW_MAX_PAGE_SIZE, collection: dosgames_collection});
            dosgames_collection.fetch(); // fetch new data off the server according to parameters, eg sorting, pagination
        },

        filter_by_genre: function(genre, page_number) {
            this.index(page_number, genre, null);    // the code for filter by genre and publisher are identical, but the backbone routes get confused between them, so have create a simple wrapper
        },                                           // if we can figure out how to remove the need for this, we can technical set this up to have both filters enabled at the same time 

        filter_by_publisher: function(publisher, page_number) {
            this.index(page_number, null, publisher); 
        },        

        game: function (request_slug) {
            $(document).scrollTop(0); // Scroll to the top of the page

            let dosgame_model = new App.Models.DosGame({slug: request_slug});
            dosgame_model.fetch();
            let DosGamesDetailView = new App.Views.DosGamesDetailView({model: dosgame_model});
        },

        publishers_listview: function(page_number) {
         
            if (page_number != null && page_number != undefined) {      // our home page is the first page of the list view, see above we have two routes, one for index and one with a page number
                publisher_collection.current_page = page_number;
            }

            $(document).scrollTop(0); // Scroll to the top of the page
            let PublisherListView = new App.Views.PublisherListView({page_size: PUBLISHER_LISTVIEW_MAX_PAGE_SIZE, collection: publisher_collection});
            publisher_collection.fetch(); 
        }, 
    });

    // set the max page sizes for pagination
    var DOSGAMES_LISTVIEW_MAX_PAGE_SIZE = 18;       // these numbers must match DRFs pagination
    var PUBLISHER_LISTVIEW_MAX_PAGE_SIZE = 20;

    // collect our genre objects so as to create the genre drop down as part of the page navigation
    var genre_collection = new App.Collections.Genres();
    genre_collection.fetch();

    // draw our navigation bar
    var PageNavigation = new App.Views.PageNavigation({collection: genre_collection});

    // initialize our collection
    var dosgames_collection = new App.Collections.DosGames();
    //dosgames_collection.fetch(); // initial fetch of default data. not entirely necessary

    var publisher_collection = new App.Collections.Publishers();

    // put in place our routers
    var router = new App.Router();
    Backbone.history.start();

    //console.log('EOF');
});