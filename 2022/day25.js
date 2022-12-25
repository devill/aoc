import { promises as fs } from 'fs';

const SNAFUdigits = {
    0: 0,
    1: 1,
    2: 2,
    '-': -1,
    '=': -2,
}

let data = (await fs.readFile('./input25.txt', 'utf8'))
// let data = (await fs.readFile('./test25.txt', 'utf8'))
    .split('\n')
    .map(l => l.split(''))
    .map(l => l.map(d => SNAFUdigits[d]))
    .map(l => l.reverse().reduce((v, d, i) => v + Math.pow(5, i) * d), 0);

console.log(data);

let sum = data.reduce((sum, v) => sum + v);

console.log(sum);

const decimalToSNAFU = n => {
    let SNAFU = "";
    if(n === 0) return "0";
    while(n > 0) {
        let d = n % 5;
        SNAFU = `${['0','1','2','=','-'][d]}${SNAFU}`;
        if(d > 2) d -= 5;
        n -= d;
        n /= 5;
        n = Math.round(n);
    }
    return SNAFU;
}

// console.log(Array(10).fill(0).map((_,i) => i).concat([10,15,20,2022,12345, 314159265]).map(decimalToSNAFU).join('\n'));
// console.log(decimalToSNAFU(2022));

console.log(decimalToSNAFU(sum));