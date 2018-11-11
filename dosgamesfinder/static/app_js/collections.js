$(function() {         
    // ===============
    // = Collections
    // ===============

    App.Collections.DosGames = Backbone.Collection.extend({
        baseURL: '/api/dosgames', 
        current_page: 1, 
        // url: '/api/dosgames',  
        model: App.Models.DosGame,

        url: function() {
            return this.baseURL + '?page=' + this.current_page;
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

        parse: function(response) {
            return response.results;
        }
    });

    App.Collections.Publishers = Backbone.Collection.extend({
        url: '/api/publishers',  
        model: App.Models.Publusher,
    });
});