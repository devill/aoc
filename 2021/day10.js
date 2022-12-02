import { promises as fs } from 'fs';

let rawData = await fs.readFile('./input10.txt', 'utf8');
// let rawData = await fs.readFile('./test10.txt', 'utf8');

let data = rawData.split('\n').filter(l => l !== '');

console.log(data);

const matching = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

let syntaxChecks = data
    .map(l => {

        let stack = [];

        for(let i = 0; i < l.length; i++) {
            if(Object.keys(matching).includes(l[i])) {
                stack.unshift(matching[l[i]]);
            } else {
                const close = stack.shift();
                if(l[i] !== close) {
                    return { errorChar: l[i], completion: null };
                }
            }
        }
        return { errorChar: null, completion: stack}
    });


const errorVal = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

let corruptions = syntaxChecks
    .filter(({errorChar}) => errorChar)
    .map(({errorChar}) => errorVal[errorChar])
    .reduce((sum,v) => sum + v, 0);

console.log(corruptions);

const completionVal = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

let scores = syntaxChecks
    .filter(({completion}) => completion)
    .map(({completion}) => completion.map(c => completionVal[c]).reduce((score, v) => score * 5 + v, 0) )
    .sort((a,b) => a - b);

console.log(scores[(scores.length - 1)/2]);