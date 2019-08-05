var socket = io();
socket.on('connect', function() {
    socket.emit('text', {data: 'I\'m connected!'});
});