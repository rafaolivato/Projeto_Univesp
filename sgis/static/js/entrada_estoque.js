document.addEventListener("DOMContentLoaded", function () {
    const formsetContainer = document.querySelector(".form-fields");
    const totalForms = document.querySelector("#id_form-TOTAL_FORMS");
    const addButton = document.querySelector("#add-item");

    addButton.addEventListener("click", function () {
        let formNum = parseInt(totalForms.value);
        let newForm = document.querySelector(".formset-form").cloneNode(true);

        // Limpa os valores dos inputs clonados
        newForm.querySelectorAll("input, select").forEach(input => {
            input.value = "";
            input.name = input.name.replace(/-\d+-/g, `-${formNum}-`);
            input.id = input.id.replace(/-\d+-/g, `-${formNum}-`);
        });

        formsetContainer.appendChild(newForm);
        totalForms.value = formNum + 1;
    });
});
