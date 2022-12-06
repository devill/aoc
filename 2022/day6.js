import { promises as fs } from 'fs';

let data = (await fs.readFile('./input6.txt', 'utf8')).split('\n');
data.pop();

data.forEach(l => {
    for(let i = 3; i < l.length; i++) {
        if(
            l[i-3] !== l[i-2] && l[i-3] !== l[i-1] && l[i-3] !== l[i] &&
            l[i-2] !== l[i-1] && l[i-2] !== l[i] &&
            l[i-1] !== l[i]
        ) {
            console.log(l, i+1);
            break;
        }
    }
});

data.forEach(l => {
    for(let i = 14; i < l.length; i++) {
        let isMessage = true;
        let used = {};
        for(let j = -14; j < 0; j++) {
            if(used[l[i+j]]) {
                isMessage = false;
                break;
            } else {
                used[l[i+j]] = true;
            }
        }
        if(isMessage) {
            console.log(l, i);
            break;
        }
    }
});