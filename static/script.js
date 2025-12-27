const algorithmSelect = document.getElementById("algorithm");
const modeGroup = document.getElementById("modeGroup");
const keyGroup = document.getElementById("keyGroup");

function updateUI() {
    const alg = algorithmSelect.value;

    // RSA key istemez
    if (alg === "rsa") {
        keyGroup.style.display = "none";
        modeGroup.style.display = "none";
        return;
    }

    // AES / DES → key + mode
    if (["aes", "des"].includes(alg)) {
        keyGroup.style.display = "block";
        modeGroup.style.display = "block";
        return;
    }

    // 🔥 MANUEL ALGORİTMALAR → SADECE KEY
    keyGroup.style.display = "block";
    modeGroup.style.display = "none";
}

algorithmSelect.addEventListener("change", updateUI);
updateUI();

document.getElementById("cryptoForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
        message: document.getElementById("message").value,
        algorithm: algorithmSelect.value,
        operation: document.getElementById("operation").value,
        key: document.getElementById("key").value || null
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
