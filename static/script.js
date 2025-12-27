const algorithmSelect = document.getElementById("algorithm");
const modeGroup = document.getElementById("modeGroup");
const keyGroup = document.getElementById("keyGroup");

function updateUI() {
    const alg = algorithmSelect.value;

    if (["aes", "des", "rsa"].includes(alg)) {
        modeGroup.style.display = "block";
        keyGroup.style.display = "block";
    } else {
        modeGroup.style.display = "none";
        keyGroup.style.display = "none";
    }
}

algorithmSelect.addEventListener("change", updateUI);
updateUI(); // sayfa açılınca

document.getElementById("cryptoForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
        message: document.getElementById("message").value,
        algorithm: algorithmSelect.value,
        mode: document.getElementById("mode").value,
        operation: document.getElementById("operation").value,
        key: document.getElementById("key").value
    };

    const res = await fetch("/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const data = await res.json();
    document.getElementById("response").innerText =
        JSON.stringify(data, null, 2);
});
