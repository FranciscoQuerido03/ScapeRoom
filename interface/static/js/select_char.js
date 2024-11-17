function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
function disableButton(character_id) {
  const button = document.getElementById("char" + character_id);
  if (button) { // Verifica se o botão existe
      button.disabled = true;
  }
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
  if (data.type === 'select_character') {
      const character_id = data.character_id;
      disableButton(character_id); // Corrigido o nome da função
  }
});

// Desabilitar botões de personagens que já foram selecionados
document.querySelectorAll('.character-btn').forEach(button => {
  button.addEventListener('click', (event) => {
      if (button.disabled) {
          event.preventDefault();
          event.stopPropagation();
      }
  });
});


document.querySelectorAll('.character-btn').forEach(button => {
  button.addEventListener('click', async () => {

    try {
      const characterId = button.getAttribute('data-char-id');
      const playerId = getCookie('player_id');
      
      const response = await fetch("http://192.168.1.112:8000/charAtribute/", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          characterId: characterId,
          playerId: playerId,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('data: ', data);

        document.cookie = `room_name=${data.room_name}; path=/;`;
        document.cookie = `key=${data.key}; path=/;`;

        const url = `http://192.168.1.112:8000/char_specs/${data.character_acao}/${data.character_image}`;
        window.location.href = url;
      } else {
        console.error('Erro ao selecionar personagem:', response.statusText);
      }
    } catch (error) {
      console.error('Erro de rede ou outro:', error);
    }
  });
});
