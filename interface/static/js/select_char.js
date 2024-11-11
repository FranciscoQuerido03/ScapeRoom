function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

const socket = new WebSocket('ws://' + window.location.host + '/ws/lobby/');

socket.addEventListener('open', function() {
    console.log('WebSocket connection established');
});

// Ouvir mensagens do WebSocket
socket.addEventListener('message', function (event) {
    const data = JSON.parse(event.data);
    console.log('Mensagem do servidor:', data);  // Verificar o conteúdo da mensagem

    // Verificar se a mensagem indica que o jogo começou
    if (data.type === 'character_selected') {
        
    }
});

  document.querySelectorAll('.character-btn').forEach(button => {
    button.addEventListener('click', () => {
      const characterId = button.getAttribute('data-char-id');
      fetch("http://localhost:8000/charAtribute/", {
        method: 'POST',
        body: JSON.stringify({characterId: characterId, playerId: getCookie('player_id')}),
    }).then(data => {
      window.location.href = 'http://localhost:8000/wait_room/';
  })
    });
  });