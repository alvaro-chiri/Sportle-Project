var height = 6;
var width = 5;

var row = 0;
var col = 0;

var gameOver = false

window.onload = function(){
    initialize();
}

function initialize() {
    // make gameboard
    for (let r = 0; r < height; r++) {
        for (let c = 0; c< width; c++) {
            let tile = document.createElement("span");
            tile.id = r.toString() + "-" + c.toString();
            tile.classList.add("tile");
            document.getElementById("board").appendChild(tile);
        }
    }
}