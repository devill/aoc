import { promises as fs } from 'fs';
import {GPU} from "gpu.js";

const gpu = new GPU();


let rawData = await fs.readFile('./input20.txt', 'utf8');
// let rawData = await fs.readFile('./test20.txt', 'utf8');

rawData = rawData.split('\n')

let enhancement = rawData.shift().split('').map(d => d === '#' ? 1 : 0);
console.log(enhancement.length);
rawData.shift();

let image = rawData.map(l => l.split('').map(d => d === '#' ? 1 : 0));

const printImage = (image) => {
    console.log(image[0].length, image.length);
    console.log(image.map(l => l.map(c => c === 1 ? '#' : '.').join('')).join('\n'));
}

const enhance = (image, iteration) => {
    let width = image[0].length;
    let height = image.length;

    const padKernel = gpu.createKernel(function(image, width, height, padWith) {
        if(this.thread.x < 2 || this.thread.x > width + 1) return padWith;
        if(this.thread.y < 2 || this.thread.y > height + 1) return padWith;
        return image[this.thread.y - 2][this.thread.x - 2];
    })
        .setStrictIntegers(true)
        .setOutput([width + 4, height + 4]);

    const enhanceKernel = gpu.createKernel(function(image, enhancement) {
        let x = this.thread.x + 1;
        let y = this.thread.y + 1;

        let index =
            256 * image[y - 1][x - 1] +
            128 * image[y - 1][x + 0] +
            64  * image[y - 1][x + 1] +
            32  * image[y + 0][x - 1] +
            16  * image[y + 0][x + 0] +
            8   * image[y + 0][x + 1] +
            4   * image[y + 1][x - 1] +
            2   * image[y + 1][x + 0] +
            1   * image[y + 1][x + 1];

        return enhancement[index];
    })
        .setStrictIntegers(true)
        .setOutput([width + 2, height + 2]);

    let padded = padKernel(image, width, height, iteration % 2).map(l => [...l]);
    return enhanceKernel(padded, enhancement).map(l => [...l]);
}



for(let it = 0; it < 50; it++) {
    image = enhance(image, it);
}
printImage(image);

console.log(image.flat().reduce((s,v) => s+v));