

let userState = ''

function scrolltoend() {
    $('#board').stop().animate({
        scrollTop: $('#board')[0].scrollHeight
    }, 800);
}

const text_box = '<div class="card-panel right" style="width: 75%; position: relative">' +
    '<div style="position: absolute; top: 0; left:3px; font-weight: bolder" class="title">{sender}</div>' +
    '{message}' +
    '</div>';

function send(sender, receiver, message) {
    $.post('/api/messages/', '{"sender": "' + sender + '", "receiver": "' + receiver + '","message": "' + message + '" }', function (data) {
        var box = text_box.replace('{sender}', "You");
        box = box.replace('{message}', message);
        $('#board').append(box);
        scrolltoend();
    })
}

function send_chatroom(sender_username, sender_anon, chatroom_id, message, is_anonymous){
    var display_name = sender_username;
    var static_str = "true";
    if(is_anonymous == static_str){
        display_name = sender_anon;
    }
    $.post('/api/chat-room/send-messages/', '{"sender": "' + sender_username + '", "chat_room": "' + chatroom_id + '","message": "' + message+ '","anonymous": "' + is_anonymous+ '" ,"display_name": "' + display_name + '"}', function(data) {
        var static_str = "true";
        var sender = "You";
        if(is_anonymous == static_str){
            sender = sender_anon;
        }
        var box = text_box.replace('{sender}', sender);
        box = box.replace('{message}', message);
        $('#board').append(box);
        scrolltoend();
    })
}

function receive() {
    var url = '';
    if(typeof chatroom_id === 'undefined'){
        url = '/api/messages/' + sender_id + '/' + receiver_id + '/';
    }
    else{
        url = '/api/messages/'+chatroom_id+'/';
    }
    $.get(url, function (data) {
        if (data.length !== 0) {
            if(typeof chatroom_id === 'undefined'){
                for (var i = 0; i < data.length; i++) {
                    var box = text_box.replace('{sender}', data[i].sender);
                    box = box.replace('{message}', data[i].message);
                    box = box.replace('right', 'left blue lighten-5');
                    $('#board').append(box);
                    scrolltoend();
                }
            }
            else{
                for (var i = 0; i < data.length; i++) {
                    var box = text_box.replace('{sender}', data[i].display_name);
                    box = box.replace('{message}', data[i].message);
                    box = box.replace('right', 'left blue lighten-5');
                    $('#board').append(box);
                    scrolltoend();
                }
            }

        }
    })
}

function register(username, password) {
    $.post('/api/users/', '{"username": "' + username + '", "password": "' + password + '"}',
        function (data) {
            window.location = '/';
        }).fail(function (response) {
            $('#id_username').addClass('invalid');
        })
}
