var height = 6;
var width = 5;

var row = 0;
var col = 0;

var gameOver = false

document.addEventListener('DOMContentLoaded', function () {
    initialize();

    // // Event listener for the form
    // document.querySelector('.answerForm form').addEventListener('submit', function (event) {
    //     event.preventDefault();

    //     const userAnswer = document.getElementById('userAnswer').value;

    //     submitAnswer(userAnswer);
    // });
});

// function submitAnswer() {
//     // Get the user's answer from the input field
//     const userAnswer = document.getElementById('userAnswer').value;

//     // Call a function to send the answer to the backend
//     fetchData(userAnswer);
// }

// function fetchData(answer) {
//     // Make a request to the backend
//     fetch(`/user_answer?user_answer=${encodeURIComponent(answer)}`)
//         .then(response => response.json())
//         .then(data => {
//             // Update the content dynamically, e.g., manipulate the DOM
//             console.log('Data received from the server:', data);
//             // You can update the DOM or perform other actions here
//         })
//         .catch(error => console.error('Error:', error));
// }


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
    }
}

// function submitAnswer(answer) {
//     fetch('/user_answer', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ user_answer: answer }),
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log('Data received after submission:', data);
//     })
//     .catch(error => console.error('Error', error));
// }