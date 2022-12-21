import { promises as fs } from 'fs';

// const data = (await fs.readFile('./input21.txt', 'utf8'))
let data = (await fs.readFile('./test21.txt', 'utf8'))
    .split('\n')
    .map(l => l.split(': '))
    .reduce((dict, [k,v]) => {
        let m = v.match(/(\w+) ([+\-*\/]) (\w+)/);

        if(m) {
            dict[k] = {type: m[2], operands: [m[1], m[3]]};
        } else {
            dict[k] = {type: 'value', value: parseInt(v)};
        }
        return dict;
    }, {});

const operations = {
    '+': (l,r) => l + r,
    '-': (l,r) => l - r,
    '*': (l,r) => l * r,
    '/': (l,r) => l / r
}

const calculate = (node) => {
    if(!data[node].value) {
        let values = data[node].operands.map(op => calculate(op));
        data[node].value = operations[data[node].type](...values);
    }
    return data[node].value
}

const result = calculate('root');

console.log(data);
console.log(result);
