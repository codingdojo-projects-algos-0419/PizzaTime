/*
Internal script for Pizza time
*/
$(document).ready(function() {
     // $.get('/nav', function(nav){
     //      $('#nav').html(nav)
     // })
     //connect to the socket server.
     var socket = io.connect('http://' + document.domain + ':' + location.port + '/restdash');
     //receive details from server
     socket.on('neworder', function(msg) {
          console.log("Received order" + msg);
     });
})
