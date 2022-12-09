import { promises as fs } from 'fs';

let data = (await fs.readFile('./input9.txt', 'utf8'))
// let data = (await fs.readFile('./test9.txt', 'utf8'))
// let data = (await fs.readFile('./test9_2.txt', 'utf8'))
    .split('\n')
    .slice(0, -1)
    .map(l => l.split(' '));

let usedShortTail = { '0_0': true };
let usedLongTail = { '0_0': true };
let countShortTail = 1;
let countLongTail = 1;
let rope = Array(10).fill(0).map(k => [0,0]);


data.forEach(l => {
    for (let i = 0; i < parseInt(l[1]); i++){
        if(l[0] === 'U') rope[0][0]--;
        if(l[0] === 'D') rope[0][0]++;
        if(l[0] === 'L') rope[0][1]--;
        if(l[0] === 'R') rope[0][1]++;

        for(let j = 1; j < 10; j++) {
            if (Math.abs(rope[j][0] - rope[j-1][0]) + Math.abs(rope[j][1] - rope[j-1][1]) > 2) {
                rope[j][0] += -1 * Math.sign(rope[j][0] - rope[j-1][0]);
                rope[j][1] += -1 * Math.sign(rope[j][1] - rope[j-1][1]);
            } else {
                if (Math.abs(rope[j][0] - rope[j-1][0]) > 1) rope[j][0] += -1 * Math.sign(rope[j][0] - rope[j-1][0]);
                if (Math.abs(rope[j][1] - rope[j-1][1]) > 1) rope[j][1] += -1 * Math.sign(rope[j][1] - rope[j-1][1]);
            }
        }


        if(!usedShortTail[`${rope[1][0]}_${rope[1][1]}`]) {
            usedShortTail[`${rope[1][0]}_${rope[1][1]}`] = true;
            countShortTail++;
        }
        if(!usedLongTail[`${rope[9][0]}_${rope[9][1]}`]) {
            usedLongTail[`${rope[9][0]}_${rope[9][1]}`] = true;
            countLongTail++;
        }
        /*
        for(let y = -19; y < 20; y++) {
            for(let x = -19; x < 20; x++) {

                process.stdout.write(".");
            }
            process.stdout.write("\n");
        }
        process.stdout.write("\n\n\n");
        */
    }
});

console.log(countShortTail);
console.log(countLongTail);