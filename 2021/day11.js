import { promises as fs } from 'fs';

let rawData = await fs.readFile('./input11.txt', 'utf8');
// let rawData = await fs.readFile('./test11.txt', 'utf8');

let data = rawData.split('\n').map(l => l.split('').map(d => parseInt(d)));

const deltas = [
    [-1, -1],
    [-1, 0],
    [-1, 1],
    [0, -1],
    [0, 0],
    [0, 1],
    [1, -1],
    [1, 0],
    [1, 1]
];

const propagate = (x,y) => {
    if(x < 0 || x > 9 || y < 0 || y > 9) return;
    data[x][y]++;
    if(data[x][y] === 10) {
        deltas.forEach(([dx, dy]) => {
            propagate(x+dx,y+dy);
        });
    }
}

let flashes = 0;

for(let iteration = 0; iteration < 1000; iteration++) {
    let flashAtOnce = 0;
    for(let i = 0; i < 10; i ++) {
        for(let j = 0; j < 10; j++) {
            propagate(i,j);
        }
    }

    for(let i = 0; i < 10; i ++) {
        for(let j = 0; j < 10; j++) {
            if (data[i][j] > 9) {
                data[i][j] = 0;
                flashes++;
                flashAtOnce++;
            } else {
                data[i][j] = data[i][j];
            }
        }
    }
    if(flashAtOnce === 100) {
        console.log(' ');
        console.log('Flashes:', flashes);
        console.log('Iteration', iteration + 1);
        console.log(data.map(l => l.map(c => c === 0 ? '*' : c)).map(l => l.join('')).join(['\n']));
        break;
    }
}

console.log('Flashes:', flashes);
