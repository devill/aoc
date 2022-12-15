import { promises as fs } from 'fs';

let data = (await fs.readFile('./input15.txt', 'utf8'))
// let data = (await fs.readFile('./test15.txt', 'utf8'))
    .split('\n')
    .map(l => /Sensor at x=(?<Sx>-?\d+), y=(?<Sy>-?\d+): closest beacon is at x=(?<Bx>-?\d+), y=(?<By>-?\d+)/.exec(l))
    .map(l => l.groups)
    .map(l => Object.entries(l).reduce((d, [k,v]) => ({...d, [k]: parseInt(v)}), {}))
    .map(l => ({S: {x:l.Sx, y:l.Sy}, B: {x:l.Bx, y: l.By}}));

console.log(data);

const manhattanDistance = (p1, p2) => {
    return Math.abs(p1.x - p2.x) + Math.abs(p1.y - p2.y);
};



const blockedOnLine  = (line) => {
    let blocked = [];
    data.forEach(({S, B}) => {
        const d = manhattanDistance(S, B);
        const dx = d - Math.abs(S.y - line);
        if (dx >= 0) {
            blocked.push({x: S.x - dx, type: 1});
            blocked.push({x: S.x + dx, type: -1});
        }
    });
    blocked.sort((l, r) => l.x - r.x);
    return blocked;
}

let blocked = blockedOnLine(2000000);

let totalBlocked = 0;
let level = 0;
let lastStart = null;
blocked.forEach(({x, type}) => {
    if(level === 0 && type === 1) {
        lastStart = x;
    }
    if(level === 1 && type === -1) {
        totalBlocked += x - lastStart;
    }
    level += type;
});
console.log(totalBlocked);

for(let y = 0; y <= 4000000; y++) {
    const blocked = blockedOnLine(y);

    let level = 0;
    blocked.forEach(({x, type}, i) => {
        level += type;
        if(level === 0 && (i+1 >= blocked.length || blocked[i+1].x - x > 1)) {// && x+1 >= 0 && x+1 <= 20 && (i >= blocked.length || blocked[i+1].x - x > 2)) {
            if( x+1 >= 0 && x+1 <= 4000000) {
                // console.log(blocked);
                // console.log(x + 1, y);
                console.log((x+1)*4000000+y);
            }
        }
    });
}