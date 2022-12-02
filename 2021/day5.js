import { promises as fs } from 'fs';
import { GPU } from 'gpu.js'

const gpu = new GPU();

let rawData = await fs.readFile('./input5.txt', 'utf8');
// let rawData = await fs.readFile('./test5.txt', 'utf8');

let data = rawData
    .split('\n')
    .map(l => l.match(/(?<x1>\d+),(?<y1>\d+) -> (?<x2>\d+),(?<y2>\d+)/))
    .filter(l => !!l)
    .map(l => l.groups)
    .map(l => [parseInt(l.x1), parseInt(l.y1), parseInt(l.x2), parseInt(l.y2)]);

let restrictedLines = data.filter(l => l[0] === l[2] || l[1] === l[3]);
let max = Math.max(...data.flat()) + 1

const findIntersections = gpu.createKernel(function(lines, length) {
    let result = 0;

    for(let i = 0; i < length; i++) {
        let x1 = lines[i][0];
        let y1 = lines[i][1];
        let x2 = lines[i][2]
        let y2 = lines[i][3];
        let minx = Math.min(x1,x2);
        let maxx = Math.max(x1,x2);
        let miny = Math.min(y1,y2);
        let maxy = Math.max(y1,y2);
        let x = this.thread.x;
        let y = this.thread.y;

        if(minx <= x && x <= maxx && miny <= y && y <= maxy &&
            (minx === maxx || miny === maxy || (y1 - y2)*(x - x2) === (x1 - x2)*(y - y2))) {
            result++;
        }
    }
    return result;
}).setOutput([max,max]);

// const occupied = findIntersections(restrictedLines, restrictedLines.length).map(l => Array.from(l));
const occupied = findIntersections(data, data.length).map(l => Array.from(l));

for(let i = 0; i < max; i++) {
    console.log(Array.from(occupied[i]).map(x => x === 0 ? '.' : x.toString()).join(''))
}

console.log(occupied.flat().filter(x => x > 1).length);



