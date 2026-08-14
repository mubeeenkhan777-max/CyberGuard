const passwordInput = document.getElementById("password");

const strengthBar = document.getElementById("strength-bar-fill");
const strengthText = document.getElementById("strength-text");

const lengthRequirement = document.getElementById("length");
const uppercaseRequirement = document.getElementById("uppercase");
const lowercaseRequirement = document.getElementById("lowercase");
const numberRequirement = document.getElementById("number");
const specialRequirement = document.getElementById("special");


passwordInput.addEventListener("input", function () {

    const password = passwordInput.value;

    let score = 0;


    // Check password length
    const hasLength = password.length >= 8;

    if (hasLength) {
        score++;
    }


    // Check uppercase letter
    const hasUppercase = /[A-Z]/.test(password);

    if (hasUppercase) {
        score++;
    }


    // Check lowercase letter
    const hasLowercase = /[a-z]/.test(password);

    if (hasLowercase) {
        score++;
    }


    // Check number
    const hasNumber = /[0-9]/.test(password);

    if (hasNumber) {
        score++;
    }


    // Check special character
    const hasSpecial = /[^A-Za-z0-9]/.test(password);

    if (hasSpecial) {
        score++;
    }


    // Update requirements
    updateRequirement(lengthRequirement, hasLength);
    updateRequirement(uppercaseRequirement, hasUppercase);
    updateRequirement(lowercaseRequirement, hasLowercase);
    updateRequirement(numberRequirement, hasNumber);
    updateRequirement(specialRequirement, hasSpecial);


    // Update strength
    updateStrength(score);

});


function updateRequirement(element, passed) {

    if (passed) {

        element.textContent = "✓ " + element.textContent.replace("✓ ", "");

    } else {

        element.textContent = "✗ " + element.textContent.replace("✓ ", "").replace("✗ ", "");

    }

}


function updateStrength(score) {

    if (score === 0) {

        strengthBar.style.width = "0%";
        strengthText.textContent = "Enter a password to check its strength.";

    } else if (score <= 2) {

        strengthBar.style.width = "30%";
        strengthText.textContent = "Weak password";

    } else if (score <= 4) {

        strengthBar.style.width = "65%";
        strengthText.textContent = "Medium password";

    } else {

        strengthBar.style.width = "100%";
        strengthText.textContent = "Strong password";

    }

}
