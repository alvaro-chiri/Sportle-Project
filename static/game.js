var height = 6;
var width = 5;

var row = 0;
var col = 0;

var gameOver = false;
var gameWin = false;

const randomTeamData = window.randomTeamData;

console.log('Random Team Data:', randomTeamData);

// Now you can access the properties of the random_team object
const randomTeamName = randomTeamData.teamName;
console.log('Random Team Name from the JS script:', randomTeamName);

document.addEventListener('DOMContentLoaded', function () {
    initialize();
});


function initialize() {
    // make gameboard
    for (let r = 0; r < height; r++) {
        for (let c = 0; c < width; c++) {
            let tile = document.createElement("span");
            tile.id = r.toString() + "-" + c.toString();
            tile.classList.add("tile");
            tile.innerText = " ";
            document.getElementById("board").appendChild(tile);
        }

        let guessTile = document.createElement("span");
        guessTile.id = r.toString() + "-guess";
        guessTile.classList.add("guessTile");
        guessTile.innerText = " ";
        document.getElementById("board").appendChild(guessTile);
    }
}

function guess() {
    event.preventDefault();

    var selectedAnswerString = document.getElementById("userAnswer").value;

    try {
        var correctedString = selectedAnswerString.replace(/'/g, '"');
        
        var selectedAnswer = JSON.parse(correctedString);

        console.log("Selected Answer:", selectedAnswer);

        // check the guess is the correct team
        if (selectedAnswer['id'] == randomTeamData.id) {
            for (let c = 0; c < width; c++) {
                var tileID = row.toString() + "-" + c.toString();
                document.getElementById(tileID).classList.add("correct");
            }
            var guessTileID = row.toString() + "-guess";
            document.getElementById(guessTileID).innerText = selectedAnswer['teamName']
        
            //end the game
            gameWin = true;

            gameWinFunction()
        }
        else {
            if (selectedAnswer['sport'] == randomTeamData.sport) {
                var tileID = row.toString() + '-0'
                document.getElementById(tileID).classList.add("correct");
            }
            else {
                var tileID = row.toString() + '-0'
                document.getElementById(tileID).classList.add("incorrect");
            }
            if (selectedAnswer['continent'] == randomTeamData.continent) {
                var tileID = row.toString() + '-1'
                document.getElementById(tileID).classList.add("correct");
            }
            else {
                var tileID = row.toString() + '-1'
                document.getElementById(tileID).classList.add("incorrect");
            }
            if (selectedAnswer['country'] == randomTeamData.country) {
                var tileID = row.toString() + '-2'
                document.getElementById(tileID).classList.add("correct");
            }
            else {
                var tileID = row.toString() + '-2'
                document.getElementById(tileID).classList.add("incorrect");
            }
            if (selectedAnswer['league'] == randomTeamData.league) {
                var tileID = row.toString() + '-3'
                document.getElementById(tileID).classList.add("correct");
            }
            else {
                var tileID = row.toString() + '-3'
                document.getElementById(tileID).classList.add("incorrect");
            }
            var tileID = row.toString() + '-4'
            document.getElementById(tileID).classList.add("incorrect");

            var guessTileID = row.toString() + "-guess";
            document.getElementById(guessTileID).innerText = selectedAnswer['teamName']
        }

        if (gameWin == false && gameOver == false) {
            row += 1
        }

        if (row == 6) {
            gameOver = true
            gameOverFunction()
        }
    } catch (error) {
        console.error('Error parsing selected answer:', error);
    }
}


// function gameOverFunction() {
//     fetch('/game_over', {
//         method: 'post',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//     })
//     .then(response => response.text())  // Assuming the server responds with a redirect URL
//     .then(redirectUrl => {
//         // Redirect to the specified URL
//         window.location.href = redirectUrl;
//     })
//     .catch(error => {
//         console.error('Error calling Python action:', error);
//     });
// }

function gameOverFunction() {
    console.log('Game Over!'); // Add this line
    fetch('/game_over', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.text())
    .then(redirectUrl => {
        console.log('Redirecting to:', redirectUrl); // Add this line
        window.location.href = redirectUrl;
    })
    .catch(error => {
        console.error('Error calling Python action:', error);
    });
}

function gameWinFunction() {
    fetch('/game_win', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.text())  // Assuming the server responds with a redirect URL
    .then(redirectUrl => {
        // Redirect to the specified URL
        window.location.href = redirectUrl;
    })
    .catch(error => {
        console.error('Error calling Python action:', error);
    });
}