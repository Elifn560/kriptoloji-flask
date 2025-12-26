document.getElementById('cryptoForm').addEventListener('submit', async function(e){
    e.preventDefault();
    const message = document.getElementById('message').value;
    const algorithm = document.getElementById('algorithm').value;
    const mode = document.getElementById('mode').value;
    const operation = document.getElementById('operation').value;

    const res = await fetch('/send', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message, algorithm, mode, operation})
    });

    const data = await res.json();
    document.getElementById('response').innerText = JSON.stringify(data, null, 2);
});
