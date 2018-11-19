$(function() {       
    // ===============
    // = Views
    // ===============
    App.Views.PageNavigation = Backbone.View.extend({
        // View for rendering the page navigation bar 
        el: '#page-navigation-container', 
        page_navigation_template: _.template($('#page-navigation').html()),

        initialize: function() {
            //this.render();
            this.collection.on('sync', this.render, this); 
        },
        render: function() {
            this.$el.html(this.page_navigation_template({genres: this.collection})); 
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
            for (let i = 0; i < this.row_length; i++) {
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

    App.Views.ListViewPagination = Backbone.View.extend({
        // generic pagination view class that can be used for DosGamesListView or PublisherListView
        el: '#appWindow',
        tagName: 'div',
        pagination_template: _.template($('#pagination').html()),

        initialize: function(args) {
            this.page_size = args['page_size'];
            this.render();      // since this is used as a child class of listView, it will have missed the sync event. Init of this view will only happen after the collection is fully synced
        },

        get_url_suffix: function() {        // when applying pagination, it needs to include this suffix
            // /#genre/action/1
            // /#genre/action/
            // /#/1
            current_url = String(Backbone.history.fragment);

            if (current_url == '') { // if it's a blank string, no need to create any suffix 
                return '';
            }

            current_url = current_url.replace(/\d+/, ''); // replace any number of digits with blanks.
            
            if (current_url[current_url.length - 1] != '/') {   // is the last character in this string a /?
                current_url = current_url + '/';        // if we don't already, append the stirng with a forward slash, but only one. 
            }

            return current_url;
        }, 
    
        render: function() {
            let number_of_pages = Math.ceil(this.collection.count / this.page_size);
            //console.log(`page size: ${this.page_size}, count: ${this.collection.count} = ${number_of_pages} pages`);

            this.url_suffix = this.get_url_suffix();    // get our url suffix so that filtering doesn't break pagination
            //console.log(`URL prefix: '${this.url_suffix}'`);

            if (this.collection.count > this.page_size) { // we only render pagination when necessary
                let current_page = Number(this.collection.current_page);        // getting some strange errors due to loose typing

                this.$el.append(this.pagination_template({
                    number_of_pages: number_of_pages, 
                    url_suffix: this.url_suffix, 
                    current_page: String(current_page), 
                    prev_page: String(current_page - 1),    // rather than doing the math within the template, just a bit cleaner to do it here.  
                    next_page: String(current_page + 1)
                }));  
                
            }
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

        initialize: function(args) {
            //this.render();
            this.collection.on('sync', this.render, this); // whenever we finish re-syncing to database, we want to render
            this.page_size = args['page_size'];
        },

        return_collection_of_three_games: function(index) {   
            var three_games = new App.Collections.DosGames;
                
            for (let i = 0; i < 3; i++) {
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
            let PageTitle = new App.Views.PageTitle("Games List A-Z");
            this.$el.html(PageTitle.el); 

            // render the pagination at the top of the page
            let DosGamesPaginationViewTop = new App.Views.ListViewPagination({page_size: this.page_size, collection: this.collection});
            this.$el.append(DosGamesPaginationViewTop.el);
            
            //console.log(this.collection);

            // split this.collection into collections containing 3 games each and send to DosGamesCardListViewRow render function
            for (let i = 0; i < this.collection.length; i += 3) { 
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

            // render the bottom pagination
            let DosGamesPaginationViewBottom = new App.Views.ListViewPagination({page_size: this.page_size, collection: this.collection});
            this.$el.append(DosGamesPaginationViewBottom.el);

            //console.log('ListView rendered');
            return this;
        }
    });

    App.Views.DosGamesDetailView = Backbone.View.extend({
        el: '#appWindow',
        tagName: 'div',
        className: 'container listing',
        detailView_template: _.template($('#game-detailView').html()),

        initialize: function(args) {
            this.model.on('sync', this.render, this);
        },

        render: function() {
            this.$el.html(this.detailView_template(this.model.toJSON()));         
            return this;
        }
    });    


});    