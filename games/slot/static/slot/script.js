let balance = 100.0;

function playSlot() {
    const betInput = document.getElementById("betAmount");
    const bet = parseFloat(betInput.value);
    const errorDiv = document.getElementById("error");
    const rowDisplay = document.getElementById("row");
    errorDiv.textContent = "";

    if (isNaN(bet) || bet <= 0) {
        errorDiv.textContent = "Please enter a valid bet.";
        return;
    }

    if (bet > balance) {
        errorDiv.textContent = "Insufficient balance.";
        return;
    }

    // Simula animación inicial
    rowDisplay.textContent = "🎰 | 🎰 | 🎰";
    rowDisplay.classList.add("animate");

    setTimeout(() => {
        fetch('/slot/api/play/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                balance: balance,
                bet: bet
            })
        })
        .then(response => response.json())
        .then(data => {
            balance = data.balance;

            document.getElementById("balance").textContent = balance.toFixed(2);
            document.getElementById("row").textContent = data.row.join(" | ");
            document.getElementById("payout").textContent = data.payout;

            // Quitar animación después de mostrar resultado
            rowDisplay.classList.remove("animate");

            if (balance <= 0) {
                errorDiv.textContent = "Game over. You ran out of money.";
            }
        });
    }, 700); // Tiempo de "giro"
}

// Obtener CSRF token de las cookies (Django lo necesita)
function getCSRFToken() {
    const name = "csrftoken=";
    const decodedCookies = decodeURIComponent(document.cookie);
    const cookies = decodedCookies.split(';');
    for (let cookie of cookies) {
        while (cookie.charAt(0) === ' ') cookie = cookie.substring(1);
        if (cookie.indexOf(name) === 0) return cookie.substring(name.length, cookie.length);
    }
    return "";
}
