import { promises as fs } from 'fs';


let [rawBoard, rawInstructions] = (await fs.readFile('./input22.txt', 'utf8'))
// const [rawBoard, rawInstructions] = (await fs.readFile('./test22.txt', 'utf8'))
    .split('\n\n');

// rawInstructions = "3R16R1L11L4R28R10L5L10";
const boardTmp = rawBoard.split('\n').map(l => l.split(''));
let maxWidth = Math.max(...boardTmp.map(l => l.length));
const board = boardTmp.map(l => l.concat(Array(maxWidth-l.length).fill(' ')));


const instructions = rawInstructions
    .replace(/([RL])/g, ' $1 ')
    .split(' ')
    .map(item => item.match(/\d+/) ? parseInt(item) : item);

let mapOfMoves = board.map(l => [...l]);

let position = { x: board[0].findIndex(v => v === '.'), y: 0 };
let direction = 0;

const rotations = {
    'L': d => (d + 3) % 4,
    'R': d => (d + 1) % 4
}

const directionToVector = direction =>
    ({
        x: Math.round(Math.cos(direction * Math.PI/2)),
        y: Math.round(Math.sin(direction * Math.PI/2))
    });
/*
const jumpRules = [
    [
        { from: {x: [100, 100], y:[0, 50]}, to: { x: [99, 99], y: [149, 99]}, newDirection: 2 },
        { from: {x: [50,50], y:[50,100]}, to: { x: [50,100], y: [49,49]}, newDirection: 3 },
        { from: {x: [50,50], y:[100,150]}, to: { x: [149,149], y: [49,-1]}, newDirection: 2 },
        { from: {x: [0,0], y:[150,200]}, to: { x: [50,100], y: [149,149]}, newDirection: 3 },
    ],
    [
        { from: {x: [100,150], y:[0,0]}, to: { x: [99,99], y: [50,100]}, newDirection: 1 },
        { from: {x: [0, 50], y:[150, 150]}, to: { x: [100, 150], y: [0, 0]}, newDirection: 1 },
        { from: {x: [50,100], y:[100,100]}, to: { x: [49,49], y: [150,200]}, newDirection: 2 },
    ],
    [
        { from: {x: [50, 50], y:[0, 50]}, to: { x: [0, 0], y: [149, 99]}, newDirection: 0 },
        { from: {x: [50, 50], y:[50, 100]}, to: { x: [0, 50], y: [100, 100]}, newDirection:  1},
        { from: {x: [0, 0], y:[100, 150]}, to: { x: [50,50], y: [49, -1]}, newDirection: 0 },
        { from: {x: [0, 0], y:[150,200]}, to: { x: [50,100], y: [0,0]}, newDirection: 1 },

    ],
    [
        { from: {x: [50, 100], y:[0,0]}, to: { x: [0,0], y: [150, 200]}, newDirection: 0 },
        { from: {x: [100,150], y:[0,0]}, to: { x: [0,50], y: [199,199]}, newDirection: 3 },
        { from: {x: [0, 50], y:[100, 100]}, to: { x: [50, 50], y: [50, 100]}, newDirection: 0 },
    ],
]

const roundToCorner = (point) => ({
    x: Math.floor(point.x / 50) * 50,
    y: Math.floor(point.y / 50) * 50
});

const jumpEdge = (position, direction)  => {
    const corner = roundToCorner(position);
    for(let rule of jumpRules[direction]) {
        if(rule.from.x[0] === corner.x && rule.from.y[0] === corner.y) {
            let id = (direction % 2 === 1) ? position.x - corner.x : position.y - corner.y;
            return [
                {
                    x: rule.to.x[0] + id * (rule.to.x[1] - rule.to.x[0])/50,
                    y: rule.to.y[0] + id * (rule.to.y[1] - rule.to.y[0])/50
                },
                rule.newDirection
            ];
        }
    }
    return null;
}
*/

const roundToCorner = (point) => ({
    x: Math.floor(point.x / 50) * 50,
    y: Math.floor(point.y / 50) * 50
});

