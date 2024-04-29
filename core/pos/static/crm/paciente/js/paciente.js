document.addEventListener('DOMContentLoaded', () => {
    const checktAlergia = document.querySelector('#id_alergias_bolean');
    const inputAlergias = document.querySelector('#alergias');
    const action = document.querySelector('#action');
    
    // Verificar si el checkbox está marcado
    if (checktAlergia.checked) {
        inputAlergias.classList.remove('d-none')
    }
});
