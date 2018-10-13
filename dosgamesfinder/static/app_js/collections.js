$(function() {         
    // ===============
    // = Collections
    // ===============

    App.Collections.DosGames = Backbone.Collection.extend({
        model: App.Models.DosGame
    });
});