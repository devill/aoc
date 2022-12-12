import { promises as fs } from 'fs';
import {Heap} from 'heap-js';

let start = {
    x: null,
    y: null
}
let end = {
    x: null,
    y: null
}

let elevations = (await fs.readFile('./input12.txt', 'utf8'))
// let elevations = (await fs.readFile('./test12.txt', 'utf8'))
    .split('\n')
    .map((l, y) => l.split('').map((e, x) => {
        if(e === 'S') {
            start.x = x;
            start.y = y;
            return 0;
        } else if (e === 'E') {
            end.x = x;
            end.y = y;
            return 25;
        } else {
            return e.charCodeAt(0) - 97;
        }
    }));

console.log(start);
console.log(end);

let reached = elevations.map(l => l.map(c => false));
reached[end.y][end.x] = true;


let heap = new Heap((a,b) => a.cost - b.cost);
heap.push({ cost: 0, ...end });

let firstBottomFound = false;

while(heap.peek()) {
    const current = heap.pop();

    if(elevations[current.y][current.x] === 0 && !firstBottomFound) {
        firstBottomFound = true
        console.log('Result 2:', current.cost);
    }
    if(start.x === current.x && start.y === current.y) {
        console.log('Result 1:', current.cost);
    }
    let candidates = [];
    if(current.y - 1 >= 0) candidates.push({x: current.x, y: current.y - 1});
    if(current.y + 1 < elevations.length) candidates.push({x: current.x, y: current.y + 1});
    if(current.x - 1 >= 0) candidates.push({x: current.x - 1, y: current.y});
    if(current.x + 1 < elevations[current.y].length) candidates.push({x: current.x + 1, y: current.y});
    candidates.forEach(n => {
        if(!reached[n.y][n.x] && elevations[current.y][current.x] - elevations[n.y][n.x] <= 1) {
            reached[n.y][n.x] = true;
            heap.push({ cost: current.cost + 1, ...n})
        }
    });
    // console.log(reached.map(l => l.map(v => v ? '#' : '.').join('')).join('\n'));
    // console.log('\n\n');
}

