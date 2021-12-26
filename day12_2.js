import { promises as fs } from 'fs';

let rawData = await fs.readFile('./input12.txt', 'utf8');
// let rawData = await fs.readFile('./test12_1.txt', 'utf8');
// let rawData = await fs.readFile('./test12_2.txt', 'utf8');
// let rawData = await fs.readFile('./test12_3.txt', 'utf8');

const caveType = (name) => {
    return name === name.toLowerCase() ? 'small' : 'large';
}

const data = rawData
    .split('\n')
    .map(l => l.split('-'))
    .reduce((nodes, l) => {
        nodes[l[0]] = nodes[l[0]] || { type: caveType(l[0]), neighbours: [] };
        nodes[l[1]] = nodes[l[1]] || { type: caveType(l[1]), neighbours: [] };
        nodes[l[0]].neighbours.push(l[1]);
        nodes[l[1]].neighbours.push(l[0]);
        return nodes;
    }, {});

console.log(data);

let visited = Object.keys(data).reduce((v, c) => {
    v[c] = 0;
    return v;
}, {});

let route = [];
let doubleVisitUsedAt = null;

const findRouts = (caveName) => {
    visited[caveName]++;
    route.push(caveName);

    if(caveName === 'end') {
        console.log(route.join(','), doubleVisitUsedAt);
        visited[caveName]--;
        route.pop();
        return 1;
    }
    let routs = data[caveName].neighbours.reduce((routs, n) => {
        if(data[n].type === 'large' || visited[n] === 0) {
            routs += findRouts(n);
        } else if(doubleVisitUsedAt === null && visited[n] === 1 && n !== 'start') {
            doubleVisitUsedAt = n;
            routs += findRouts(n);
            doubleVisitUsedAt = null;
        }
        return routs;
    }, 0);

    visited[caveName]--;
    route.pop();
    return routs;
}

console.log(findRouts('start'));