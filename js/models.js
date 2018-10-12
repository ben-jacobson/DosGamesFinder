$(function() {         
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
});