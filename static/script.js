const algorithmSelect = document.getElementById("algorithm");
const modeSelect = document.getElementById("mode");
const modeGroup = document.getElementById("modeGroup");
const keyGroup = document.getElementById("keyGroup");
const keyInput = document.getElementById("key");

function updateUI() {
    const alg = algorithmSelect.value;

    // RSA → key ve mode yok
    if (alg === "rsa") {
        keyGroup.style.display = "none";
        modeGroup.style.display = "none";
        return;
    }

    // AES / DES → key + mode
    if (alg === "aes" || alg === "des") {
        keyGroup.style.display = "block";
        modeGroup.style.display = "block";
        return;
    }

    // KLASİK (manuel) → sadece key
    keyGroup.style.display = "block";
    modeGroup.style.display = "none";
}

algorithmSelect.addEventListener("change", updateUI);
updateUI();

document.getElementById("cryptoForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const alg = algorithmSelect.value;
    const key = keyInput.value.trim();

    // 🔴 KRİTİK: manuel algoritmalar key'siz gönderilmesin
    if (alg !== "rsa" && key === "") {
        alert("Bu algoritma için key girmelisin!");
        return;
    }

    const payload = {
        message: document.getElementById("message").value,
        algorithm: alg,
        operation: document.getElementById("operation").value,
        key: key
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
