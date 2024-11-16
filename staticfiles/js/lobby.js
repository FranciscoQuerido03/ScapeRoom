const playersList = document.getElementById('players');

const chatSocket = new WebSocket(
    (window.location.protocol === 'https:' ? 'wss://' : 'ws://') + 
    window.location.host + 
    '/ws/lobby/'
);

// Flag para saber se a redireção foi realizada
let redirectToSharedScreen = false;

chatSocket.onopen = function() {
    console.log('WebSocket connection established');
}


chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

chatSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    if (data.type === 'player_joined') {
        const playerName = data.player_name;

        // Verifica se a mensagem de lista vazia está presente e remove-a
        const emptyMessage = playersList.querySelector('li');
        if (emptyMessage && emptyMessage.textContent === 'No players have joined yet.') {
            playersList.removeChild(emptyMessage);
        }

        // Adiciona o novo jogador
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

        // Se a lista estiver vazia depois da remoção, adiciona a mensagem de lista vazia
        if (playersList.children.length === 0) {
            const li = document.createElement('li');
            li.textContent = 'No players have joined yet.';
            playersList.appendChild(li);
        }
    }
};


function onClick() {
    const message = JSON.stringify({ type: 'start_game' });
    chatSocket.send(message);
}
