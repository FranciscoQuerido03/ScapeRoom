const playersList = document.getElementById('players');
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/lobby/');

// Flag para saber se a redireção foi realizada
let redirectToSharedScreen = false;

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

chatSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    if (data.type === 'player_joined') {
        const playerName = data.player_name;
        const li = document.createElement('li');
        li.textContent = playerName;
        playersList.appendChild(li);
    } else if (data.type === 'start_game') {
        window.location.href = '/shared_screen/';
    } else if (data.type === 'player_left') {
        const playerName = data.player_name;

        const playerItems = playersList.getElementsByTagName('li');
        for (let i = 0; i < playerItems.length; i++) {
            if (playerItems[i].textContent === playerName) {
                playersList.removeChild(playerItems[i]);
                break; 
            }
        }
    }
};


function onClick() {
    const message = JSON.stringify({ type: 'start_game' });
    chatSocket.send(message);
}
