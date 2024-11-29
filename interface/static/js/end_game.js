function victory() {
    const soundsDiv = document.getElementById("sounds");
    const win = soundsDiv.getAttribute("win-sound");
    const win_sound = new Audio(win);
    win_sound.play();
    confetti();

    const elementoTexto = document.querySelector(".Vitória");
    if (elementoTexto) {
        elementoTexto.classList.add("vitoria-animacao");

        setTimeout(() => {
            elementoTexto.classList.remove("vitoria-animacao");
        }, 2000); 
    }
}

function Lose() {
    const elementoTexto = document.querySelector(".Derrota"); 
    
    if (elementoTexto) {
        const textoCompleto = elementoTexto.textContent + "..."; 
        let indice = 0;
        elementoTexto.textContent = ""; 

        function escreverTexto() {
            if (indice < textoCompleto.length) {
                elementoTexto.textContent += textoCompleto.charAt(indice);
                indice++;
                setTimeout(escreverTexto, 100);
            }
        }

        escreverTexto(); 
    }

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