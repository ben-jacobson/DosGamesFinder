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

        index: function (page_number, genre, publisher, page_title) {   
            $(document).scrollTop(0); // Scroll to the top of the page

            if (page_number == null || page_number == undefined) {
                page_number = 1; 
            }

            if (page_title == null || page_title == undefined) {
                page_title = 'Dos Games A-Z'; 
            }

            // set our filters - okay if these are null as this is the default. 
            dosgames_collection.genre_filter = genre;       
            dosgames_collection.publisher_filter = publisher; 
            dosgames_collection.current_page = page_number;

            DosGamesListView = new App.Views.DosGamesListView({page_size: DOSGAMES_LISTVIEW_MAX_PAGE_SIZE, page_title: page_title, collection: dosgames_collection});
            dosgames_collection.fetch(); // fetch new data off the server according to parameters, eg sorting, pagination
        },

        filter_by_genre: function(genre, page_number) {  

            if (genre_collection.fetched === true) {  // if we can use the genre's name in the title, we will. if not then use something generic
                genre_obj = genre_collection.find({slug: genre});
                genre_name = genre_obj.get('name');
                DosGamesListView.trigger('RenamePage', `${genre_name} games`);          
            } 

            this.index(page_number, genre, null, "Filter By Genre");    // the code for filter by genre and publisher are identical, but the backbone routes get confused between them, so have create a simple wrapper
        },                                          

        filter_by_publisher: function(publisher, page_number) {
            this.index(page_number, null, publisher, "Filter By Publisher"); 
        },        

        game: function (request_slug) {
            $(document).scrollTop(0); // Scroll to the top of the page

            let dosgame_model = new App.Models.DosGame({slug: request_slug});
            dosgame_model.fetch();
            DosGamesDetailView = new App.Views.DosGamesDetailView({model: dosgame_model});
        },

        publishers_listview: function(page_number) {
         
            if (page_number != null && page_number != undefined) {      // our home page is the first page of the list view, see above we have two routes, one for index and one with a page number
                publisher_collection.current_page = page_number;
            }

            $(document).scrollTop(0); // Scroll to the top of the page
            
            PublisherListView = new App.Views.PublisherListView({page_size: PUBLISHER_LISTVIEW_MAX_PAGE_SIZE, collection: publisher_collection});
            publisher_collection.fetch(); 
        }, 
    });

    // set the max page sizes for pagination
    var DOSGAMES_LISTVIEW_MAX_PAGE_SIZE = 18;       // these numbers must match DRFs pagination
    var PUBLISHER_LISTVIEW_MAX_PAGE_SIZE = 20;

    // collect our genre objects so as to create the genre drop down as part of the page navigation
    var genre_collection = new App.Collections.Genres();
    genre_collection.fetch();

    // set up an event to write a status of when genre has been fetched, this is used for when the page needs to switch it's title
    genre_collection.on('sync', function() {        
        genre_collection.fetched = true; 
    });

    // draw our navigation bar
    var PageNavigation = new App.Views.PageNavigation({collection: genre_collection});

    // initialize our collection
    var dosgames_collection = new App.Collections.DosGames();
    var publisher_collection = new App.Collections.Publishers();

    // create empty objects for our views
    var DosGamesListView = [];
    var DosGamesDetailView = [];
    var PublisherListView = [];

    _.extend(DosGamesListView, Backbone.Events);        // DosGamesListView needs some event triggers

    $(document).ready(function() {
        // put in place our routers
        var router = new App.Router();
        Backbone.history.start();
    });
    //console.log('EOF');
});