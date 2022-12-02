import { promises as fs } from 'fs';
import {GPU} from "gpu.js";

const gpu = new GPU();

let rawData = await fs.readFile('./input15.txt', 'utf8');
// let rawData = await fs.readFile('./test15.txt', 'utf8');

let data = rawData.split('\n').map(l => l.split('').map(c => parseInt(c)));
data = data.map(l => [0,1,2,3,4].flatMap(i => l.map(c => (c+i-1)%9+1)));
data = [0,1,2,3,4].flatMap(i => data.map(l => l.map(c => (c+i-1)%9+1)));

let path = data.map(l => l.map(c => -1));
path[0][0] = 0;

let pathCalc = gpu.createKernel(function(cost, data, path, lengthy, lengthx) {
    let x = this.thread.x;
    let y = this.thread.y;
    if(path[y][x] > -1) return path[y][x];
    if(x > 0 &&      path[y][x-1] > -1 && path[y][x-1] + data[y][x] <= cost) return path[y][x-1] + data[y][x];
    if(x + 1 < lengthx && path[y][x+1] > -1 && path[y][x+1] + data[y][x] <= cost) return path[y][x+1] + data[y][x];
    if(y > 0 &&      path[y-1][x] > -1 && path[y-1][x] + data[y][x] <= cost) return path[y-1][x] + data[y][x];
    if(y + 1 <lengthy &&  path[y+1][x] > -1 && path[y+1][x] + data[y][x] <= cost) return path[y+1][x] + data[y][x];
    return -1;
}).setOutput([data.length, data[0].length]);

let cost;
for(cost = 0; path[path.length-1][path[0].length - 1] < 0; cost++) {
    path = pathCalc(cost, data, path, data.length, data[0].length).map(l => Array.from(l));
}

console.log(cost - 1);