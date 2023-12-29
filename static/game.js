var height = 6;
var width = 5;

var row = 0;
var col = 0;

var gameOver = false

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
