$(function () {
    // ===============
    // = Models
    // ===============

    App.Models.DosGame = Backbone.Model.extend({
        defaults: {
            main_screenshot: 'https://via.placeholder.com/320x200',

            //id: '',       // don't want to create a default ID
            slug: 'slug',
            title: 'title',
            genre: 'genre',
            description: 'description lorem ipsum dolor sit amet..',
            year_released: 'year released',
            user_rating: 'user rating',
            publisher: 'publisher',
        },

        initialize: function (attrs) {
            // some initial data validation takes place here, just incase of missing data, 
            // we'll fill in with placeholder data
            //console.log(attrs);

            // if we get data where there is no screenshots, stay with the default. 
            // Otherwise, set it to screenshot 0

            if (attrs.screenshots != undefined && attrs != undefined) {
                if (attrs.screenshots.length != 0) {
                    this.set('main_screenshot', attrs.screenshots[0].img_src); // set default screenshot to first one
                } /*else {
                    console.log(`No screenshots  for ${attrs.title}`);
                }*/
    
                // if we receive no download locations for our game, set a flag for our view to use
                if (attrs.download_locations != undefined && attrs.download_locations.length == 0) {
                    //console.log(`No download locations for ${attrs.title}`);
                    this.set('download_locations', false);
                }
            }
        },
    });

    App.Models.Ad = Backbone.Model.extend({  // placeholder for now
        defaults: {
            ad_img_url: "https://via.placeholder.com/728x90",
        }
    });
});