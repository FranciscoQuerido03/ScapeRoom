document.addEventListener("DOMContentLoaded", function () {

    const socket = new WebSocket('ws://' + window.location.host + '/ws/lobby/');


        // Ouvir mensagens do WebSocket
    socket.addEventListener('message', function (event) {
        const data = JSON.parse(event.data);
        if (data.type === 'room_unlocked') {
            const { currentRoom, nextRoom, playerData } = data;

            console.log("Mensagem WebSocket recebida", data);   

            if (currentRoom && nextRoom && playerData) {
                rightAnswerSound.play();
                updateRoom(currentRoom, nextRoom, playerData);
            } else {
                console.error("Mensagem WebSocket incompleta", data);
            }
        }

        if (data.type === 'win_game') {
            window.location.href = `${data.url}/${data.message}`; // Redirect to lose page
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
            if (nextRoom === "Hall") {
                const roomInfoCount = nextRoomElement.querySelectorAll('.room_info').length;

                if (roomInfoCount === 3) {
                    socket.send(JSON.stringify({
                        type: 'win_game'
                    }));
                }

                // Append another room_info div if nextRoom is Hall
                nextRoomElement.innerHTML += `
                    <div class="room_info">
                        <img src="${playerData.skin_url}" class="character-image">
                        <p class="character-name">${playerData.name}</p>
                    </div>
                `;
            } else {
                // Overwrite content for other rooms
                nextRoomElement.innerHTML = `
                    <div class="room_info">
                        <img src="${playerData.skin_url}" class="character-image">
                        <p class="character-name">${playerData.name}</p>
                    </div>
                `;
            }
        }
    }

    ws.onclose = function () {
        console.log("Conexão WebSocket fechada");
    };
});
