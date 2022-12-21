import { promises as fs } from 'fs';

const data = (await fs.readFile('./input21.txt', 'utf8'))
// let data = (await fs.readFile('./test21.txt', 'utf8'))
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

data['root'].type = '=';
data['humn'] = { type: 'variable', value: 'h', isResolver: true }

const buildResolver = (node) => {
    if(!data[node].value) {
        let values = data[node].operands.map(op => buildResolver(op));
        if(data[node].operands.find(op => data[op].isResolver )) {
            data[node].isResolver = true;
            data[node].value = '(' + data[node].operands.map(op => data[op].value.toString()).join(data[node].type) + ')';
        } else {
            data[node].value = operations[data[node].type](...values);
        }
    }
    return data[node].value
}

const result = buildResolver('root');

console.log(data);
console.log(result);

let targetValue = data[data['root'].operands.find(op => !data[op].isResolver)].value;

let eq = data['root'].operands.find(op => data[op].isResolver);

console.log(targetValue, ' = ', data[eq].value);

while(eq !== 'humn') {
    // console.log(data[eq]);
    if(data[eq].type === '+') {
        targetValue -= data[data[eq].operands.find(op => !data[op].isResolver)].value
    } else if(data[eq].type === '-') {
        if(data[data[eq].operands[0]].isResolver) {
            targetValue += data[data[eq].operands[1]].value;
        } else {
            targetValue = data[data[eq].operands[0]].value - targetValue;
        }
    } else if(data[eq].type === '*') {
        targetValue /= data[data[eq].operands.find(op => !data[op].isResolver)].value
    } else if(data[eq].type === '/') {
        if(data[data[eq].operands[0]].isResolver) {
            targetValue *= data[data[eq].operands[1]].value;
        } else {
            targetValue = data[data[eq].operands[0]].value / targetValue;
        }
    }
    eq = data[eq].operands.find(op => data[op].isResolver);
    console.log(targetValue, ' = ', data[eq].value);
}