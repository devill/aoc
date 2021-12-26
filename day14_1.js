import { promises as fs } from 'fs';

let rawData = await fs.readFile('./input14.txt', 'utf8');
// let rawData = await fs.readFile('./test14.txt', 'utf8');

let [template,rawRules] = rawData.split('\n\n');

let rules = rawRules
    .split('\n')
    .map(l => l.match(/(\w\w) -> (\w)/))
    .reduce((acc,r) => {
        acc[r[1]] = r[2];
        return acc;
    }, {});

// console.log(rules);
console.log(template);
for(let j = 0; j < 1; j++) {
    let newTemplate = template[0];

    for (let i = 1; i < template.length; i++) {
        newTemplate += rules[template.slice(i - 1, i + 1)] || '';
        newTemplate += template[i];
    }
    template = newTemplate;
    console.log(template.split('').reduce((acc, c, i, arr) => {
            let key = arr.slice(i-1,i+1).join('');
            acc[key] = acc[key] + 1 || 1;
            return acc;
        }
    , {}));
    console.log('Step:', j, 'Size:', template.length);
}

let charCounts = template.split('').reduce((sums, c) => {
    sums[c] = sums[c] || 0;
    sums[c] += 1;
    return sums;
}, {});

console.log(charCounts);

let counts = Object.values(charCounts).sort((a, b) => a - b);


console.log(counts.pop() - counts.shift());