import { promises as fs } from 'fs';

let rawData = await fs.readFile('./input13.txt', 'utf8');
// let rawData = await fs.readFile('./test13.txt', 'utf8');

let [rawDots, rawFolds] = rawData.split('\n\n').map(g => g.split('\n'));

let dots = rawDots.map(l => l.split(',').map(c => parseInt(c))).map(([x,y]) => ({x,y}));
let folds = rawFolds
    .map(l => l
        .match(/fold along (?<direction>\w)=(?<coordinate>\d+)/).groups
    );

const fold = (direction, coordinate) => {
    return ({x,y}) => {
        switch (direction) {
            case 'x':
                return {x: coordinate - Math.abs(x - coordinate), y};
            case 'y':
                return {x, y:coordinate - Math.abs(y - coordinate)};
        }
    }
}

let foldedDots = Object.values(dots.reduce((b,sourceDot) => {
    let dot = folds.reduce((dot, nextFold) => fold(nextFold.direction, nextFold.coordinate)(dot), sourceDot)
    b[`${dot.x}_${dot.y}`] = dot;
    return b;
},{}))

// console.log(foldedDots);

const printBoard = (board) => {
    let sizex = Math.max(...board.map(({x}) => x)) + 1;
    let sizey = Math.max(...board.map(({y}) => y)) + 1;

    console.log(board.reduce((b, d) => {
        b[d.y][d.x] = '*';
        return b;
    }, Array(sizey).fill(0).map(l => Array(sizex).fill('.'))).map(l => l.join('')).join('\n'));

}

printBoard(foldedDots);
// RZKZLPGH


