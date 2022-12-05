import { promises as fs } from 'fs';

let rawData = await fs.readFile('./input5.txt', 'utf8');
// let rawData = await fs.readFile('./test5.txt', 'utf8');

let lines = rawData.split('\n');

const endOfCratesIndex = lines.findIndex(v => v === '');

let rawInitialStates = lines.slice(0, endOfCratesIndex - 1).reverse();
let initialStates = rawInitialStates.map(l => l.match(/.{1,4}/g).map(v => v[1]));

let rawMoves = lines.slice(endOfCratesIndex+1);
rawMoves.pop();
let moves = rawMoves.map(l => l.match(/\d+/g));


let state1 = new Array(initialStates[0].length).fill(0).map(() => [] );
initialStates.forEach(r => r.forEach((c, i) => { if(c !== ' ') {state1[i].push(c) }}));



moves.forEach(([count, from_col, to_col]) => {
    for(let i = 0; i < count; i++) {
        state1[to_col-1].push(state1[from_col-1].pop());
    }
});

console.log(state1.map(c => c.pop()).join(''));




let state2 = new Array(initialStates[0].length).fill(0).map(() => [] );
initialStates.forEach(r => r.forEach((c, i) => { if(c !== ' ') {state2[i].push(c) }}));

moves.forEach(([count, from_col, to_col]) => {
    state2[to_col-1].push(...state2[from_col-1].splice(-count,count))
});

console.log(state2.map(c => c.pop()).join(''));