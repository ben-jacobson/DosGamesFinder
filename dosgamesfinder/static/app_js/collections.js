$(function() {         
    // ===============
    // = Collections
    // ===============

    App.Collections.DosGames = Backbone.Collection.extend({
        baseURL: '/api/dosgames/', 
        current_page: 1, 
        genre_filter: null,
        publisher_filter: null,
        model: App.Models.DosGame,

        url: function() {
            var query_string = this.baseURL + '?page=' + this.current_page; 

            if (this.genre_filter != null) {
                query_string += '&genre=' + this.genre_filter;
            }

            if (this.publisher_filter != null) {
                query_string += '&publisher=' + this.publisher_filter;
            }
            //console.log(`collection returns url as ${query_string}`);
            return query_string;
        },

        parse: function(response) {
            //console.log(response);
            this.count = response.count;    // for pagination, we also want to populate this. 
            return response.results;
        }
    });

    App.Collections.Genres = Backbone.Collection.extend({
        url: '/api/genres/',  
        model: App.Models.Genre,

        parse: function(response) {
            return response.results;
        }
    });

    App.Collections.Publishers = Backbone.Collection.extend({
        current_page: 1,      
        baseURL: '/api/publishers/',  
        model: App.Models.Publisher,

        url: function() {
            var query_string = this.baseURL + '?page=' + this.current_page; 
            return query_string;
        },

        parse: function(response) {
            this.count = response.count;  
            return response.results;
        }
    });
});