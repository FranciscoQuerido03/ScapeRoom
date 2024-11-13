// Função para pegar o valor de um cookie específico pelo nome
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Estabelecer conexão WebSocket
const socket = new WebSocket('ws://' + window.location.host + '/ws/lobby/');

socket.addEventListener('open', function() {
    console.log('WebSocket connection established');
});

// Ouvir mensagens do WebSocket
socket.addEventListener('message', function (event) {
    const data = JSON.parse(event.data);
    console.log('Mensagem do servidor:', data);

    if (data.type === 'start_game') {
        const roomName = getCookie('room_name');
        console.log('Iniciando redirecionamento para /choose_char');
        window.location.href = `/game/${roomName}`;
    }
});

// Adicionar listener para erros
socket.addEventListener('error', function(error) {
    console.error('WebSocket error:', error);
});

// Listener para fechamento da conexão WebSocket
socket.addEventListener('close', function(event) {
    console.error('WebSocket closed:', event);
});


