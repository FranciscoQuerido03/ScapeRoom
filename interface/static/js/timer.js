// Tempo inicial em segundos
let startTime = 300;
let timeLeft = startTime;

const soundsDiv = document.getElementById("sounds");
const startSoundPath = soundsDiv.getAttribute("data-start-sound");
const halfTimeSoundPath = soundsDiv.getAttribute("data-half-sound");
const oneMinuteSoundPath = soundsDiv.getAttribute("data-one-minute-sound");
const wrongAnswerSoundPath = soundsDiv.getAttribute("data-wrong-answer-sound");
const rightAnswerSoundPath = soundsDiv.getAttribute("data-right-answer-sound");

// Carregar os sons WAV usando os caminhos passados
const startSound = new Audio(startSoundPath); // Som de início
const halfTimeSound = new Audio(halfTimeSoundPath); // Som de meio tempo
const oneMinuteSound = new Audio(oneMinuteSoundPath); // Som de 1 minuto
const wrongAnswerSound = new Audio(wrongAnswerSoundPath); // Som de resposta errada
const rightAnswerSound = new Audio(rightAnswerSoundPath); // Som de resposta correta

// Criar o elemento do timer
const countdownDisplay = document.createElement("p");
countdownDisplay.id = "countdown";
document.querySelector(".timer").appendChild(countdownDisplay);

// Formatar o tempo como "mm:ss"
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

const socket = new WebSocket('ws://' + window.location.host + '/ws/lobby/');

socket.addEventListener('open', function() {
  console.log('WebSocket connection established');
});

// Ouvir mensagens do WebSocket
socket.addEventListener('message', function (event) {
    const data = JSON.parse(event.data);

    // Verificar se a mensagem indica que a resposta foi errada
    if (data.type === 'wrong_answer') {
        const previousTimeLeft = timeLeft;
        timeLeft -= 10;
        countdownDisplay.textContent = `${formatTime(timeLeft)}`;

        // Tocar som de resposta errada
        wrongAnswerSound.play();

        // Verificar se passou pela metade do tempo com o desconto
        if (previousTimeLeft > startTime / 2 && timeLeft <= startTime / 2) {
            halfTimeSound.play();
        }

        // Verificar se passou pelo limite de 1 minuto
        if (previousTimeLeft > 60 && timeLeft <= 60) {
            oneMinuteSound.play();
        }

        // Verificar se o tempo se esgotou
        if (timeLeft <= 0) {
            timeLeft = 0;
            countdownDisplay.textContent = "Tempo esgotado!";
            clearInterval(countdownInterval);
        }
    }

    if(data.type === 'right_answer'){
        rightAnswerSound.play();
    }

    if (data.type === 'lose_game') {
        window.location.href = `${data.url}/${data.message}`; // Redirect to lose page
    }
});

// Atualiza o display inicial
countdownDisplay.textContent = `${formatTime(timeLeft)}`;

// Função para iniciar a contagem regressiva
function startCountdown() {
    const countdownInterval = setInterval(() => {
        timeLeft--;
        countdownDisplay.textContent = `${formatTime(timeLeft)}`;

        // Tocar som quando o timer começar (primeira vez, no segundo 119)
        if (timeLeft === startTime - 1) {
            startSound.play();
        }

        // Tocar som na metade do tempo
        if (timeLeft === startTime / 2) {
            halfTimeSound.play();
        }

        // Tocar som quando faltar 1 minuto
        if (timeLeft === 60) {
            oneMinuteSound.play();
        }

        // Quando o tempo se esgota
        if (timeLeft <= 0) {
            clearInterval(countdownInterval);
            countdownDisplay.textContent = "Tempo esgotado!";
            // Desativa o botão "start-game" se existir
            const startButton = document.getElementById("start-game");
            if (startButton) {
                startButton.disabled = true;
            }

            socket.send(JSON.stringify({
                type: 'lose_game'
            }));
        }
    }, 1000);
}

// Inicia a contagem decrescente
startCountdown();
