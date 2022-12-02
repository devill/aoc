import {GPU} from "gpu.js";

const gpu = new GPU();

let positions = [5, 3];
let scores = [0,0];
let onTurn = 0;
let roll = 0;

while(scores[0] < 1000 && scores[1] < 1000) {
    for(let i = 0; i < 3; i++) {
        roll++;
        positions[onTurn] += (roll - 1) % 100 + 1;
        positions[onTurn] = positions[onTurn] % 10;

    }
    scores[onTurn] += positions[onTurn] + 1;
    onTurn = 1 - onTurn;
}
console.log("Part 1:", Math.min(...scores)*roll);


