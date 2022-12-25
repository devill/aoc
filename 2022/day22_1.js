import { promises as fs } from 'fs';


const [rawBoard, rawInstructions] = (await fs.readFile('./input22.txt', 'utf8'))
// const [rawBoard, rawInstructions] = (await fs.readFile('./test22.txt', 'utf8'))
    .split('\n\n');

const board = rawBoard.split('\n').map(l => l.split(''));

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

let maxWidth = Math.max(...board.map(l => l.length));

const move = (position, direction, distance) => {
    const v = directionToVector(direction);
    for(let i = 0; i < distance; i++) {
        const oldPosition = {...position};
        do {
            position.y = (position.y + v.y + board.length) % board.length;
            position.x = (position.x + v.x + maxWidth) % maxWidth;
        } while (board[position.y].length <= position.x || board[position.y][position.x] === ' ');

        if(board[position.y][position.x] === '#') {
            return oldPosition;
        }
        mapOfMoves[position.y][position.x] = ['>', 'v', '<', '^'][direction];
    }
    return position;
}


console.log(position, direction);
mapOfMoves[position.y][position.x] = ['>', 'v', '<', '^'][direction];
instructions.forEach(instruction => {
    if(['L','R'].includes(instruction)) {
        direction = rotations[instruction](direction);
        mapOfMoves[position.y][position.x] = ['>', 'v', '<', '^'][direction];
    } else {
        position = move(position, direction, instruction);
    }
    //console.log(position, direction);
});

console.log(mapOfMoves.map(l => l.join('')).join('\n'));

console.log(position, direction, maxWidth, board.length);
console.log(1000 * (position.y + 1) + 4 * (position.x + 1) + direction);

