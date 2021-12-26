import {promises as fs} from 'fs';
import {GPU} from "gpu.js";

const gpu = new GPU();

let rawData = await fs.readFile('./input22.txt', 'utf8');
// let rawData = await fs.readFile('./test22.txt', 'utf8');
// let rawData = await fs.readFile('./test22_1.txt', 'utf8');
// let rawData = await fs.readFile('./test22_2.txt', 'utf8');

let data = rawData
    .split('\n')
    .map(l => l
        .match(/(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)/)

    ).map(l => [l[1] === 'on' ? 1 : 0, ...l.slice(2).map(d => parseInt(d))]);

const getUniq = a => [...new Set(a)].sort((a,b) => a-b);
const getMap = coords => {
    return coords.reduce((m, v, i) => {
        m[v] = i;
        return m;
    }, {})
}

const xCoords = getUniq([...data.map(l => l[1]), ...data.map(l => l[2]+1)]);
const yCoords = getUniq([...data.map(l => l[3]), ...data.map(l => l[4]+1)]);
const zCoords = getUniq([...data.map(l => l[5]), ...data.map(l => l[6]+1)]);

const xMap = getMap(xCoords);
const yMap = getMap(yCoords);
const zMap = getMap(zCoords);

const compressedData = data.map(l => [l[0], xMap[l[1]], xMap[l[2]+1], yMap[l[3]], yMap[l[4]+1], zMap[l[5]], zMap[l[6]+1]])
const performActions = gpu.createKernel(function(z, actions, actionsLength) {
    let result = 0;
    for(let i = 0; i < actionsLength; i++) {
        if (
            this.thread.x >= actions[i][1] &&
            this.thread.x < actions[i][2] &&
            this.thread.y >= actions[i][3] &&
            this.thread.y < actions[i][4] &&
            z >= actions[i][5] &&
            z < actions[i][6]
        ) {
            result = actions[i][0];
        }
    }
    return result;
})
    .setStrictIntegers(true)
    .setOutput([xCoords.length - 1, yCoords.length - 1]);

const total = Array(zCoords.length - 1)
    .fill(0)
    .map((s,z) => {
            console.log(z);

            return performActions(z, compressedData, compressedData.length)
                .map(l => [...l])
                .map((line, y) => line.map((on, x) => {
                    return Math.round(on) * (xCoords[x + 1] - xCoords[x]) * (yCoords[y + 1] - yCoords[y]) * (zCoords[z + 1] - zCoords[z])
                }))
                .flat()
                .reduce((s, t) => s+t);
        }
    )
    .reduce((s,v) => s + v);

console.log(total);
console.log(total-1282401587270826);
