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
            // location.href = 'game_win';
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
            // location.href = 'game_over';
        }
    } catch (error) {
        console.error('Error parsing selected answer:', error);
    }
}


async function gameOverFunction() {
    try {
        await fetch('/game_over_update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        location.href = 'game_over';
    } catch (error) {
        console.error('Error calling Python action:', error);
    }
}

async function gameWinFunction() {
    try {
        await fetch('/game_win_update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        location.href = 'game_win';
    } catch (error) {
        console.error('Error calling Python action:', error);
    }
}