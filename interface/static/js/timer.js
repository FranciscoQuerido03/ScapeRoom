// Tempo inicial em segundos
let startTime = 120;
let timeLeft = startTime;

const soundsDiv = document.getElementById("sounds");
const startSoundPath = soundsDiv.getAttribute("data-start-sound");
const halfTimeSoundPath = soundsDiv.getAttribute("data-half-sound");
const oneMinuteSoundPath = soundsDiv.getAttribute("data-one-minute-sound");

// Carregar os sons WAV usando os caminhos passados
const startSound = new Audio(startSoundPath); // Som de início
const halfTimeSound = new Audio(halfTimeSoundPath); // Som de meio tempo
const oneMinuteSound = new Audio(oneMinuteSoundPath); // Som de 1 minuto

// Verifique se os sons estão carregados corretamente
startSound.onload = () => console.log("Som de início carregado.");
halfTimeSound.onload = () => console.log("Som de meio tempo carregado.");
oneMinuteSound.onload = () => console.log("Som de 1 minuto carregado.");

// Criar o elemento do timer
const countdownDisplay = document.createElement("p");
countdownDisplay.id = "countdown";
countdownDisplay.style.fontSize = "1.5rem";
countdownDisplay.style.marginTop = "20px";
document.querySelector(".timer").appendChild(countdownDisplay);

// Formatar o tempo como "mm:ss"
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

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
        }
    }, 1000);
}

// Inicia a contagem decrescente
startCountdown();
