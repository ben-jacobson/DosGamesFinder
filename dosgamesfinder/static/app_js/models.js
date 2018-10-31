$(function () {
    // ===============
    // = Models
    // ===============

    App.Models.DosGame = Backbone.Model.extend({
        urlRoot: '/api/dosgames',
        idAttribute: 'slug',

        defaults: {
            //id: '',       // don't want to create a default ID
            main_screenshot: 'https://via.placeholder.com/320x200',
            slug: 'slug',
            title: 'title',
            genre: 'genre',
            description: 'description lorem ipsum dolor sit amet..',
            year_released: 'year released',
            user_rating: 'user rating',
            publisher: 'publisher',
        },

        initialize: function (attrs) {
        // Data Validation - in case of missing data, fill it out here 
            // first check that we have an attributes argument to use. 

            // we need to rely on getters and setters to introduce an array into the model
            if (attrs != undefined) {
                if (attrs.screenshots != undefined && attrs.screenshots.length != 0) {
                    this.set('main_screenshot', attrs.screenshots[0].img_src);
                }

                // fill in missing download location data if necessary
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