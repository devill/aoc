import { promises as fs } from 'fs';

let rawData = await fs.readFile('./input4.txt', 'utf8');
// let rawData = await fs.readFile('./test4.txt', 'utf8');

let data = rawData.split('\n').map(l => l.match(/\d+/g)?.map(v => parseInt(v)));
data.pop();

let result1 = data.filter(l => (l[0] <= l[2] && l[3] <= l[1]) || (l[2] <= l[0] && l[1] <= l[3])).length

console.log(result1);

let result2 = data.filter(l => !(l[1] < l[2] || l[3] < l[0] )).length

console.log(result2);