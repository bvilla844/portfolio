document.addEventListener("DOMContentLoaded", () => {
  const iniciarBtn = document.getElementById("iniciarJuego");
  const jugador1Input = document.getElementById("jugador1");
  const jugador2Input = document.getElementById("jugador2");
  const faseUbicacion = document.getElementById("faseUbicacion");
  const faseAtaque = document.getElementById("faseAtaque");
  const mensajeUbicacion = document.getElementById("mensajeUbicacion");
  const direccionSelect = document.getElementById("direccion");
  const defensaJugador = document.getElementById("defensaJugador");
  const turnoActualLabel = document.getElementById("turnoActual");
  const ataqueOponente = document.getElementById("ataqueOponente");

  let jugadores = [];
  let jugadorActual = 0;
  let pasoBarcos = [5, 4, 3, 2];
  let barcoActual = 0;

  const tableros = [
    crearMatriz(9, 9),
    crearMatriz(9, 9)
  ];

  const barcosUbicados = [[], []];

  // Asignación de los nombres de los jugadores y cambio de fase
  iniciarBtn.addEventListener("click", () => {
    const nombre1 = jugador1Input.value.trim();
    const nombre2 = jugador2Input.value.trim();
    if (!nombre1 || !nombre2) {
      alert("Por favor ingresa ambos nombres.");
      return;
    }

    jugadores = [nombre1, nombre2];
    document.querySelector(".form-section").classList.add("hidden");
    faseUbicacion.classList.remove("hidden");
    renderTablero(defensaJugador, tableros[jugadorActual]);
    actualizarMensaje();

    // Mostrar nombres de los jugadores
    actualizarTurno();
  });

  function actualizarTurno() {
    // Asegurarse de que los nombres de los jugadores sean correctos
    turnoActualLabel.textContent = `¡Comienza la fase de ubicación! Es el turno de ${jugadores[jugadorActual]}`;
  }

  function crearMatriz(filas, columnas) {
    const matriz = [];
    for (let i = 0; i < filas; i++) {
      const fila = new Array(columnas).fill(null);
      matriz.push(fila);
    }
    return matriz;
  }

  function actualizarMensaje() {
    if (barcoActual < pasoBarcos.length) {
      mensajeUbicacion.textContent = `Ubica tu barco de ${pasoBarcos[barcoActual]} casillas, ${jugadores[jugadorActual]}`;
    } else {
      mensajeUbicacion.textContent = `¡Es el turno de atacar! Ahora, ${jugadores[jugadorActual]}`;
    }
  }

  function renderTablero(elemento, tablero) {
    if (!elemento) {
      console.error("El elemento no existe en el DOM");
      return;
    }
    elemento.innerHTML = "";
    tablero.forEach((fila, x) => {
      fila.forEach((celda, y) => {
        const div = document.createElement("div");
        div.dataset.x = x;  
        div.dataset.y = y;  

        // Mostrar los barcos, aciertos y fallos
        if (celda === "B") {
          div.classList.add("ship");
        } else if (celda === "X") {
          div.classList.add("hit");
        } else if (celda === "O") {
          div.classList.add("miss");
        }

        div.addEventListener("click", () => manejarUbicacion(x, y));
        elemento.appendChild(div);
      });
    });
  }

  function manejarUbicacion(x, y) {
    const longitud = pasoBarcos[barcoActual];
    const direccion = direccionSelect.value;
    const tablero = tableros[jugadorActual];

    if (puedeUbicarBarco(tablero, x, y, longitud, direccion)) {
      ubicarBarco(tablero, x, y, longitud, direccion);
      renderTablero(defensaJugador, tablero);

      barcoActual++;
      if (barcoActual >= pasoBarcos.length) {
        const barcosJugador = [];
        tablero.forEach((fila, x) => {
          fila.forEach((celda, y) => {
            if (celda === "B") {
              barcosJugador.push({ x, y });
            }
          });
        });

        enviarBarcos(jugadores[jugadorActual], barcosJugador);

        barcoActual = 0;
        jugadorActual++;

        if (jugadorActual >= jugadores.length) {
          cambiarFaseAtaque();
          return;
        }

        renderTablero(defensaJugador, tableros[jugadorActual]);
        actualizarMensaje();
      } else {
        actualizarMensaje();
      }
    } else {
      alert("No puedes ubicar el barco ahí.");
    }
  }

  function puedeUbicarBarco(tablero, x, y, longitud, direccion) {
    if (direccion === "h") {
      if (y + longitud > tablero[0].length) return false;
      for (let i = 0; i < longitud; i++) {
        if (tablero[x][y + i] !== null) return false;
      }
    } else {
      if (x + longitud > tablero.length) return false;
      for (let i = 0; i < longitud; i++) {
        if (tablero[x + i][y] !== null) return false;
      }
    }
    return true;
  }

  function ubicarBarco(tablero, x, y, longitud, direccion) {
    if (direccion === "h") {
      for (let i = 0; i < longitud; i++) {
        tablero[x][y + i] = "B";
      }
    } else {
      for (let i = 0; i < longitud; i++) {
        tablero[x + i][y] = "B";
      }
    }
  }

  function cambiarFaseAtaque() {
    faseUbicacion.classList.add("hidden");
    faseAtaque.classList.remove("hidden");
  
    // Mostrar nombres
    document.getElementById("jugador1Nombre").textContent = jugadores[0];
    document.getElementById("jugador2Nombre").textContent = jugadores[1];
  
    // Renderizar ambos tableros de ataque
    const ataqueJugador1 = document.getElementById("ataqueJugador1");
    const ataqueJugador2 = document.getElementById("ataqueJugador2");
  
    renderTableroAtaque(ataqueJugador1, 0); // Jugador 1 ataca a jugador 2
    renderTableroAtaque(ataqueJugador2, 1); // Jugador 2 ataca a jugador 1
  }

  function renderTableroAtaque(elemento, atacante) {
    const objetivo = oponente(atacante);
    const tableroObjetivo = tableros[objetivo];
  
    elemento.innerHTML = "";
    tableroObjetivo.forEach((fila, x) => {
      fila.forEach((celda, y) => {
        const div = document.createElement("div");
        div.dataset.x = x;
        div.dataset.y = y;
        div.classList.add("celda");
  
        if (celda === "X") {
          div.classList.add("hit");
        } else if (celda === "O") {
          div.classList.add("miss");
        }
  
        div.addEventListener("click", () => {
          disparar(jugadores[atacante], jugadores[objetivo], x, y, () => {
            renderTableroAtaque(elemento, atacante); // Actualizar tablero tras disparo
          });
        });
  
        elemento.appendChild(div);
      });
    });
  }
  
  function manejarDisparo(event) {
    const x = event.target.dataset.x;
    const y = event.target.dataset.y;
    if (event.target.classList.contains("ship")) {
      disparar(jugadores[jugadorActual], jugadores[oponente(jugadorActual)], x, y);
    }
  }

  function disparar(jugador, objetivo, x, y, callback) {
    fetch('/battleship/make-move/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({
        jugador: jugador,
        objetivo: objetivo,
        x: x,
        y: y
      })
    })
    .then(res => res.json())
    .then(data => {
      console.log('Movimiento realizado:', data);

      if (data.juego_terminado) {
        // Mostrar pantalla de victoria
        document.getElementById('mensaje-victoria').textContent = `🎉 ¡${data.ganador} ha ganado! 🎉`;
        document.getElementById('pantalla-victoria').style.display = 'block';
      
        // Desactivar más clics
        document.querySelectorAll('.celda').forEach(c => c.style.pointerEvents = 'none');
      
        // Contador de reinicio
        let segundos = 10;
        const contador = document.getElementById('contador-reinicio');
        const intervalo = setInterval(() => {
          segundos--;
          contador.textContent = segundos;
          if (segundos === 0) {
            clearInterval(intervalo);
            location.reload();  // Reinicia la página
          }
        }, 1000);
      
        return;
      }
         
      // Marcar en el tablero si fue acierto o fallo (opcional si backend no devuelve estado)
      const tablero = tableros[oponente(jugadores.indexOf(jugador))];
      tablero[x][y] = data.resultado === "hit" ? "X" : "O";

      const cell = document.querySelector(`[data-x="${x}"][data-y="${y}"]`);
      if (cell) {
        if (data.resultado === "hit") {
          cell.style.backgroundColor = "#FF4C4C"; // rojo
        } else {
          cell.style.backgroundColor = "#ADD8E6"; // azul claro
        }

        cell.style.pointerEvents = "none"; // opcional: desactiva clicks en esa celda
      }
      if (callback) callback();
    });
  }
  
  function oponente(jugador) {
    return jugador === 0 ? 1 : 0;
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function enviarBarcos(jugador, barcos) {
    fetch('/battleship/place-ships/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({
        jugador: jugador,
        barcos: barcos
      })
    })
    .then(res => {
      console.log('Headers:', [...res.headers.entries()]);
      return res.text(); // Cambiar temporalmente a .text() para ver la respuesta cruda
    })
    .then(text => {
      console.log('Respuesta cruda:', text);
      try {
        const json = JSON.parse(text);  // Validamos si es JSON realmente
        console.log('JSON parseado correctamente:', json);
      } catch (e) {
        console.error('Error al parsear JSON:', e);
      }
    });
  }
});
