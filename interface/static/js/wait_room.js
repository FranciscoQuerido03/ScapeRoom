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
    console.log('Mensagem do servidor:', data);  // Verificar o conteúdo da mensagem

    // Verificar se a mensagem indica que o jogo começou
    if (data.type === 'start_game') {
        console.log('Iniciando redirecionamento para /choose_char');
        window.location.href = '/choose_char/';
    }
});

// Adicionar listener para erros
socket.addEventListener('error', function(error) {
    console.error('WebSocket error:', error);
});

// Listener para fechamento da conexão WebSocket
socket.addEventListener('close', function(event) {
    console.error('WebSocket closed:', event);
    sendDisconnectRequest();
});

// Adicionar evento `beforeunload` para enviar a requisição antes da página ser descarregada
window.addEventListener('beforeunload', sendDisconnectRequest);

// Função para enviar requisição de desconexão ao backend
function sendDisconnectRequest() {
    const playerId = getCookie('player_id'); // Altere 'player_id' para o nome correto do cookie

    if (playerId) {
        navigator.sendBeacon('http://localhost:8000/leave_game/', JSON.stringify({ player_id: playerId }));
        console.log('ID do jogador enviado ao backend usando sendBeacon');
    } else {
        console.error('ID do jogador não encontrado nos cookies');
    }
}
