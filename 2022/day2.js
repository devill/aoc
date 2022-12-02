import { promises as fs } from 'fs';

let rawData = await fs.readFile('./input2.txt', 'utf8');
// let rawData = await fs.readFile('./test2.txt', 'utf8');

let data = rawData.split('\n').map((l) => {
    return [l.charCodeAt(0)-64, l.charCodeAt(2)-87];
});
data.pop();

let scores1 = data.map(([them, me]) => {
    let isWin = me - them === 1  || (them === 3 && me === 1);
    let isDraw = (me === them);
    return me + (isDraw ? 3 : 0) + (isWin ? 6 : 0)
})

console.log(scores1);
console.log(scores1.reduce((v,s) => v+s));

let scores2 = data.map(([them, outcome]) => {
    let isWin = (outcome === 3);
    let isDraw = (outcome === 2);
    let me = (them + outcome) % 3 + 1;
    return me + (isDraw ? 3 : 0) + (isWin ? 6 : 0)
})

console.log(scores2);
console.log(scores2.reduce((v,s) => v+s));