//
const jumpRules = [
    [
        { start:   0, to: { start: { x:  99, y: 149 }, edgeDirection: 3 }, newDirection: 2 },
        { start:  50, to: { start: { x: 100, y:  49 }, edgeDirection: 0 }, newDirection: 3 },
        { start: 100, to: { start: { x: 149, y:  49 }, edgeDirection: 3 }, newDirection: 2 },
        { start: 150, to: { start: { x:  50, y: 149 }, edgeDirection: 0 }, newDirection: 3 },
    ],
    [
        { start:   0, to: { start: { x: 100, y:   0 }, edgeDirection: 0 }, newDirection: 1 },
        { start:  50, to: { start: { x:  49, y: 150 }, edgeDirection: 1 }, newDirection: 2 },
        { start: 100, to: { start: { x:  99, y:  50 }, edgeDirection: 1 }, newDirection: 2 },
    ],
    [
        { start:   0, to: { start: { x:   0, y: 149 }, edgeDirection: 3 }, newDirection: 0 },
        { start:  50, to: { start: { x:   0, y: 100 }, edgeDirection: 0 }, newDirection: 1 },
        { start: 100, to: { start: { x:  50, y:  49 }, edgeDirection: 3 }, newDirection: 0 },
        { start: 150, to: { start: { x:  50, y:   0 }, edgeDirection: 0 }, newDirection: 1 },
    ],
    [
        { start:   0, to: { start: { x:  50, y:  50 }, edgeDirection: 1 }, newDirection: 0 },
        { start:  50, to: { start: { x:   0, y: 150 }, edgeDirection: 1 }, newDirection: 0 },
        { start: 100, to: { start: { x:   0, y: 199 }, edgeDirection: 0 }, newDirection: 3 },
    ],
];
let jumps = 0;
const jumpEdge = (position, direction) => {
    jumps++;
    const corner = roundToCorner(position);
    for(let rule of jumpRules[direction]) {
        if(
            (direction % 2 === 0 && rule.start === corner.y) ||
            (direction % 2 === 1 && rule.start === corner.x)
        ) {
            let id = (direction % 2 === 1) ? position.x - corner.x : position.y - corner.y;
            const vector = directionToVector(rule.to.edgeDirection);
            const result = [
                {
                    x: rule.to.start.x + id * vector.x,
                    y: rule.to.start.y + id * vector.y
                },
                rule.newDirection
            ];
            console.log("\npos", position, "\ndir", direction, "\nid", id, "\nrule", rule, "\nvector", vector, "\nresult", result);
            return result;
        }
    }
    return null;
}

const move = (position, direction, distance) => {
    for(let i = 0; i < distance; i++) {
        const v = directionToVector(direction);
        const oldPosition = {...position};
        const oldDirection = direction;
        [position.x,position.y] = [
            (position.x + v.x + maxWidth) % maxWidth,
            (position.y + v.y + board.length) % board.length
        ]

        if(board[position.y][position.x] === ' ') {
            [position, direction] = jumpEdge(oldPosition, direction);
            console.log
        }
        if(board[position.y][position.x] === '#') {
            console.log("Blocked at", oldPosition, position);
            return [oldPosition, oldDirection];
        }
        mapOfMoves[position.y][position.x] = ['>', 'v', '<', '^'][direction];
    }
    return [position, direction];
}


console.log(position, direction);
mapOfMoves[position.y][position.x] = ['>', 'v', '<', '^'][direction];
try {
    instructions.forEach(instruction => {
        if (['L', 'R'].includes(instruction)) {
            direction = rotations[instruction](direction);
            mapOfMoves[position.y][position.x] = ['>', 'v', '<', '^'][direction];
        } else {
            [position, direction] = move(position, direction, instruction);
            // if(jumps > 2) throw "stop";
        }
        //console.log(position, direction);
    });
} catch (e) {
    console.log(e);
}

console.log(mapOfMoves.map(l => l.join('')).join('\n'));

console.log(position, direction, maxWidth, board.length);
console.log(1000 * (position.y + 1) + 4 * (position.x + 1) + direction);

