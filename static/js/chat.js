

let userState = ''

const userDiv = (senderId, receiverId, name, online) =>
    (`<a href="/chat/${senderId}/${receiverId}" id="user${receiverId}" class="collection-item row">
                    <img src="https://frontend-1.adjust.com/new-assets/images/site-images/interface/user.svg" class="col s2">
                    <div class="col s10">
                    <span class="title" style="font-weight: bolder">${name}</span>
                    <span style="color: ${online ? 'green' : 'red'}; float: right">${online ? 'online' : 'offline'}</span>
                    </div>
                </a>`)

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

function send_chatroom(sender, chatroom_id, message){
    $.post('/api/chat-room/send-messages/', '{"sender": "' + sender + '", "chat_room": "' + chatroom_id + '","message": "' + message+ '" }', function(data) {
        var box = text_box.replace('{sender}', "You");
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
            for (var i = 0; i < data.length; i++) {
                var box = text_box.replace('{sender}', data[i].sender);
                box = box.replace('{message}', data[i].message);
                box = box.replace('right', 'left blue lighten-5');
                $('#board').append(box);
                scrolltoend();
            }
        }
    })
}

function getUsers(senderId, callback) {
    return $.get('/api/users', function (data) {
        if (userState !== JSON.stringify(data)) {
            userState = JSON.stringify(data);
            const doc = data.reduce((res, user) => {
                if (user.id === senderId) {
                    return res
                } else {
                    return [userDiv(senderId, user.id, user.username, user.online), ...res]
                }
            }, [])
            callback(doc)
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
