$(function () {
    // ===============
    // = Routers
    // ===============
    App.Router = Backbone.Router.extend({
        routes: {
            '': 'index',
            'game/:request_slug': 'game',
            'publisher/:request_slug': 'publisher',
            //'test': 'test',
        },

        index: function () {
            var DosGamesListView = new App.Views.DosGamesListView({ collection: dosgames_collection });
            dosgames_collection.fetch(); // fetch new data off the server according to parameters, eg sorting, pagination
        },

        game: function (request_slug) {
            // we pass the entire collection into the DetailView, so that the view can use event listeners to update data
            var DosGamesDetailView = new App.Views.DosGamesDetailView({ collection: dosgames_collection, game_slug: request_slug });
            dosgames_collection.fetch(); // fetch new data off the server according to parameters, eg sorting, pagination
        },

        publisher: function(request_slug) {


        }, 

        /* test: function () {
            var PageNavigation = new App.Views.PageNavigation;

            // create 24 identical DosGame objects and insert into the test collection , each using the models default values. just for testing purposes
            // for debugging purposes, we want to name them letters of the alphabet, so that we can test sorting, splitting, etc
            var alphabet = 'abcdefghijklmnopqrstuvwxyz';

            var DosGames = new App.Collections.DosGames;
            //test_collection_prototype = Backbone.Collection.extend({model: App.Models.DosGame})
            //var DosGames = new test_collection_prototype();
            for (let i = 0; i < 24; i++) {
                Dosgame = new App.Models.DosGame({ title: alphabet[i % alphabet.length] });
                DosGames.add(Dosgame);
            }

            var DosGamesListView = new App.Views.DosGamesListView({ collection: DosGames });
            console.log(DosGames);
            DosGamesListView.render(); // since there is no fetch event to trigger, we need to run ourselves.
        },

        game: function (slug) {
            console.log('slug = ' + slug); 

            var PageNavigation = new App.Views.PageNavigation;

            test_dos_game = new App.Models.DosGame({
                screenshot: 'https://via.placeholder.com/320x200',
                title: 'Doom',
                description: 'Doom is a 1993 first-person shooter video game by id Software. It is considered one of the most significant and influential titles in video game history, for having helped to pioneer the now-ubiquitous first-person shooter.',
                genre: 'Action',
                publisher: 'Id Software',
                year_released: '1993',
                user_rating: '5',
            });

            var DosGamesDetailView = new App.Views.DosGamesDetailView({ model: test_dos_game });
        },        
        
        */ 
    });

    // draw our navigation bar
    var PageNavigation = new App.Views.PageNavigation;

    // initialize our collection
    var dosgames_collection = new App.Collections.DosGames();
    //dosgames_collection.fetch(); // initial fetch of default data. not entirely necessary

    // put in place our routers
    var router = new App.Router();
    Backbone.history.start();

    console.log('EOF');
});