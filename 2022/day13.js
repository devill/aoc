import { promises as fs } from 'fs';


const parse = (string) => {
    if(string[0] === '[') {
        let result = [];
        let c = [result];
        [...string.matchAll(/(,|\[|\]|\d+)/g)].map(m => m[0]).forEach(token => {
            if(token.match(/^\d+$/)) {
                c[c.length-1].push(parseInt(token));
            } else if(token === '[') {
                let a = [];
                c[c.length-1].push(a);
                c.push(a)
            } else if(token === ']') {
                c.pop();
            } else if(token === ',') {
            } else {
                throw `Unexpexted token ${token}`;
            }
        });
        return result[0];
    } else if(string.match(/^\d*$/)) {
        return parseInt(string);
    } else {
        throw `Unexpected token ${string}`;
    }
}

let data = (await fs.readFile('./input13.txt', 'utf8'))
// let data = (await fs.readFile('./test13.txt', 'utf8'))
    .split('\n\n')
    .map(item => item
        .split('\n')
        .map(s => parse(s))
    );

const compare = (left,right) => {
    if(!Array.isArray(left) && !Array.isArray(right)) {
        let val = Math.sign(right - left);
        //console.log('-',left,' ---',right, ' === ', val);
        return val;
    }
    if(!Array.isArray(left)) left = [left];
    if(!Array.isArray(right)) right = [right];

    for(let i = 0; i < Math.min(left.length, right.length); i++) {
        let r = compare(left[i], right[i]);
        if(r !== 0) {
            //console.log('-',left,' ---',right, ' === ', r, 'ITT');
            return r;
        }
    }

    if(left.length !== right.length) {
        let val = Math.sign(right.length - left.length);
        //console.log('-',left,' ---',right, ' === ', val, 'VAGY ITT');
        return val;
    }

    return 0;
}

console.log(data.map((c,i) => compare(...c) > 0 ? i+1 : 0).reduce((s, i) => s+i, 0));

data = data.flat();
let a = [[2]];
let b = [[6]];
data.push(a);
data.push(b);
data.sort((l,r) => compare(r,l));

console.log((data.findIndex(i => i === a) + 1)*(data.findIndex(i => i === b) + 1));