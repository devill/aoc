import { promises as fs } from 'fs';

let data = (await fs.readFile('./input18.txt', 'utf8'))
// let data = (await fs.readFile('./test18.txt', 'utf8'))
    .split('\n')
    .map(l => l.split(',').map(c => parseInt(c)));

let faces = {};
let count = 0;
data.forEach(c => {
    [
        [...c, 'x'].join('_'),
        [...c, 'y'].join('_'),
        [...c, 'z'].join('_'),
        [c[0]+1,c[1],c[2],'x'].join('_'),
        [c[0],c[1]+1,c[2],'y'].join('_'),
        [c[0],c[1],c[2]+1,'z'].join('_')
    ].forEach(face => {
        if(!faces[face]) {
            faces[face] = 1;
            count += 1;
        } else if(faces[face] === 1) {
            faces[face] = 2;
            count -= 1;
        } else {
            console.log(face);
            console.log('WTF, this should not happen');
        }
    })

});

console.log(count);

let boundingBox = [
    [Math.min(...data.map(c => c[0]))-1, Math.max(...data.map(c => c[0])) + 1],
    [Math.min(...data.map(c => c[1]))-1, Math.max(...data.map(c => c[1])) + 1],
    [Math.min(...data.map(c => c[2]))-1, Math.max(...data.map(c => c[2])) + 1],
]



let cubes = {}
data.forEach(c => {
    cubes[c.join('_')] = 'lava';
});

let stack = [boundingBox.map(b => b[1])];

let deltas = Array(3).fill(0).flatMap((_,i) => [
    Array(3).fill(0).map((_,j) => i===j ? 1: 0),
    Array(3).fill(0).map((_,j) => i===j ? -1: 0)
]);
console.log(deltas);

let outerCount = 0;
while(stack.length > 0) {
    const c = stack.pop();
    deltas
        .map(d => d.map((v,i) => v + c[i]))
        .forEach(n => {
            if(n.filter((v,i) => v < boundingBox[i][0] || v > boundingBox[i][1]).length > 0) {
                // console.log(n, ' is out of bounds');
            } else if(!cubes[n.join('_')]) {
                cubes[n.join('_')] = 'outside';
                stack.push(n);
            } else if(cubes[n.join('_')] === 'lava') {
                outerCount += 1;
            }
        });
}

console.log(cubes);
console.log(outerCount);

