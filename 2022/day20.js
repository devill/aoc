import { promises as fs } from 'fs';

const rawData = (await fs.readFile('./input20.txt', 'utf8'))
// let rawData = (await fs.readFile('./test20.txt', 'utf8'))
    .split('\n');


let data = rawData
    .map((d, i)=> ({ value: parseInt(d), originalId: i }));

// console.log('Initial arrangement:');
// console.log(data.map(item => item.value).join(' '));

const mixStep = (data, id) => {
    const currentId = data.findIndex(item => item.originalId === id);
    const item = data[currentId];

    let newId = (currentId + item.value - 1) % (data.length - 1) + 1;
    if(newId <= 0) newId += data.length - 1;

    let dir = Math.sign(newId - currentId);
    for(let i = currentId; i !== newId; i += dir) {
        data[i] = data[i + dir];
    }
    data[newId] = item;
    const beforeNewId = (newId === 0) ? data.length - 1 : newId - 1;
    const afterNewId = (newId === data.length - 1) ? 0 : newId + 1;

    // console.log('');
    // console.log(item.value, 'moves between', data[beforeNewId].value, 'and', data[afterNewId].value, ':')
    return data;
}

for(let i = 0; i < data.length; i++) {
    data = mixStep(data, i);
    // console.log(data.map(item => item.value).join(' '));
}
//
let offset = data.findIndex(item => item.value === 0);
console.log("Result 1: ", [1000,2000,3000].map(i => data[(offset+i) % data.length].value).reduce((s,v) => s + v, 0));

data = rawData
    .map((d, i)=> ({ value: parseInt(d)*811589153, originalId: i }));

for(let j = 0; j < 10; j++) {
    for (let i = 0; i < data.length; i++) {
        data = mixStep(data, i);
        // console.log(data.map(item => item.value).join(' '));
    }
}

offset = data.findIndex(item => item.value === 0);
console.log("Result 2: ", [1000,2000,3000].map(i => data[(offset+i) % data.length].value).reduce((s,v) => s + v, 0));