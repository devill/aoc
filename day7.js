import { promises as fs } from 'fs';
import {GPU} from "gpu.js";

const gpu = new GPU();

let rawData = await fs.readFile('./input7.txt', 'utf8');
// let rawData = await fs.readFile('./test7.txt', 'utf8');

let data = rawData.split(',').filter(n => n !== '').map(n => parseInt(n));


let min = Math.min(...data);
let max = Math.max(...data);

let costCalculations = gpu.createKernel(function(data, length) {
    let v = this.thread.x;
    let cost = 0;
    let largeCost = 0;
    for(let i = 0; i < length; i++) {
        let n = Math.abs(data[i] - v);
        cost += n*(n+1)/2;
        while(cost > 1000000) {
            largeCost += 1;
            cost -= 1000000;
        }
    }
    return [largeCost,cost];
}).setOutput([max+1]).setStrictIntegers('unsigned');

const result_gpu = Array.from(costCalculations(data, data.length)).map(v => v[0]*1000000+v[1]);
console.log(Math.min(...result_gpu));
//
// console.log(result_gpu);
//
// let result = [];
// for(let v = 0; v < max+1; v++) {
//     let cost = 0;
//     for(let i = 0; i < data.length; i++) {
//         let n = Math.abs(data[i] - v);
//         cost += n*(n+1)/2;
//     }
//     result.push(cost);
// }
//
//
// // console.log(result.join(' '));
// console.log(min,max);
// console.log(Math.min(...result), Math.min(...result_gpu));
// console.log(Math.min(...result) - Math.min(...result_gpu));
// console.log(Math.max(...result), Math.max(...result_gpu));
//


