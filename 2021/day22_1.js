import { promises as fs } from 'fs';
import {GPU} from "gpu.js";

const gpu = new GPU();

let rawData = await fs.readFile('./input22.txt', 'utf8');
// let rawData = await fs.readFile('./test22.txt', 'utf8');

let data = rawData
    .split('\n')
    .map(l => l
        .match(/(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)/)

    ).map(l => [l[1] === 'on' ? 1 : 0, ...l.slice(2).map(d => parseInt(d))]);


 const performActions = gpu.createKernel(function(cells, actions, actionsLength) {
     let result = 0;
     for(let i = 0; i < actionsLength; i++) {
         if (
             this.thread.x - 50 >= actions[i][1] &&
             this.thread.x - 50 <= actions[i][2] &&
             this.thread.y - 50 >= actions[i][3] &&
             this.thread.y - 50 <= actions[i][4] &&
             this.thread.z - 50 >= actions[i][5] &&
             this.thread.z - 50 <= actions[i][6]
         ) {
             result = actions[i][0];
         }
     }
    return result;
})
     .setStrictIntegers(true)
     .setOutput([101,101,101]);


let cells = Array(101).fill(0).map(l => Array(101).fill(0).map(l => Array(101).fill(0)));

let result = performActions(cells, data, data.length).map(l => [...l.map(l => [...l])]);
console.log(result.flat().flat().reduce((s,t) => s+t));
