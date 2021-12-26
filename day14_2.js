import { promises as fs } from 'fs';

let rawData = await fs.readFile('./input14.txt', 'utf8');
// let rawData = await fs.readFile('./test14.txt', 'utf8');

let [rawTemplate,rawRules] = rawData.split('\n\n');

let firstChar = rawTemplate[0];
let template = rawTemplate
    .split('')
    .reduce((acc, c, i, arr) => {
        if(i === 0) return acc;
        let key = arr.slice(i-1,i+1).join('');
        acc[key] = acc[key] + 1 || 1;
        return acc;
    },{});


let rules = rawRules
    .split('\n')
    .map(l => l.match(/(\w\w) -> (\w)/))
    .reduce((acc,r) => {
        acc[r[1]] = [r[1][0]+r[2], r[2] + r[1][1]];
        return acc;
    }, {});


for(let i = 0; i < 40; i++) {
    template = Object.entries(template).reduce((temp, [pair, count]) => {
        if (rules[pair]) {
            temp[rules[pair][0]] = temp[rules[pair][0]] + count || count;
            temp[rules[pair][1]] = temp[rules[pair][1]] + count || count;
        } else {
            temp[pair] = temp[pair] + count || count;
        }
        return temp;
    }, {})
    console.log('Step:', i, 'Size:', Object.values(template).reduce((sum, v) => sum + v, 0)+1);
}

let charCounts = Object.entries(template).reduce((charCounts,[pair, count]) => {
    charCounts[pair[1]] = charCounts[pair[1]] + count || count;
    return charCounts;
},{[firstChar]:1});

console.log(charCounts);

let counts = Object.values(charCounts).sort((a,b) => a - b);

console.log(counts.pop() - counts.shift());

