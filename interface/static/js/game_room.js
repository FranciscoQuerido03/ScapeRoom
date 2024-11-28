// Estabelecer conexão WebSocket
const socket = new WebSocket('ws://' + window.location.host + '/ws/lobby/');

socket.addEventListener('open', function() {
    console.log('WebSocket connection established');
});

// Ouvir mensagens do WebSocket
socket.addEventListener('message', function (event) {
    const data = JSON.parse(event.data);

    if (data.type === 'lose_game') {
        window.location.href = `${data.url}/${data.message}`; // Redirect to lose page
    }

    if (data.type === 'win_game') {
        window.location.href = `${data.url}/${data.message}`; // Redirect to lose page
    }
});

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = "flex";
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = "none";
    }
}

window.onclick = function(event) {
    const modals = document.getElementsByClassName("modal");
    for (let i = 0; i < modals.length; i++) {
        if (event.target === modals[i]) {
            modals[i].style.display = "none";
        }
    }
};

function closeModalOnClick(event) {
    event.preventDefault();

    const modals = document.getElementsByClassName("modal");
    for (let i = 0; i < modals.length; i++) {
        modals[i].style.display = "none";
    }
}

window.onload = function() {
    const modals = document.getElementsByClassName("modal");
    for (let i = 0; i < modals.length; i++) {
        modals[i].style.display = "none";
    }
};

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Função para envio da resposta do puzzle
async function submitPuzzleAnswer(event) {
    event.preventDefault();

    const answer = document.getElementById("puzzleAnswer").value;
    const feedbackMessage = document.getElementById("feedbackMessage");

    let room_name = getCookie("room_name");
    let player_id = getCookie("player_id");

    // Enviar a resposta ao servidor
    const response = await fetch("/check_answer/", {
        method: "POST",
        body: JSON.stringify({
            room_name: room_name,
            answer: answer,
            player_id: player_id,
        })
    });

    const result = await response.json();
    console.log(result);
    // Exibir feedback da resposta
    if (result.success) {
        feedbackMessage.textContent = "Resposta correta!";
        feedbackMessage.style.color = "green";

        let nextRoom = result.context.room_name;
        let key = result.context.key;
        
        document.cookie = `room_name=${nextRoom}; path=/;`;
        document.cookie = `key=${key}; path=/;`;
        console.log(result);
        if (nextRoom) {
            setTimeout(() => {
                window.location.href = `/game/${nextRoom}/${key}`;
            }, 1000);
        }

    } else {
        feedbackMessage.textContent = "Resposta incorreta, tente novamente.";
        feedbackMessage.style.color = "red";
    }
}

// Função auxiliar para obter o token CSRF
function getCSRFToken() {
    const cookieValue = document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
    return cookieValue;
}

