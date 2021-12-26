import { promises as fs } from 'fs';

let rawData = await fs.readFile('./input6.txt', 'utf8');
// let rawData = await fs.readFile('./test6.txt', 'utf8');

let data = rawData.split(',').filter(n => n !== '').map(n => parseInt(n));

console.log(data);

let clockCount = data.reduce((acc, item) => {
    acc[item] += 1;
    return acc;
}, Array(9).fill(0));

for(let i = 0; i < 256; i++) {
    let spawnGeneration = clockCount.shift();
    clockCount.push(spawnGeneration);
    clockCount[6] += spawnGeneration;
}

console.log(clockCount, clockCount.reduce((acc,val) => acc + val, 0));
