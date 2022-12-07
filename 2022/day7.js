import { promises as fs } from 'fs';

let data = (await fs.readFile('./input7.txt', 'utf8')).split('\n');
// let data = (await fs.readFile('./test7.txt', 'utf8')).split('\n');
data.pop();

let root = { parent: null, subdirs: {}, files: {}};
let current = root;
data.forEach(l => {
    if(l === '$ cd /') {
        current = root;
    } else if(l === '$ cd ..') {
        current = current.parent;
    } else if(l.slice(0,5) === '$ cd ') {
        current = current.subdirs[l.slice(5)];
    } else if (l[0] !== '$') {
        let [size, name] = l.split(' ');
        if(size === 'dir') {
            if(!current.subdirs[name]) {
                current.subdirs[name] = { parent: current, subdirs: {}, files: {} };
            }
        } else {
            current.files[name] = { size: parseInt(size)};
        }
    }

});

const fillSizes = (dir) => {
    let mySize = 0;
    Object.entries(dir.subdirs).forEach(([name, d]) => {
        mySize += fillSizes(d);
    });
    Object.entries(dir.files).forEach(([name, f]) => {
        mySize += f.size;
    });
    dir.size = mySize;
    return mySize;
}

const printTree = (dir, depth) => {
    Object.entries(dir.subdirs).forEach(([name, d]) => {
        console.log(' '.repeat(depth) + name + " (" + d.size + ")");
        printTree(d, depth + 1);
    });
    Object.entries(dir.files).forEach(([name, f]) => {
        console.log(' '.repeat(depth) + name + " (" + f.size + ")");
    });
}

fillSizes(root);
printTree(root, 1);

const sumSmallDirs = (dir) => {
    let sum = 0;
    Object.entries(dir.subdirs).forEach(([name, d]) => {
        sum += sumSmallDirs(d);
        if(d.size < 100000) {
            sum += d.size;
        }
    });
    return sum;
};

console.log('\nRESULT 1: ' + sumSmallDirs(root) + '\n');

let necessarySpace = 30000000 - (70000000 - root.size);

console.log(necessarySpace);

let candidateDirs = [];
const findCandidateDirs = (dir) => {
    Object.entries(dir.subdirs).forEach(([name, d]) => {
        findCandidateDirs(d);
        if(d.size >= necessarySpace) {
            candidateDirs.push(d);
        }
    });
};
findCandidateDirs(root);


let smallestCandidate = candidateDirs[0];
console.log(smallestCandidate.size);
candidateDirs.forEach(d => {
    console.log(" - ", d.size, smallestCandidate.size);
    if(d.size < smallestCandidate.size) {
        smallestCandidate = d;
    }
});

console.log('\nRESULT 2: ' + smallestCandidate.size);