import {Heap} from 'heap-js';

let startingPositions = '...........ADDBCCBABBADDACC'.split('');

const printPositions = (positions) => {
    console.log(
        '#############' +
        '\n#' + positions.slice(0,11).join('') + '#\n' +
        '###' + positions[11] + '#' + positions[15] + '#' + positions[19] + '#' + positions[23] + '###\n' +
        '  #' + positions[12] + '#' + positions[16] + '#' + positions[20] + '#' + positions[24] + '#\n' +
        '  #' + positions[13] + '#' + positions[17] + '#' + positions[21] + '#' + positions[25] + '#\n' +
        '  #' + positions[14] + '#' + positions[18] + '#' + positions[22] + '#' + positions[26] + '#\n' +
        '  #########  '
    );
}

const costOf = (name) =>
    Math.pow(10,name.charCodeAt(0) - 65);


const allIsHomeIn = (positions, roomId) => {
    const roomOwner = String.fromCharCode(65+roomId);
    for(let i = 0; i < 4; i++){
        if(!['.',roomOwner].includes(positions[11+4*roomId+i])) {
            return false;
        }
    }
    return true;
}

const nextValidPositions = (positions) => {
    let nextPositions = [];
    // move out of a room
    for(let i = 0; i < 4; i++) {

        // Skip if in the right place
        if(allIsHomeIn(positions,i)) {
            continue;
        }


        let cost = 0;
        let firstStep = [...positions];
        // take one step out if only rear is occupied
        if(firstStep[11+4*i] === '.') {
            for(let j = 1; j < 4; j++) {
                if(['A','B','C','D'].includes(firstStep[11+4*i + j])) {
                    cost += j*costOf(firstStep[11+4*i + j]);
                    firstStep[11+4*i] = firstStep[11+4*i + j];
                    firstStep[11+4*i + j] = '.';
                    break;
                }
            }
        }


        if(['A','B','C','D'].includes(firstStep[11+4*i]) && firstStep[2+2*i] === '.') {
            // look left
            for(let j = 1+2*i; j >= 0 && firstStep[j] === '.'; j--) {
                if([2,4,6,8].includes(j)) continue;
                let newPositions = [...firstStep];
                newPositions[j] = newPositions[11+4*i];
                newPositions[11+4*i] = '.';
                nextPositions.push({ cost: cost + costOf(newPositions[j]) * (2+2*i - j + 1), positions: newPositions});
            }
            // look right
            for(let j = 3+2*i; j < 11 && firstStep[j] === '.'; j++) {
                if([2,4,6,8].includes(j)) continue;
                let newPositions = [...firstStep];
                newPositions[j] = newPositions[11+4*i];
                newPositions[11+4*i] = '.';
                nextPositions.push({ cost: cost + costOf(newPositions[j]) * (j - (2+2*i) + 1), positions: newPositions});
            }
        }
    }

    const canMoveHome = j => {
        let roomId = positions[j].charCodeAt(0) - 65;
        if(allIsHomeIn(positions,roomId))  {// positions[11+2*roomId] === '.' && ['.',positions[j]].includes(positions[11+2*roomId + 1])) {
            let from = Math.min(2+2*roomId, j+1);
            let to = Math.max(2+2*roomId, j-1);
            for(let i = from; i <= to; i++) {
                if(positions[i] !== '.') return false;
            }
            return true;
        }
        return false;
    }

    // move into room
    for(let i = 0; i < 11; i++) {
        if(['A','B','C','D'].includes(positions[i]) && canMoveHome(i)) {
            let roomId = positions[i].charCodeAt(0) - 65;
            let cost = Math.abs(2+2*roomId - i) + 1;
            let newPositions = [...positions];
            for(let j = 3; j >= 0; j--) {
                if(positions[11+4*roomId + j] === '.') {
                    newPositions[11+4*roomId + j] = positions[i];
                    cost += j;
                    break;
                }
            }
            newPositions[i] = '.';

            nextPositions.push({ cost: cost * costOf(positions[i]), positions: newPositions})
        }
    }
    return nextPositions;
}

// printPositions(posiotions);

// let next = nextValidPositions(nextValidPositions(nextValidPositions(posiotions)[0].positions)[0].positions);
//
//
// next.forEach((p) => {
//     console.log(p.cost);
//     printPositions(p.positions);
// });


let heap = new Heap((a,b) => a.cost - b.cost);
heap.push({ positions: startingPositions, cost: 0});
let reached = {};

let count = 0;
while(heap.peek() && heap.peek().positions.join('') !== '...........AAAABBBBCCCCDDDD' && count < 10000000) {

    let current = heap.pop();
    if(reached[current.positions.join('')]) {
        continue;
    }
    reached[current.positions.join('')] = { previous: current.previous, cost: current.cost, costChange: current.costChange };
    // console.log(count, current.cost);
    // printPositions(current.positions);

    nextValidPositions(current.positions).forEach(({positions, cost}) => {
        heap.push({positions, cost: cost + current.cost, costChange: cost, previous: current.positions });
    })

    if(count % 10000 === 0) {
        console.log(count, current.cost);
        printPositions(current.positions);
    }
    count++;
}

console.log('\n\n\n');

printPositions(heap.peek().positions);
let step = heap.peek();
console.log(step.cost, step.costChange);
console.log('');
printPositions(step.previous);

while(step = reached[step.previous.join('')]) {
    if(step.cost === 0) { break; }
    console.log(step.cost, step.costChange);
    console.log('');
    console.log(step.previous.join(''));
    printPositions(step.previous);
}


console.log('\n\n\n');
if(!heap.peek()) {
    console.log('No valid path found');
} else {
    console.log(count, heap.peek().cost);
}
//
// nextValidPositions('A..DD.........BCCBABBADDACC'.split('')).forEach(({positions, cost}) => {
//     console.log(cost);
//     printPositions(positions);
// })


// previous answers: 39836