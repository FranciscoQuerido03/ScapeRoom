function submitForm(event) {
    event.preventDefault(); 

    const formData = new FormData(event.target); 

    fetch("http://localhost:8000/register/", {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) 
    .then(data => {
        document.cookie = `player_id=${data.player}`;

        window.location.href = 'http://localhost:8000/wait_room/';
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Ocorreu um erro ao processar a solicitação.');
    });
}
