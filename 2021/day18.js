import { promises as fs } from 'fs';

let rawData = await fs.readFile('./input18.txt', 'utf8');
// let rawData = await fs.readFile('./test18.txt', 'utf8');

// let data = rawData.split('\n').map(l => eval(l));

// const snailNumberToString = (n)  => {
//     if(Array.isArray(n)) return '[' + n.map(i => snailNumberToString(i)).join(',') + ']';
//     return n.toString();
// }

// console.log(data.map(l => snailNumberToString(l)).join('\n'));

const parseLine = (l) => l.split('').map(c => ['[',']',','].includes(c) ? c : parseInt(c));

let data = rawData.split('\n').map(l => parseLine(l));

const doExplode = (n) => {
    let depth = 0;
    let previous = null;

    for(let i = 0; i < n.length; i++) {

        switch (n[i]) {
            case '[':
                depth++;
                if(depth === 5) {
                    if(previous) n[previous] += n[i+1];
                    for (let j = i+4; j < n.length; j++) {

                        if(Number.isInteger(n[j])) {
                            n[j] += n[i+3];
                            break;
                        }
                    }
                    n.splice(i, 5, 0);
                    return true;
                }
                break;
            case ']':
                depth--;
                break;
            case ',':
                break;
            default:
                previous = i;
                break;
        }
    }
    return false;
}

const doSplit = (n) => {
    for(let i = 0; i < n.length; i++) {
        if(Number.isInteger(n[i]) && n[i] >= 10) {
            let f = Math.floor(n[i]/2);
            let c = Math.ceil(n[i]/2);
            n.splice(i,1,'[',f,',',c,']');
            return true;
        }
    }
    return false;
}

const snailReduce = (n) => {
    while(doExplode(n) || doSplit(n)) {
    }
    return n;
}

const snailMagnitude = (n) => {
    let values = [[]];
    for(let i = 0; i < n.length; i++) {
        switch (n[i]) {
            case '[':
                values.push([]);
                break;
            case ']':
                let v = values.pop();
                values[values.length - 1].push(3*v[0]+2*v[1]);
                break;
            case ',':
                break;

            default:
                values[values.length - 1].push(n[i]);
        }
    }
    return values[0][0];
}

const snailAdd = (l, r) => {

    let sum = snailReduce(['[',...l,',',...r,']']);
    return sum;
}

let snailSum = data.reduce((s, i) => snailAdd(s,i));
console.log(snailSum.join(''));
console.log(snailMagnitude(snailSum));

let maxMagnitude = 0;
for(let i = 0; i < data.length; i++) {
    for(let j = 0; j < data.length; j++) {
        let magnitude = snailMagnitude(snailAdd(data[i],data[j]));
        console.log(magnitude);
        maxMagnitude = Math.max(maxMagnitude, magnitude);
    }

}

console.log(maxMagnitude);

// snailAdd(data[0],data[1]);

// console.log(data[0]);
// snailReduce(data[0]);

// let example = parseLine('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]');
// console.log(example.join(''));
// console.log(snailMagnitude(example));

