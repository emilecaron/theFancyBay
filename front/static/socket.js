/*
 * A flask_websocket experiment by zozor
 */

var ws;
console.log('Running js')

$(document).ready( function(){
    // prepare movie template
    var movie;    
    $.get('static/_vignette.html', function( data){
        movie = _.template( data );
    })
    
    // setup websocket
    var grid = $('.moviegrid');
    ws = new WebSocket('ws://'+ document.domain +':8000/socket');
    ws.onopen = function () {
        console.log('Websocket is up and running');
        //load top 100 on startup
        ws.send('');
    };
    ws.onerror = function (err) {
        console.log('Websocket Error : '+err);
    };

    // Display movies on receive
    ws.onmessage = function (msg) {
        obj = JSON.parse(msg.data)
        grid.append(movie(obj));
    }
});
