$(function() {         
    // ===============
    // = Collections
    // ===============

    App.Collections.DosGames = Backbone.Collection.extend({
        baseURL: '/api/dosgames', 
        page_number: 1, 
        // url: '/api/dosgames',  
        model: App.Models.DosGame,

        url: function() {
            return this.baseURL + '?page=' + this.page_number;
        },

        parse: function(response) {
            //console.log(response);
            this.count = response.count;    // for pagination, we also want to populate this. 
            return response.results;
        }
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