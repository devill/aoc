import { promises as fs } from 'fs';

let rawData = await fs.readFile('./input1.txt', 'utf8');

let data = [[]];

rawData
    .split('\n')
    .forEach((l) => {
        if(l === '') {
            data.push([]);
        } else {
            data[data.length-1].push(parseInt(l));
        }
    });

let sums = data.map((e) => e.reduce((v,s) => v +s, 0));

console.log(Math.max(...sums));

console.log(sums.sort().reverse().slice(0,3).reduce((v,s) => v + s));