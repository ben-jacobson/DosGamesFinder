$(function () {
    // ===============
    // = Models
    // ===============

    App.Models.DosGame = Backbone.Model.extend({
        defaults: {
            screenshot1: 'https://via.placeholder.com/320x200',
            screenshot2: 'https://via.placeholder.com/320x200',
            screenshot3: 'https://via.placeholder.com/320x200',
            screenshot4: 'https://via.placeholder.com/320x200',
            screenshot5: 'https://via.placeholder.com/320x200',

            id: '',
            slug: '',
            title: '',
            genre: '',
            description: '',
            year_released: '',
            user_rating: '',

            publisher_name: '',
            publisher_slug: '',
        },

        initialize: function (attrs) {
            // we know that the DosGame object in the API cannot be created without a publisher
            // essentially this flattens this relationship to make things simpler            
            this.set({
                publisher_name: attrs.publisher.name,   // name of publisher
                publisher_slug: attrs.publisher.slug,   // slug for publisher DetailView, used to create a href
            });
        },
    });

    App.Models.Ad = Backbone.Model.extend({  // placeholder for now
        defaults: {
            ad_img_url: "https://via.placeholder.com/728x90",
        }
    });
});