$( document ).ready(function() {
    (function() { 
        window.App = {
            Models: {},
            Collections: {}, 
            Views: {}
        };

        // ===============
        // = Models
        // ===============

        App.Models.DosGame = Backbone.Model.extend({
            defaults: {
                screenshot: 'https://via.placeholder.com/320x200',
                title: 'The Lorem Ipsum',
                description: "Game Desctiption Lorem ipsum dolor amet schlitz bitters taxidermy, etsy pour-over iPhone ugh mumblecore 90's XOXO meggings 3 wolf moon enamel pin flexitarian. Kitsch migas hammock shaman dreamcatcher butcher. Art party kitsch single-origin coffee dreamcatcher banjo roof party selvage blog neutra cronut",
                genre: 'Adventure',
                publisher: 'Dolor Amet Games',
                year_released: '1981',
                rating: 'xxxxx',
            }
        });

        // ===============
        // = Collections
        // ===============

        App.Collections.DosGames = Backbone.Collection.extend({
            model: App.Models.DosGame
        });

        // ===============
        // = Views
        // ===============
        
        App.Views.DosGameCardListViewCol = Backbone.View.extend({
            tagName: 'div',
            className: 'col-sm-4',  // the card view uses a 12 column grid, each card takes 4 columns.  
            dosgame_card_template: _.template($('#game-card-listView').html()),

            initialize: function() {
                this.render();
            },

            render: function() {
                this.$el.html(this.dosgame_card_template(this.model.toJSON())); // this is how to compile the template
                return this; 
            }        
        });

        App.Views.DosGameCardListViewRow = Backbone.View.extend({
            //el: '#listViewRow',
            tagName: 'div',
            className: 'row games-list-row', 
            row_length: 3, 

            initialize: function() {
                this.render();
            },

            render_card: function(DosGameModel) {
                var DosGameView = new App.Views.DosGameCardListViewCol({model: DosGameModel});
                this.$el.append(DosGameView.el);                    
            },

            render: function() {    // simply render a row, which is the first 3 items it receives in the collection. 
                for (var i = 0; i < this.row_length; i++) {
                    this.render_card(this.collection.at(i));
                }
                return this; 
            }       
        }); 

        App.Views.DosGamesListView = Backbone.View.extend({
            // enter the full collection into this view, the view will split the collection into as many
            // 3 column rows it can. Render a page title, then a pattern of 2 rows then adbreak, repeat.

            el: '#listView',
            tagName: 'div',
            className: 'container listing',

            initialize: function() {
                this.render();
            },
            
            render: function() {
                // split this.collection into collections containing 3 games each and send to DosGamesCardListViewRow render function
                //var DosGameCardListViewRow = new App.Views.DosGameCardListViewRow({collection: row_of_three});
                //this.$el.append(DosGameCardListViewRow.el);
                return this;
            }
        });

        // create 6 identical DosGame objects and insert into the test collection , each using the models default values. just for testing purposes
        var DosGames = new App.Collections.DosGames; // todo - refactor to have the collection read off Django

        for (var i = 0; i < 12; i++) {
            DosGames.add(new App.Models.DosGame);
        }

        var DosGamesListView = new App.Views.DosGamesListView({collection: DosGames});
        console.log('done'); // just for debugging purpose
    })();
});



