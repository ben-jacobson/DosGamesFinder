$(function() {       
    // ===============
    // = Views
    // ===============

    App.Views.PageNavigation = Backbone.View.extend({
        // View for rendering the page navigation bar 
        el: '#page-navigation-container', 
        page_navigation_template: _.template($('#page-navigation').html()),

        initialize: function() {
            this.render();
        },
        render: function() {
            this.$el.html(this.page_navigation_template()); 
            return this; 
        }        
    });

    App.Views.PageTitle = Backbone.View.extend({
        // View for rendering page titles, be that listView or detailView
        tagName: 'div',
        className: 'row page-header',
        page_header_template: _.template($('#page-title').html()),

        initialize: function(page_title) {
            this.page_title = page_title;
            this.render();
        },
        render: function() {
            // by design, this view also alters the browser title to be the same as the views title. 
            var brand_page_title = $(document).attr("title");
            $(document).attr("title", this.page_title + " - " + brand_page_title);

            // then creates a header to render from template 
            this.$el.html(this.page_header_template({page_title: this.page_title})); 
            return this; 
        }
    });
    
    App.Views.DosGameCardListViewCol = Backbone.View.extend({
        // View for rendering the individual cards, within the row, of the listView
        tagName: 'div',
        className: 'col-sm-4',  // the card view uses a 12 column grid, each card takes 4 columns.  
        dosgame_card_template: _.template($('#game-card-listView').html()),

        initialize: function() {
            this.render();
        },

        render: function() {
            this.$el.html(this.dosgame_card_template(this.model.toJSON())); 
            return this; 
        }        
    });

    App.Views.DosGameCardListViewRow = Backbone.View.extend({
        // view for rendering a row of dos game cards in list view
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
        // View for rendering ad breaks between rows in list view
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
        // One of the main app views
        // enter the full collection into this view, the view will split the collection into as many
        // 3 column rows it can. Render a page title, then a pattern of 3 rows then adbreak, repeat.
        el: '#appWindow',
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
            var PageTitle = new App.Views.PageTitle("Games List A-Z");
            this.$el.html(PageTitle.el);

            // split this.collection into collections containing 3 games each and send to DosGamesCardListViewRow render function
            for (var i = 0; i < this.collection.length; i += 3) { 
                // create a row of dos games
                var row_collection = this.return_collection_of_three_games(i);
                var DosGameCardListViewRow = new App.Views.DosGameCardListViewRow({collection: row_collection});
                this.$el.append(DosGameCardListViewRow.el);
                //console.log('render row ' + i);

                // every three rows, serve an ad
                if (i % 9 == 6) { // you wouldn't believe how much math that took to pull off...
                    var adModel = new App.Models.Ad;
                    var ListViewAdBreak = new App.Views.ListViewAdBreak({model: adModel});
                    this.$el.append(ListViewAdBreak.el);
                    //console.log('serve ad'); 
                } 
            }
            return this;
        }
    });

    App.Views.DosGamesDetailView = Backbone.View.extend({
        el: '#appWindow',
        tagName: 'div',
        className: 'container listing',
        detailView_template: _.template($('#game-detailView').html()),

        initialize: function() {
            this.render();
        },
        
        render: function() {
            // render the page title
            //var PageTitle = new App.Views.PageTitle(this.model.get('title'));
            //this.$el.html(PageTitle.el);
            this.$el.html(this.detailView_template(this.model.toJSON()));         
            return this;
        }
    });
});    