function submitForm(event) {
    event.preventDefault(); 

    const formData = new FormData(event.target); 

    fetch("https://scaperoom.onrender.com/register/", {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) 
    .then(data => {
        console.log(data);

        document.cookie = `player_id=${data.player}`;
        
        setTimeout(() => {
            window.location.href = 'https://scaperoom.onrender.com/select_char/';
        }, 100); 
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Ocorreu um erro ao processar a solicitação.');
    });
}
