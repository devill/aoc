import { promises as fs } from 'fs';

let data = (await fs.readFile('./input14.txt', 'utf8'))
// const data = (await fs.readFile('./test14.txt', 'utf8'))
    .split('\n')
    .map(l => l
        .split(' -> ')
        .map(p => p.split(','))
        .map(p => ({x: parseInt(p[0]), y: parseInt(p[1])}))
    );

const allCoordinatePairs = data.flat().flat();
const xCoordinates = allCoordinatePairs.map(p => p.x);
const yCoordinates = allCoordinatePairs.map(p => p.y);
const bounds = { x: [Math.min(...xCoordinates), Math.max(...xCoordinates)], y: [Math.min(...yCoordinates), Math.max(...yCoordinates)]}
const pointId = (p) => `${p.x}_${p.y}`;

let blocks = {};
data.forEach(line => {
    for(let lineId = 1; lineId < line.length; lineId++) {

        let p = {...line[lineId-1]};
        if(line[lineId-1].x !== line[lineId].x) {
            while (p.x !== line[lineId].x) {
                blocks[pointId(p)] = '#';
                p.x += line[lineId].x - line[lineId - 1].x < 0 ? -1 : 1;
            }
            blocks[pointId(p)] = '#';
        } else {
            while (p.y !== line[lineId].y) {
                blocks[pointId(p)] = '#';
                p.y += line[lineId].y - line[lineId - 1].y < 0 ? -1 : 1;
            }
            blocks[pointId(p)] = '#';
        }
    }
});

console.log(data);
console.log(bounds);

const display = () => {
    console.log('\n\n');
    for (let y = 0; y <= bounds.y[1]+5; y++) {
        let lin = ""
        for (let x = bounds.x[0]-2; x <= bounds.x[1]+2; x++) {
            lin += blocks[pointId({x: x, y: y})] || '.';
        }
        console.log(lin);
    }
}

display();
let sand = { x: 500, y:0 };
let count = 0;
while(true) {
    if(!blocks[pointId({x:sand.x, y:sand.y+1})] && sand.y < bounds.y[1] + 1) {
        sand = {x:sand.x, y:sand.y+1};
    } else if(!blocks[pointId({x:sand.x-1, y:sand.y+1})] && sand.y < bounds.y[1] + 1) {
        sand = {x:sand.x-1, y:sand.y+1};
        bounds.x[0] = Math.min(bounds.x[0], sand.x-1);
    } else if(!blocks[pointId({x:sand.x+1, y:sand.y+1})] && sand.y < bounds.y[1] + 1) {
        sand = {x:sand.x+1, y:sand.y+1};
        bounds.x[1] = Math.max(bounds.x[1], sand.x+1);
    } else {
        if(sand.x === 500 && sand.y === 0) break;
        blocks[pointId(sand)] = 'o';
        sand = { x: 500, y:0 };
        count++;

    }
}
blocks['500_0'] = 'o';
count++;
display();
console.log(count);