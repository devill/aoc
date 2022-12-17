import { promises as fs } from 'fs';

const maxRocks = 1000000000000;
// const maxRocks = 2022;
let data = (await fs.readFile('./input17.txt', 'utf8'))
// let data = (await fs.readFile('./test17.txt', 'utf8'))
    .split('')
    .map(d => d === '>' ? 1 : -1);

let rocks = [
    ['####'],
    ['.#.', '###', '.#.'],
    ['..#','..#','###'],
    ['#','#','#','#'],
    ['##','##']
].map((r) => r.map((l,y) => l.split('')
    .map((c,x) => [x,y, c])
    .filter(c => c[2] === '#')
    .map(c => c.slice(0,2))
).flat());

let rockBottoms = rocks.map(r => Math.max(...r.map(c => c[1])));
let chamberTop = 0;
let chamberContent = [];

const collides = (rockPosition, rock) => {
    for(let i = 0; i < rock.length; i++) {

        const c = [rockPosition[0] + rock[i][0], rockPosition[1] - rock[i][1]];
        if(c[0] < 0 || c[0] >= 7) return true;
        if(c[1] < 0) return true;
        if(chamberContent[c[1]][c[0]] !== '.') return true;

    }
    return false;
}

let tops = Array(7).fill(0);
let pushId = 0;

let maxFall = 0;
let cache = {};
let step = 0;
let offset = 0;
for(let i = 0; i < maxRocks; i++) {
    while(chamberContent.length < chamberTop + 7) {
        chamberContent.push(Array(7).fill('.'));
    }

    let nextRock = rocks[i%5];
    const rockBottom = rockBottoms[i%5];
    let rockPosition = [2, chamberTop + 3 + rockBottom];
    let fall = 0;
    while(true) {
        rockPosition[0] += data[pushId];
        if(collides(rockPosition,nextRock)) rockPosition[0] -= data[pushId];
        pushId = (pushId + 1) % data.length;
        step++;
        if(pushId === 0) {
            const c = chamberContent.slice(-maxFall-7, -7).map(l => l.join('')).join(' ') + " - " + (i%5).toString() + "," + rockPosition[0].toString() + "," + fall.toString();
            console.log(c);
            if(cache[c]) {
                const jump = i - cache[c].i;
                offset = Math.floor((maxRocks - i)/jump) * (chamberTop - cache[c].chamberTop);
                i += Math.floor((maxRocks - i)/jump) * jump;
                cache = {};
            } else {
                cache[c] = { i:i, chamberTop: chamberTop };
            }
        }
        rockPosition[1] -= 1;
        fall++;

        if(collides(rockPosition,nextRock)) {
            rockPosition[1] += 1;
            break;
        }

    }
    maxFall = Math.max(maxFall, fall);
    nextRock.forEach(p => {
        chamberContent[rockPosition[1]-p[1]][rockPosition[0]+p[0]] = ['-','+','>','|','#'][i%5];
        tops[rockPosition[0]+p[0]] = Math.max(tops[rockPosition[0]+p[0]], rockPosition[1]-p[1]);
    });
    chamberTop = Math.max(chamberTop,rockPosition[1]+1);
}
//console.log(chamberContent.map(l => l.join('')).reverse().join('\n'), '\n\n');
console.log(data.length, maxFall);
console.log(tops);
console.log(chamberTop + offset);