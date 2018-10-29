$(function() {         
    // ===============
    // = Collections
    // ===============

    App.Collections.DosGames = Backbone.Collection.extend({
        url: '/api/dosgames',  
        model: App.Models.DosGame,
    });

    App.Collections.Genres = Backbone.Collection.extend({
        url: '/api/genres',  
        model: App.Models.Genre,
    });

    App.Collections.Publishers = Backbone.Collection.extend({
        url: '/api/publishers',  
        model: App.Models.Publusher,
    });
});