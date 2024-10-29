function submitForm(event) {
    event.preventDefault(); 

    const formData = new FormData(event.target); 


    fetch("http://localhost:8000/register/", {
        method: 'POST',
        body: formData
    })
    .then(data => {
        window.location.href = 'http://localhost:8000/wait_room/';
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Ocorreu um erro ao processar a solicitacao.');
    });
}
