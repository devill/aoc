import { promises as fs } from 'fs';


const rawData = (await fs.readFile('./input23.txt', 'utf8'))
// const rawData = (await fs.readFile('./test23.txt', 'utf8'))
// const rawData = (await fs.readFile('./test23s.txt', 'utf8'))
    .split('\n')
    .map(l => l.split(''));

let data = {};

rawData.forEach((l,y) => l.forEach((v, x) => {
    if(v === '#') {
        data[`${x}_${y}`] = {x, y};
    }
}));

const directions = [
    { x: 0, y: -1},
    { x: 0, y: 1},
    { x: -1, y: 0},
    { x: 1, y: 0}
];

const deltas = [-1, 0, 1];

const checksForDirection = directions.map(d => {
    return deltas.map(delta => ({ x: d.x === 0 ? delta : d.x, y: d.y === 0 ? delta : d.y}))
});

let directionShift = 0;

const getDirectionFor = elf => {
    let count = 0;
    for(let dy = -1; dy < 2; dy++) {
        for(let dx = -1; dx < 2; dx++) {
            if(dx !== 0 || dy !== 0) {
                let [x, y] = [
                    elf.x + dx,
                    elf.y + dy
                ]
                if (!!data[`${x}_${y}`]) {
                    count++;
                }
            }
        }
    }
    if(count === 0) {
        return null;
    }
    for(let id = 0; id < directions.length; id++) {
        let i = (id + directionShift) % directions.length;
        let count = 0;
        for(let j = 0; j < checksForDirection[i].length; j++) {
            let [x, y] = [
                elf.x + checksForDirection[i][j].x,
                elf.y + checksForDirection[i][j].y
            ]
            if(data[`${x}_${y}`]) {
                count++;
            }
        }
        if(count === 0) {
            return {
                x: elf.x + directions[i].x,
                y: elf.y + directions[i].y
            };
        }
    }
    return null;
}

const getBoundingBox = data => ({
    x: {
        min: Math.min(...Object.values(data).map(v => v.x)),
        max: Math.max(...Object.values(data).map(v => v.x))
    },
    y: {
        min: Math.min(...Object.values(data).map(v => v.y)),
        max: Math.max(...Object.values(data).map(v => v.y))
    }
})

const printBoard = data => {
    const bb = getBoundingBox(data);
    let board = "\n\n";
    board += `(${bb.x.min}, ${bb.y.min})\n`;
    for(let y = bb.y.min - 1; y < bb.y.max + 2; y++) {
        for(let x = bb.x.min - 1; x < bb.x.max + 2; x++) {
            board += !data[`${x}_${y}`] ? '.' : '#';
        }
        board += "\n";
    }
    board += "\n";
    console.log(board);
}

const printMoves = (moves, bb) => {
    let board = "\n\n";
    board += `(${bb.x.min}, ${bb.y.min})\n`;
    for(let y = bb.y.min - 1; y < bb.y.max + 2; y++) {
        for(let x = bb.x.min - 1; x < bb.x.max + 2; x++) {

            board += !moves[`${x}_${y}`] ? '.' : moves[`${x}_${y}`];
        }
        board += "\n";
    }
    board += "\n";
    console.log(board);
}

printBoard(data);

for(let i = 0; i < 10; i++) {
    let targets = {};
    let proposals = [];
    let moves = Object.keys(data).reduce((d,k) => { d[k]= '#'; return d }, {});
    let bb = getBoundingBox(data);

    Object.values(data).forEach(elf => {
        const target = getDirectionFor(elf);
        if(target !== null) {
            const { x, y } = target;
            if (!targets[`${x}_${y}`]) {
                targets[`${x}_${y}`] = 0;
            }
            targets[`${x}_${y}`]++;
            proposals.push({ current: elf, next: { x, y } });
        }
    });
    proposals.forEach(({current, next}) => {
        let {x, y} = next;
        if(targets[`${x}_${y}`] === 1) {
            data[`${x}_${y}`] = { x, y };
            delete data[`${current.x}_${current.y}`];
            moves[`${current.x}_${current.y}`] = ['^', '<', 'O', '>', 'v'][(x - current.x) + 2 * (y - current.y) + 2]
        }
    })

    // console.log('Round:', i);
    // printMoves(moves, bb);
    // printBoard(data);
    directionShift++;
}

printBoard(data);
let bb = getBoundingBox(data);
const totalCells = (bb.x.max - bb.x.min + 1) * (bb.y.max - bb.y.min + 1);
console.log(totalCells - Object.keys(data).length);