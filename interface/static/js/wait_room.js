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
        console.log('Iniciando redirecionamento para /chose_character');
        window.location.href = '/choose_char/';
    }
});

// Adicionar listener para erros
socket.addEventListener('error', function(error) {
    console.error('WebSocket error:', error);
});

// Adicionar listener para fechamento da conexão
socket.addEventListener('close', function(event) {
    console.error('WebSocket closed:', event);
});
