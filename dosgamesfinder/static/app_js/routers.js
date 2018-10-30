$(function () {
    // ===============
    // = Routers
    // ===============
    App.Router = Backbone.Router.extend({
        routes: {
            '': 'index',
            'game/:request_slug': 'game',
            'publisher/:request_slug': 'publisher',
        },

        index: function () {
            let DosGamesListView = new App.Views.DosGamesListView({collection: dosgames_collection});
            dosgames_collection.fetch(); // fetch new data off the server according to parameters, eg sorting, pagination
        },

        game: function (request_slug) {
            let dosgame_model = new App.Models.DosGame({slug: request_slug});
            dosgame_model.fetch();
            let DosGamesDetailView = new App.Views.DosGamesDetailView({model: dosgame_model});
        },

        publisher: function(request_slug) {

        }, 
    });

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