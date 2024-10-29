// Tempo inicial em segundos
let timeLeft = 300;

// Criar o elemento
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

// Atualizar o contador a cada segundo|
function startCountdown() {
    const countdownInterval = setInterval(() => {
        timeLeft--;
        countdownDisplay.textContent = `${formatTime(timeLeft)}`;

        // Quando o tempo se esgota
        if (timeLeft <= 0) {
            clearInterval(countdownInterval);
            countdownDisplay.textContent = "Tempo esgotado!";
            document.getElementById("start-game").disabled = true;
        }
    }, 1000);
}

// Inicia a contagem decrescente
startCountdown();
