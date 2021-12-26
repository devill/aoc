import { promises as fs } from 'fs';
import {GPU} from "gpu.js";

const gpu = new GPU();

const padWith = (arr,v) => {
    return [Array(arr[0].length+2).fill(v), ...arr.map(line => [v, ...line, v]), Array(arr[0].length+2).fill(v)]
}

const printHeatMap = (heatMap) => {
    heatMap.forEach(l => console.log(l.map(v => v % 10).join('')));
}

let rawData = await fs.readFile('./input9.txt', 'utf8');
// let rawData = await fs.readFile('./test9.txt', 'utf8');

let data = rawData.split('\n').filter(l => l !== '').map(row => row.split('').map(d => parseInt(d)));

printHeatMap(data);

const findLows = gpu.createKernel(function(data) {
    let x = this.thread.x + 1;
    let y = this.thread.y + 1;

    if(
        data[y-1][x] > data[y][x] &&
        data[y+1][x] > data[y][x] &&
        data[y][x-1] > data[y][x] &&
        data[y][x+1] > data[y][x]
    ) {
        return data[y][x] + 1;
    } else {
        return 0;
    }
}).setOutput([data[0].length, data.length]);

const lows = Array.from(findLows(padWith(data,10))).map(l => Array.from(l));

console.log('   ');
printHeatMap(lows);

const totalRisk = lows.flat().reduce((sum, v) => sum + v, 0);

console.log("Total risk: ", totalRisk);

let id = 0;
let basinIds = lows.map(l => l.map(v => v > 0 ? id++ + 1 : 0));
printHeatMap(basinIds);

const findGradient = gpu.createKernel(function(data) {
    let x = this.thread.x + 1;
    let y = this.thread.y + 1;
    let v = data[y][x];

    if(data[y][x] === 9) {
        return [-1, -1]
    }

    let dirx = -1;
    let diry = -1;
    if(data[y-1][x] < v) {
        v = data[y-1][x]
        dirx = x;
        diry = y-1;
    }
    if(data[y+1][x] < v) {
        v = data[y+1][x]
        dirx = x;
        diry = y+1;
    }
    if(data[y][x-1] < v) {
        v = data[y][x-1]
        dirx = x-1;
        diry = y;
    }
    if(data[y][x+1] < v) {
        v = data[y][x+1]
        dirx = x+1;
        diry = y;
    }

    return [dirx - 1, diry - 1]

}).setOutput([data[0].length, data.length]);

const gradient = Array.from(findGradient(padWith(data,10))).map(l => Array.from(l));

const findBasin = gpu.createKernel(function(lows, gradient) {
    let x = this.thread.x;
    let y = this.thread.y;

    while(lows[y][x] === 0) {
        if(x === -1) return 0;
        let nx = gradient[y][x][0];
        let ny = gradient[y][x][1];
        x = nx;
        y = ny;
    }
    return lows[y][x];
}).setOutput([data[0].length, data.length]);

const basins = Array.from(findBasin(basinIds, gradient)).map(l => Array.from(l));

console.log('   ');
printHeatMap(basins);

let basinSizes = basins.flat().reduce((acc, v) => { acc[v] += 1; return acc; },Array(id+1).fill(0));
basinSizes.shift();
basinSizes.sort((a,b) => b-a);
console.log(basinSizes);

console.log(basinSizes.slice(0,3).reduce((sum,v) => sum * v, 1));

