document.addEventListener("DOMContentLoaded", function () {

    const socket = new WebSocket('ws://' + window.location.host + '/ws/lobby/');


        // Ouvir mensagens do WebSocket
    socket.addEventListener('message', function (event) {
        const data = JSON.parse(event.data);
        if (data.type === 'room_unlocked') {
            const { currentRoom, nextRoom, playerData } = data;

            console.log("Mensagem WebSocket recebida", data);   

            if (currentRoom && nextRoom && playerData) {
                updateRoom(currentRoom, nextRoom, playerData);
            } else {
                console.error("Mensagem WebSocket incompleta", data);
            }
        }
    }); 

    function updateRoom(currentRoom, nextRoom, playerData) {
        // Seleciona a sala atual e remove o jogador dela
        const currentRoomElement = document.getElementById(currentRoom);
        if (currentRoomElement) {
            currentRoomElement.innerHTML = ''; // Limpa a sala atual
        }

        // Seleciona a próxima sala e adiciona o jogador
        const nextRoomElement = document.getElementById(nextRoom);
        if (nextRoomElement) {
            nextRoomElement.innerHTML = `
                <div class="room_info">
                    <img src="${playerData.skin_url}" class="character-image">
                    <p class="character-name">${playerData.name}</p>
                </div>
            `;
        }
    }

    ws.onclose = function () {
        console.log("Conexão WebSocket fechada");
    };
});
