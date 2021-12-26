
// const makeInitialArray = dims => {
//     if(dims.length === 1) return Array(dims[0]).fill(0);
//     return Array(dims[0]).fill(0).map(l => makeInitialArray(dims.slice(1)));
// }

let winCounts = [0, 0];
let counts = {}; //makeInitialArray([10,21,10,21]);

counts['6_0_4_0'] = 1;
// counts['4_0_8_0'] = 1;

function calculateChoices(i, diceSides) {

    if(diceSides.length === 1) return i <= diceSides[0] && i > 0 ? 1 : 0;
    return Array(diceSides[0]).fill(0).reduce((s,v,j) => calculateChoices(i-(j+1), diceSides.slice(1)) + s, 0);
}

const diceSides = [3,3,3];
const maxValue = diceSides.reduce((s,v) => s + v);

const choices = Array(maxValue + 1)
    .fill(0)
    .map((v, i) => calculateChoices(i, diceSides));

let openGames = true;
let onTurn = 0;
let turn = 0;
while(openGames) {
    openGames = false;
    let nextCounts = {}

    Object.entries(counts).forEach(([key, value]) => {
        let fields = [0,0];
        let scores = [0,0];
        let init = key.split('_').map(n => parseInt(n));
        for(let i = 3; i <= 9; i++) {
            [fields[0], scores[0], fields[1], scores[1]] = init;
            fields[onTurn] = (fields[onTurn] - 1 + i) % 10 + 1;
            scores[onTurn] += fields[onTurn];
            if(scores[onTurn] < 21) {
                const newKey = [fields[0], scores[0], fields[1], scores[1]].join('_');
                nextCounts[newKey] = nextCounts[newKey] || 0;
                nextCounts[newKey] += choices[i] * value;
                openGames = true;
            } else {
                winCounts[onTurn] += choices[i] * value;
            }
        }
    });
    counts = nextCounts;
    turn++;
    onTurn = 1 - onTurn;
}

console.log(counts);
console.log(winCounts);
console.log(Math.max(...winCounts));