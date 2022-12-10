import { promises as fs } from 'fs';

let data = (await fs.readFile('./input10.txt', 'utf8'))
// let data = (await fs.readFile('./test10_1.txt', 'utf8'))
// let data = (await fs.readFile('./test10_2.txt', 'utf8'))
    .split('\n')
    .slice(0, -1)
    .map(l => l !== 'noop' ? parseInt(l.split(' ')[1]) : null)
    .flatMap(l => l !== null ? [null, l] : [null]);

console.log(data);

let values = data.reduce((p, v) => {
    if(v === null) {
        return p.concat(p.slice(-1));
    } else {
        return p.concat(p.slice(-1).map(lastValue => lastValue+v))
    }
}, [1]);

console.log(values);

let signalStrength = 0;
for(let i = 20; i <= values.length; i+=40) {
    signalStrength += i*values[i-1];
    console.log(i, signalStrength);
}

console.log(signalStrength);

var chunks = function(array, size) {
    var results = [];
    while (array.length) {
        results.push(array.splice(0, size));
    }
    return results;
};

let screen = chunks(values.map((v, i) => (Math.abs(i%40 - v) <= 1) ? '#' : '.'), 40).map(l => l.join('')).join('\n');

console.log(screen);