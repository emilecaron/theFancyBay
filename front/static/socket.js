/*
 * A flask_websocket experiment by zozor
 */

var ws;      // web socket
var grid;    // movies div
var movie;   // movie template 


var search_movie = function(query) {
    grid.html('');
    get_websocket(function() { ws.send('SEARCH=' + query); });
};


var get_websocket = function (clbk) {
    if (!ws || ws.readyState!=1){
        ws = new WebSocket('ws://'+ document.domain +':8000/socket');
        ws.onmessage = function (msg) { grid.append(movie(JSON.parse(msg.data))); };
        ws.onopen = clbk;
    } else { clbk();}
};


$(document).ready( function(){
    // Init globals
    $.get('static/_vignette.html', function(data) {movie = _.template( data );});
    grid = $('.moviegrid');
    
    // Control binds
    $('#search-input').on('change', function(e) {search_movie($(e.currentTarget).val());} );
    $('.no-submit').submit(function(e){e.preventDefault();});
});
