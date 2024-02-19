function toggleForm() {
    let form = document.getElementById("myForm");
    let toggleButton = document.getElementById("toggleButton");

    if (toggleButton.checked) {
        form.className = "operatorForm"; // Changer la classe du formulaire à "operatorForm"
    } else {
        form.className = "clientForm"; // Changer la classe du formulaire à "clientForm"
    }
}
