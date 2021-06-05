const text_box = '<div class="card-panel right" style="width: 65%; position: relative">' +
    '<div style="position: absolute; top: 0; left:3px; font-weight: bolder" class="title">{sender}</div>' +
    '{message}' +
    '</div>';

let userState = ''

const userDiv = (senderId, receiverId, name,profile) =>
 (
    `<a href="/dm/${senderId}/${receiverId}" >
    <li  id="user${receiverId}" class="contact">
        <div class="wrap">
            <span class="contact-status busy"></span>
            <img style="width: 40px;height: 40px;border-radius: 50%;object-fit: cover;" src="${profile}" alt="" />
            <div class="meta">
                <p  style="color:white;font-size:18px" class="name"><strong>${name}</strong></p>
              
            </div>
        </div>
        </li  >
   </a>`)

function scrolltoend() {
    $('.messages').stop().animate({
        scrollTop: $('.messages')[0].scrollHeight
    }, 800);
}

function send(sender, receiver, message) {
    $.post('/dm/api/messages', '{"sender": "' + sender + '", "receiver": "' + receiver + '","message": "' + message + '" }', function (data) {
        console.log(data);
        var box = text_box.replace('{sender}', "You");
        box = box.replace('{message}', message);
        $('.messages').append(box);
        scrolltoend();
    })
}

function receive() {
    $.get('/dm/api/messages/' + sender_id + '/' + receiver_id, function (data) {
        console.log(data);
        if (data.length !== 0) {
            for (var i = 0; i < data.length; i++) {
                console.log(data[i]);
                var box = text_box.replace('{sender}', data[i].sender);
                box = box.replace('{message}', data[i].message);
                box = box.replace('right', 'left blue lighten-5');
                $('.messages').append(box);
                scrolltoend();
            }
        }
    })
}

function getUsers(senderId, callback) {
    return $.get('/dm/api/users', function (data) {
        // console.log("data");
        if (userState !== JSON.stringify(data)) {
            userState = JSON.stringify(data);
            const doc = data.reduce((res, user) => {
                if (user.id === senderId) {
                    console.log(res);
                    return res
                } else {
                    return [userDiv(senderId, user.id, user.username,user.profile_image), ...res]
                }
            }, [])
            callback(doc)
        }
    })
}

function register(username, password) {
    $.post('/dm/api/users', '{"username": "' + username + '", "password": "' + password + '"}',
        function (data) {
            console.log(data);
            window.location = '/';
        }).fail(function (response) {
            $('#id_username').addClass('invalid');
        })
}