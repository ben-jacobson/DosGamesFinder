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

        App.Models.Ad = Backbone.Model.extend({  // placeholder for now
            defaults: {
                ad_img_url: "https://via.placeholder.com/728x90", 
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
                    if (this.collection.at(i) == undefined) {
                        break;
                    }
                    else {
                        this.render_card(this.collection.at(i));
                    }
                }
                return this; 
            }       
        }); 

        App.Views.ListViewAdBreak = Backbone.View.extend({
            tagName: 'div',
            className: 'row text-center ad-break', 
            adbreak_template: _.template($('#listview-adbreak').html()),

            initialize: function() {
                this.render(); 
            },

            render: function() {
                this.$el.html(this.adbreak_template(this.model.toJSON()));
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

            return_collection_of_three_games: function(index) {   
                var three_games = new App.Collections.DosGames;
                    
                for (var i = 0; i < 3; i++) {
                    if (index + i >= this.collection.length) {
                        break;
                    }
                    else {
                        var extracted_game_model = this.collection.at(index + i);
                        three_games.add(extracted_game_model);
                    }
                }
                return three_games;                                               
            }, 
            
            render: function() {
                // render the page title
                // var PageTitle = new App.Views.PageTitle;
                // this.$el.append(PageTitle);

                // split this.collection into collections containing 3 games each and send to DosGamesCardListViewRow render function
                for (var i = 0; i < this.collection.length; i += 3) { 
                    // create a row of dos games
                    var row_collection = this.return_collection_of_three_games(i);
                    var DosGameCardListViewRow = new App.Views.DosGameCardListViewRow({collection: row_collection});
                    this.$el.append(DosGameCardListViewRow.el);
                    console.log('render row ' + i);

                    // every three rows, serve an ad
                    if (i % 9 == 6) { // you wouldn't believe how much math that took to pull off...
                        var adModel = new App.Models.Ad;
                        var ListViewAdBreak = new App.Views.ListViewAdBreak({model: adModel});
                        this.$el.append(ListViewAdBreak.el);
                        console.log('serve ad'); 
                    } 
                }
                return this;
            }
        });

        // create 12 identical DosGame objects and insert into the test collection , each using the models default values. just for testing purposes
        // for debugging purposes, we want to name them letters of the alphabet, so that we can test sorting, splitting, etc
        var alphabet = 'abcdefghijklmnopqrstuvwxyz';

        var DosGames = new App.Collections.DosGames; // todo - refactor to have the collection read off Django
        for (var i = 0; i < 28; i++) {
            Dosgame = new App.Models.DosGame({title: alphabet[i % alphabet.length]}); 
            DosGames.add(Dosgame);
        }
        //console.log(DosGames);

        //var test_game = DosGames.add(new App.Models.DosGame);
        //console.log(test_game);

        var DosGamesListView = new App.Views.DosGamesListView({collection: DosGames});
        console.log('done'); // just for debugging purpose
    })();
});



