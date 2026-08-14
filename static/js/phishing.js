const checkButton = document.getElementById("check-phishing");

const result = document.getElementById("phishing-result");


checkButton.addEventListener("click", function () {

    const answers = document.querySelectorAll(
        '.simulation-question input[type="checkbox"]'
    );


    let selected = [];


    answers.forEach(function (answer) {

        if (answer.checked) {
            selected.push(answer.value);
        }

    });


    const correctAnswers = [
        "urgency",
        "link",
        "suspicious"
    ];


    let correct = 0;


    selected.forEach(function (answer) {

        if (correctAnswers.includes(answer)) {
            correct++;
        }

    });


    if (correct === 3 && selected.length === 3) {

        result.textContent =
            "Excellent! 🎉 You identified the major warning signs.";

    } else if (correct >= 2) {

        result.textContent =
            "Good job! 👍 You identified several important warning signs.";

    } else {

        result.textContent =
            "Keep learning. 🔎 Look for urgency, suspicious senders, and unexpected verification requests.";

    }

});
