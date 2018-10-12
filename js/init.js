$(document).ready(function() {

    // Start by rendering the page navigation
    var PageNavigation = new App.Views.PageNavigation;

    // create 12 identical DosGame objects and insert into the test collection , each using the models default values. just for testing purposes
    // for debugging purposes, we want to name them letters of the alphabet, so that we can test sorting, splitting, etc
    /*var alphabet = 'abcdefghijklmnopqrstuvwxyz';

    var DosGames = new App.Collections.DosGames; // todo - refactor to have the collection read off Django
    for (var i = 0; i < 28; i++) {
        Dosgame = new App.Models.DosGame({title: alphabet[i % alphabet.length]}); 
        DosGames.add(Dosgame);
    }

    var DosGamesListView = new App.Views.DosGamesListView({collection: DosGames});  */

    test_dos_game = new App.Models.DosGame({
        screenshot: 'https://via.placeholder.com/320x200',
        title: 'Doom',
        description: 'Doom is a 1993 first-person shooter video game by id Software. It is considered one of the most significant and influential titles in video game history, for having helped to pioneer the now-ubiquitous first-person shooter.',
        genre: 'Action',
        publisher: 'Id Software',
        year_released: '1993',
        rating: 'ooooo',
    });

    var DosGamesDetailView = new App.Views.DosGamesDetailView({model: test_dos_game});
    console.log('done'); // just for debugging purpose
});    