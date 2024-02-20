function getRadiosCheckedValue(group) {
    let radios = document.getElementsByName(group);

    for (var i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            return radios[i].value;
        }
    }
}

function toggleOpacity(element) {
    if (element) {
        element.classList.toggle('element-show')
        element.classList.toggle('element-hide')
    }
}

function setValidation(value) {
    let form = document.getElementById('authy-header');
    let warning = document.getElementById('authy-warning')

    if (value == 'register') {
        form.textContent = 'Inscrivez-vous'
    } else if (value == 'connexion') {
        form.textContent = 'Connectez-vous' 
    }

    toggleOpacity(warning)
}

function toggleForm() {
    let user = getRadiosCheckedValue('user')
    let registration = document.getElementById('user-register')
    
    if (user == 'client') {
        registration.disabled = false;
        registration.classList.remove('element-disabled')
    }
    else if (user == 'operator') {
        registration.disabled = true;
        registration.classList.add('element-disabled')
        if (getRadiosCheckedValue('validation') == 'register') {
            let connexion = document.getElementById('user-connect')
            connexion.checked = true
            setValidation('connexion')
        }
    }
}