const scoreBar = document.querySelector(".score-bar-fill");

if (scoreBar) {

    const score = Number(scoreBar.dataset.score);

    // Set the width
    scoreBar.style.width = score + "%";


    // Set the color based on the score
    if (score >= 80) {

        scoreBar.classList.add("score-low");

    } else if (score >= 50) {

        scoreBar.classList.add("score-medium");

    } else {

        scoreBar.classList.add("score-high");

    }

}
