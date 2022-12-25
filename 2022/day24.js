import { promises as fs } from 'fs';

let data = (await fs.readFile('./input24.txt', 'utf8'))
// let data = (await fs.readFile('./test24.txt', 'utf8'))
    .split('\n')
    .map(l => l.split(''));

const directions = {
    '>': { x: 1, y: 0 },
    'v': { x: 0, y: 1 },
    '<': { x: -1, y: 0 },
    '^': { x: 0, y: -1 },
    'wait': { x: 0, y: 0 }
}

let blizards = [];

data.forEach((l,y) => l.forEach((v, x) => {
    if(directions[v]) {
        blizards.push({
            direction: directions[v],
            initialPosition: { x, y }
        })
    }
}));

let step = 0;
let reachableThisStep = {
    '1_0': { x: 1, y: 0}
};

const positiveModulus = (n, m) => (n % m < 0) ? n % m + m : n % m;

const blizzardKey = blizzard => {
    const x = positiveModulus(blizzard.initialPosition.x - 1 + blizzard.direction.x * step, data[0].length - 2) + 1;
    const y = positiveModulus(blizzard.initialPosition.y - 1 + blizzard.direction.y * step, data.length - 2) + 1;
    return `${x}_${y}`;
}

const boundary = (x,y) => {
    if(`${x}_${y}` === '1_0' || `${x}_${y}` === `${data[0].length - 2}_${data.length - 1}` ) return false;
    return x <= 0 || x >= data[0].length - 1 || y <= 0 || y >= data.length - 1;
}

let targetKeys =  [
    `${data[0].length - 2}_${data.length - 1}`,
    `1_0`,
    `${data[0].length - 2}_${data.length - 1}`,
];

targetKeys.forEach( targetKey => {
    while (!reachableThisStep[targetKey]) {
        step++;
        let blocked = blizards.reduce((acc, blizzard) => {
            acc[blizzardKey(blizzard)] = true
            return acc;
        }, {});

        reachableThisStep = Object.values(reachableThisStep).reduce((acc, p) => {
            Object.values(directions).forEach(d => {
                let [x, y] = [p.x + d.x, p.y + d.y];
                if (!blocked[`${x}_${y}`] && !boundary(x, y)) {
                    acc[`${x}_${y}`] = {x, y};
                }
            })
            return acc;
        }, {})

        /*
        console.log(data.map((l,y) => l.map((v,x) => {
            if(v === '#') return '#';
            if(blocked[`${x}_${y}`]) return '@';
            if(reachableThisStep[`${x}_${y}`]) return '+';
            return ' '
        }).join('')).join('\n'));

        console.log(step, reachableThisStep);
         */
    }
    console.log(targetKey, step);
    reachableThisStep = {
        targetKey: reachableThisStep[targetKey]
    };
});
