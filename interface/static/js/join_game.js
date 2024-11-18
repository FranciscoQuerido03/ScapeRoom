function submitForm(event) {
    event.preventDefault(); 

    const formData = new FormData(event.target); 

    fetch("http://192.168.1.127:8000/register/", {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) 
    .then(data => {
        console.log(data);

        document.cookie = `player_id=${data.player}`;
        
        setTimeout(() => {
            window.location.href = 'http://192.168.1.127:8000/select_char/';
        }, 100); 
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Ocorreu um erro ao processar a solicitação.');
    });
}
