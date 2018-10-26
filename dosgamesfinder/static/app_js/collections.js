$(function() {         
    // ===============
    // = Collections
    // ===============

    App.Collections.DosGames = Backbone.Collection.extend({
        url: 'http://localhost:8000/api/dosgames',  
        model: App.Models.DosGame,
    });
});