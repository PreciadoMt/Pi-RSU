document.addEventListener("DOMContentLoaded", function() {
    // Elementos del DOM
    const DOM = {
        formulario: document.getElementById("formulario-test"),
        preguntas: document.querySelectorAll(".pregunta"),
        opciones: document.querySelectorAll(".opcion"),
        btnContinuar: document.getElementById("btn-continuar"),
        btnVolver: document.getElementById("btn-volver"),
        barraProgreso: document.getElementById("progreso"),
        contadorPreguntas: document.getElementById("contador-preguntas")
    };

    // Estado de la aplicación
    const estado = {
        preguntaActual: 0,
        respuestas: {},
        totalPreguntas: DOM.preguntas.length
    };

    // Funciones
    function actualizarProgreso() {
        const porcentaje = ((estado.preguntaActual + 1) / estado.totalPreguntas) * 100;
        DOM.barraProgreso.style.width = `${porcentaje}%`;
        DOM.contadorPreguntas.textContent = `${estado.preguntaActual + 1}/${estado.totalPreguntas}`;
    }

    function mostrarPregunta(indice) {
        // Ocultar todas las preguntas
        DOM.preguntas.forEach(pregunta => {
            pregunta.classList.remove("visible");
        });

        // Mostrar solo la pregunta actual
        DOM.preguntas[indice].classList.add("visible");

        // Actualizar botones de navegación
        DOM.btnVolver.style.display = indice === 0 ? "none" : "flex";
        DOM.btnContinuar.textContent = indice === estado.totalPreguntas - 1 ? "Enviar resultados" : "Continuar";
        DOM.btnContinuar.disabled = !estado.respuestas[indice];

        // Actualizar progreso
        actualizarProgreso();
    }

    function guardarRespuesta(indice, respuesta) {
        estado.respuestas[indice] = respuesta;
        DOM.btnContinuar.disabled = false;
    }

    function siguientePregunta() {
        if (estado.preguntaActual < estado.totalPreguntas - 1) {
            estado.preguntaActual++;
            mostrarPregunta(estado.preguntaActual);
        } else {
            enviarResultados();
        }
    }

    function preguntaAnterior() {
        if (estado.preguntaActual > 0) {
            estado.preguntaActual--;
            mostrarPregunta(estado.preguntaActual);
        }
    }

    function enviarResultados() {
        console.log("Respuestas del usuario:", estado.respuestas);
        // Aquí iría la lógica para enviar los resultados al servidor
        alert("¡Test completado con éxito! Procesando tus resultados...");
        // window.location.href = "/resultados";
    }

    // Event Listeners
    DOM.opciones.forEach(opcion => {
        opcion.addEventListener("click", function() {
            const pregunta = this.closest(".pregunta");
            const indice = parseInt(pregunta.dataset.index);

            // Desactivar todas las opciones de esta pregunta
            pregunta.querySelectorAll(".opcion").forEach(op => {
                op.classList.remove("activa");
            });

            // Activar la opción seleccionada
            this.classList.add("activa");

            // Guardar la respuesta
            guardarRespuesta(indice, this.textContent.trim());
        });
    });

    DOM.btnContinuar.addEventListener("click", siguientePregunta);
    DOM.btnVolver.addEventListener("click", preguntaAnterior);

    // Inicialización
    mostrarPregunta(0);
});