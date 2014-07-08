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
        ws.onmessage = read_msg;
        ws.onopen = clbk;
    } else { clbk();}
};

var read_msg = function (msg){
    json = JSON.parse(msg.data);
    if ('control' in json){
        console.log(json.control.msg);
    } else {
        grid.append(movie(json));
    }
}


$(document).ready( function(){
    // Init globals
    $.get('static/_vignette.html', function(data) {movie = _.template( data );});
    grid = $('.moviegrid');
    
    // Control binds
    $('#search-input').on('change', function(e) {search_movie($(e.currentTarget).val());} );
    
});
