// (esversion: 6)


$(document).ready(function() {
    var d = $('#chatbox');
    d.scrollTop(d.prop("scrollHeight"));
})

var socket = io();

socket.on('connect', function() {
    console.log( "Connected..." );
} );

socket.on( 'disconnect', function() {
    console.log( "Disconnected..." );
} );

socket.on( 'msg-recv', function(data) {
        if (mid == data.mid) {
            if (data.uid == uid) {
                drop_n( data.html.sent )
            }
            else {
                drop_n( data.html.recv )
                $('#alert-tone')[0].play();
            }
            // $('#chats').html( data.html );
            var d = $('#chatbox');
            d.scrollTop(d.prop("scrollHeight"));
        }
    }
);

socket.on( "del-watcher", function(data) {
    if (klass == data.klass) {
        $("#stock-"+data._id).remove();
    }
});

function del_watcher( id ) {
    socket.emit( "del-watcher", data = {"klass": klass, "_id": id} )
}

function sendMsg () {
    $('#sendBtn').html(`<span class="spinner-grow spinner-grow-sm" role="status"></span>`)
    var msg = $( '#msg' ).val();
    var replyto = $( '#replyto' ).val();
    $( '#msg' ).val( "" )
    $( '#replyto' ).val( "0" )
    socket.emit( "msg-send", data = { "mid": mid, "msg": msg, "replyto": replyto } );
    $('.fa-reply').css( "color", "gray" )
    $('#sendBtn').html(`<i class="fas fa-paper-plane"></i>`)
}