function victory() {
    const soundsDiv = document.getElementById("sounds");
    const win = soundsDiv.getAttribute("win-sound");
    const win_sound = new Audio(win);
    win_sound.play();
    confetti();
}

function Lose() {
    const soundsDiv = document.getElementById("sounds");
    const lose = soundsDiv.getAttribute("lose-sound");
    const lose_sound = new Audio(lose);
    lose_sound.play();
}

// Esperar que o documento esteja totalmente carregado
document.addEventListener("DOMContentLoaded", function() {
    // Verificar se a classe 'Vitória' existe no documento
    if (document.querySelector('.Vitória')) {
        victory();
    }
    else if (document.querySelector('.Derrota')) {
        Lose();
    }
});