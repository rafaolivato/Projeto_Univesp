document.addEventListener("DOMContentLoaded", function() {
    let formset = document.getElementById('formset');
    let totalForms = document.getElementById("id_form-TOTAL_FORMS");
    let formTemplate = formset.children[0].cloneNode(true);

    document.getElementById('add-item').addEventListener('click', function() {
        let formNum = totalForms.value;

        // Criando um novo formulário a partir do template
        let newForm = formTemplate.cloneNode(true);

        // Substituindo os índices corretamente
        newForm.innerHTML = newForm.innerHTML.replace(/-\d+-/g, `-${formNum}-`);
        newForm.innerHTML = newForm.innerHTML.replace(/_\d+_/g, `_${formNum}_`);

        // Adicionando ao formset
        formset.appendChild(newForm);

        // Atualizando o número total de formulários
        totalForms.value = parseInt(formNum) + 1;
    });
});
