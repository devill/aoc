import {promises as fs} from 'fs';

let rawData = await fs.readFile('./input8.txt', 'utf8');
// let rawData = await fs.readFile('./test8.txt', 'utf8');

const data = rawData
    .split('\n')
    .filter(l => l !== '')
    .map(l => l.split(' | '))
    .map(([notes, value]) => ({
        notes: notes.split(' ').map(n => n.split('').map(d => d.charCodeAt(0) - 96)),
        value: value.split(' ').map(n => n.split('').map(d => d.charCodeAt(0) - 96))
    }) );

// console.log(data[0]);

let uniqDigits = data
    .flatMap(({value}) => value.map(v => [2,3,4,7].includes(v.length)))
    .filter(v => v).length;

console.log(uniqDigits);

let possiblePermutations = [];
function backtrack(digits) {
    if(digits.length === 7) {
        possiblePermutations.push([...digits]);
        return;
    }
    for(let i = 1; i < 8; i++) {
        if(!digits.includes(i)) {
            backtrack([...digits, i]);
        }
    }
}
backtrack([]);

const validConstellations = [
    [1,2,3,5,6,7],
    [3,6],
    [1,3,4,5,7],
    [1,3,4,6,7],
    [2,3,4,6],
    [1,2,4,6,7],
    [1,2,4,5,6,7],
    [1,3,6],
    [1,2,3,4,5,6,7],
    [1,2,3,4,6,7]
].map(l => parseInt(l.join('')));

// console.log(validConstellations);

let sData = data.map(l => ([...l.notes, ...l.value]));

let sum = 0;
for(let cid = 0; cid < data.length; cid++) {
    for(let pid = 0; pid < possiblePermutations.length; pid++) {
        let fixed = [];
        for(let did = 0; did < sData[cid].length; did++) {
            let a = parseInt(sData[cid][did].map(d => possiblePermutations[pid][d - 1]).sort().join(''));
            if (validConstellations.includes(a)) {
                fixed.push(validConstellations.indexOf(a));
            }
        }
        if(fixed.length === sData[cid].length) {
            let val = parseInt(fixed.slice(-4).join(''));
            sum += val;
        }
    }
}
console.log(sum);
