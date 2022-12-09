import { promises as fs } from 'fs';

let data = (await fs.readFile('./input8.txt', 'utf8'))
// let data = (await fs.readFile('./test8.txt', 'utf8'))
    .split('\n')
    .slice(0, -1)
    .map(l => l.split('').map(d => parseInt(d)));

console.log(data.length, data[0].length);
console.log(data.map(l => l.join('')).join('\n'));

let visibles = Array(data.length).fill(null).map(l => Array(data[0].length).fill(0));
let visibleCount = 0;
for(let i = 0; i < data.length; i++) {
    for(let j = 0; j < data[i].length; j++) {
        let thisTree = data[i][j];
        let isVisibleLeft = true;
        let isVisibleRight = true;
        let isVisibleTop = true;
        let isVisibleBottom = true;
        for(let k = 0; k < data.length; k++) {
            if(k < j) isVisibleTop = isVisibleTop && data[i][k] < thisTree
            if(k > j) isVisibleBottom = isVisibleBottom && data[i][k] < thisTree
            if(k < i) isVisibleLeft = isVisibleLeft && data[k][j] < thisTree
            if(k > i) isVisibleRight = isVisibleRight && data[k][j] < thisTree
        }
        visibles[i][j] = isVisibleLeft || isVisibleRight || isVisibleTop ||  isVisibleBottom ? 1 : 0;
        visibleCount += visibles[i][j];
    }
}
console.log('');
console.log(visibles.map(l => l.join('')).join('\n'));
console.log(visibleCount);

const look = (i, j, di, dj) => {
    let s = 0;
    while(true) {
        s += 1;
        let k = i + di * s;
        let l = j + dj * s;
        if(k < 0 || k >= data.length) return s - 1;
        if(l < 0 || l >= data[i].length) return s - 1;
        if(data[i][j] <= data[k][l]) return s;
    }
}

let scores = Array(data.length).fill(null).map(l => Array(data[0].length).fill(0));
for(let i = 0; i < data.length; i++) {
    for(let j = 0; j < data[i].length; j++) {
        scores[i][j] = look(i,j,1,0) * look(i,j,-1,0) * look(i,j,0,1) * look(i,j,0,-1);
    }
}
console.log('');
console.log(Math.max(...scores.map(l => Math.max(...l))));
