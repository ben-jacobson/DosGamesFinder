$(function () {
    // ===============
    // = Models
    // ===============

    App.Models.DosGame = Backbone.Model.extend({
        defaults: {
            /* screenshot1: 'https://via.placeholder.com/320x200',
            screenshot2: 'https://via.placeholder.com/320x200',
            screenshot3: 'https://via.placeholder.com/320x200',
            screenshot4: 'https://via.placeholder.com/320x200',
            screenshot5: 'https://via.placeholder.com/320x200',*/ 

            main_screenshot: 'https://via.placeholder.com/320x200',

            id: '',
            slug: '',
            title: '',
            genre: '',
            description: '',
            year_released: '',
            user_rating: '',

        },

        initialize: function (attrs) {
            // some initial data validation takes place here, just incase of missing data, 
            // we'll fill in with placeholder data
            
            // if we get data where there is no screenshots, stay with the default. 
            // Otherwise, set it to screenshot 0
            if (attrs.screenshots.length != 0) {
                this.set('main_screenshot', attrs.screenshots[0].img_src); // set default screenshot to first one
            }
        },
    });

    App.Models.Ad = Backbone.Model.extend({  // placeholder for now
        defaults: {
            ad_img_url: "https://via.placeholder.com/728x90",
        }
    });
});