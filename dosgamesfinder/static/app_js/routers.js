$(function () {
    // ===============
    // = Routers
    // ===============
    App.Router = Backbone.Router.extend({
        routes: {
            '': 'index', 
            ':page_number': 'index',
            'game/:request_slug': 'game',
            'publisher/:request_slug': 'publisher',
        },

        index: function (page_number) {
            $(document).scrollTop(0); // Scroll to the top of the page

            if (page_number != null && page_number != undefined) {      // our home page is the first page of the list view, see above we have two routes, one for index and one with a page number
                dosgames_collection.current_page = page_number;
            }
            
            let DosGamesListView = new App.Views.DosGamesListView({page_size: DOSGAMES_LISTVIEW_MAX_PAGE_SIZE, collection: dosgames_collection});
            //let DosGamesPaginationView = new App.Views.ListViewPagination({page_size: DOSGAMES_LISTVIEW_MAX_PAGE_SIZE, collection: dosgames_collection});
            dosgames_collection.fetch(); // fetch new data off the server according to parameters, eg sorting, pagination
        },

        game: function (request_slug) {
            $(document).scrollTop(0); // Scroll to the top of the page

            let dosgame_model = new App.Models.DosGame({slug: request_slug});
            dosgame_model.fetch();
            let DosGamesDetailView = new App.Views.DosGamesDetailView({model: dosgame_model});
        },

        publisher: function(request_slug) {

        }, 
    });

    // set the max page sizes for pagination
    var DOSGAMES_LISTVIEW_MAX_PAGE_SIZE = 18;
    var PUBLISHER_LISTVIEW_MAX_PAGE_SIZE = 10;

    // collect our genre objects so as to create the genre drop down as part of the page navigation
    var genre_collection = new App.Collections.Genres();
    genre_collection.fetch();

    // draw our navigation bar
    var PageNavigation = new App.Views.PageNavigation({collection: genre_collection});

    // initialize our collection
    var dosgames_collection = new App.Collections.DosGames();
    //dosgames_collection.fetch(); // initial fetch of default data. not entirely necessary

    // put in place our routers
    var router = new App.Router();
    Backbone.history.start();

    console.log('EOF');
});