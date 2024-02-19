function toggleForm() {
    var form = document.getElementById("myForm");
    var toggleButton = document.getElementById("toggleButton");

    if (toggleButton.checked) {
        form.className = "operatorForm"; // Changer la classe du formulaire à "operatorForm"
    } else {
        form.className = "clientForm"; // Changer la classe du formulaire à "clientForm"
    }
}
