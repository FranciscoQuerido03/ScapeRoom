
const leftArrow = document.getElementById('left_arrow');
if (leftArrow) {
    leftArrow.addEventListener('click', () => {
        console.log('Clicou na seta esquerda');
        fetch('/render_visited/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                player: getCookie('player_id'),
                direcao: 'esquerda' })
        })
        .then(response => response.json())  
        .then(data => {
            if (data.redirect_url) {
                window.location.href = data.redirect_url;  // Redireciona para a nova sala
            }
        })
        .catch(error => console.error('Erro:', error));
    });
}


const rightArrow = document.getElementById('right_arrow');
if (rightArrow) {
    rightArrow.addEventListener('click', () => {
        console.log('Clicou na seta direita');

        fetch('/render_visited/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                player: getCookie('player_id'),
                direcao: 'direita'
            })
        })
        .then(response => response.json()) 
        .then(data => {
            if (data.redirect_url) {
                window.location.href = data.redirect_url;  // Redireciona para a sala
            }
        })
        .catch(error => console.error('Erro:', error));
    });
}
