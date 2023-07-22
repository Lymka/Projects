
document.getElementById("myForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch('/save_data', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Ошибка:', error));
});
