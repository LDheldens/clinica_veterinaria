document.addEventListener('DOMContentLoaded',()=>{
    const selectAlergia = document.querySelector('#id_alergiaPregunt')
    const inputAlergias = document.querySelector('.alergias-paciente')

    selectAlergia.addEventListener('change',(e)=>{
        let valor = e.target.value
        if (valor=='si') {
            inputAlergias.classList.remove('d-none')
        }else{
            inputAlergias.classList.add('d-none')
        }
    })

})