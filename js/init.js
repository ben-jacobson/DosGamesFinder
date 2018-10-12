$(document).ready(function() {

    // Start by rendering the page navigation
    var PageNavigation = new App.Views.PageNavigation;

    // create 12 identical DosGame objects and insert into the test collection , each using the models default values. just for testing purposes
    // for debugging purposes, we want to name them letters of the alphabet, so that we can test sorting, splitting, etc
    var alphabet = 'abcdefghijklmnopqrstuvwxyz';

    var DosGames = new App.Collections.DosGames; // todo - refactor to have the collection read off Django
    for (var i = 0; i < 28; i++) {
        Dosgame = new App.Models.DosGame({title: alphabet[i % alphabet.length]}); 
        DosGames.add(Dosgame);
    }

    var DosGamesListView = new App.Views.DosGamesListView({collection: DosGames});
    console.log('done'); // just for debugging purpose
});    