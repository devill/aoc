import { promises as fs } from 'fs';

let rawData = await fs.readFile('./input3.txt', 'utf8');
// let rawData = await fs.readFile('./test3.txt', 'utf8');

let data = rawData.split('\n').map((l) => {
    return l.split('').map(c => {
        let charCode = c.charCodeAt(0);
        return charCode < 97 ? charCode - 65 + 27 : charCode - 97 + 1;
    })
});
data.pop();

let dataByCompartment = data.map(r => [r.slice(0, r.length/2), r.slice(r.length/2)])

let results1 = dataByCompartment.map(r => {
    let c1 = {};
    r[0].forEach(item => c1[item] = true);
    return r[1].find(item => !!c1[item]);
});

const sum = (a) => a.reduce((acc,v) => acc+v,0);
console.log(sum(results1));

let results2 = [];
for(let i = 0; i < data.length; i+= 3) {
    let c1 = {};
    data[i].forEach(item => c1[item] = true);
    let c2 = {};
    data[i+1].forEach(item => c2[item] = true);
    results2.push(data[i+2].find(item => (!!c1[item]) && (!!c2[item])));
}

console.log(results2);

console.log(sum(results2));