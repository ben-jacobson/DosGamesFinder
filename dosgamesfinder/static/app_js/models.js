$(function () {
    // ===============
    // = Models
    // ===============

    App.Models.DosGame = Backbone.Model.extend({
        urlRoot: '/api/dosgames',
        idAttribute: 'slug',

        defaults: {
            //id: '',       // don't want to create a default ID
            slug: 'slug',
            title: 'title',
            genre: 'genre',
            long_description: 'description lorem ipsum dolor sit amet..',
            short_description: 'description lorem ipsum dolor sit amet..',
            year_released: 'year released',
            user_rating: 'user rating',
            publisher: 'publisher',
            thumbnail_src: '/no_screenshot.jpg',     
        },

        initialize: function (attrs) {
        // Data Validation - in case of missing data, fill it out here 
            // first check that we have an attributes argument to use. 
            if (attrs != undefined) {
                // assign the main screenshot as the first screenshot from the array, ListView relies on this as the thumbnail. Otherwise, it will default to what's specified in defaults above
                if (attrs.screenshots != undefined && attrs.screenshots.length != 0) {
                    this.set('thumbnail_src', attrs.screenshots[0].img_src);
                }
            }
        }, 
    });

    App.Models.Genre = Backbone.Model.extend();

    App.Models.Publisher = Backbone.Model.extend();

    App.Models.Ad = Backbone.Model.extend({  // placeholder for now
        defaults: {
            ad_img_url: "https://via.placeholder.com/728x90",
        }
    });
});