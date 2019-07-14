var ws = new WebSocket("ws://127.0.0.1:5678"),
    messages = document.createElement('ul');
ws.onmessage = function (event) {
    var messages = document.getElementsByTagName('ul')[0],
        message = document.createElement('li'),
        content = document.createTextNode(event.data);
    message.appendChild(content);
    messages.appendChild(message);
};
document.body.appendChild(messages);

testButton.onclick = () => {
    const message = {
        title: "test",
        data: "the data"
    }
    ws.send(JSON.stringify(message))
}


const handshake_message = {
    title: "handshake",
    data: ""
}

setTimeout(() => {
    ws.send(JSON.stringify(handshake_message))
}, 1000);
