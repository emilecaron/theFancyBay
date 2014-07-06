/*
 * A flask_websocket experiment by zozor
 */

$(document).ready( function(){
    // prepare movie template
    var movie;    
    $.get('static/_vignette.html', function( data){
        movie = _.template( data );
    })
    
    // setup websocket
    var grid = $('.moviegrid');
    var ws = new WebSocket('ws://'+ document.domain +':8000/echo');
    ws.onopen = function () {
        console.log('Websocket is up and running');
        ws.send('matrix');
    };
    ws.onerror = function (err) {
        console.log('Websocket Error : '+err);
    };

    // Display movies on receive
    ws.onmessage = function (msg) {
        obj = JSON.parse(msg.data)
        console.log(obj)
        grid.append(movie(obj));
    }
});
