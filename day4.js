import { GPU } from 'gpu.js'
import * as fs from 'fs';

const gpu = new GPU();

fs.readFile('./input4.txt', 'utf8', function (err, rawData) {
    if (err) {
        throw err;
    }
    let linesData = rawData.split('\n');
    let numbersCalled = linesData.shift().split(',').map(n => parseInt(n));

    let boards = [];
    while(linesData.length > 1) {
        linesData.shift();
        boards.push(linesData.splice(0,5).map(l => l.split(' ').filter(s  => s !== '').map(n => parseInt(n))))
    }

    let boardCount = boards.length;

    let findWins = gpu.createKernel(function(boards, numbersCalled, numbersCalledLength) {
        const lineId = this.thread.x;
        const boardId = this.thread.y;

        let rowHits = 0;
        let columnHits = 0;
        for(let i = 0; i < numbersCalledLength; i++){
            for(let j = 0; j < 5; j++) {
                if (boards[boardId][lineId][j] === numbersCalled[i]) {
                    rowHits++;
                }
                if(boards[boardId][j][lineId] === numbersCalled[i]) {
                    columnHits++;
                }
            }


            if(rowHits > 4 || columnHits > 4) {
                return [i, boardId, numbersCalled[i]]
            }
        }
        return [numbersCalledLength, boardId, -1]
    }).setOutput([5,boardCount]);

    const wins = findWins(boards, numbersCalled, numbersCalled.length);
    let firstWin = wins.flat().reduce((min, win) => min[0] < win[0] ? min : win, [numbersCalled.length, null, null]);
    let lastWin = wins
        .map(w => w.reduce((min, win) => min[0] < win[0] ? min : win, [numbersCalled.length, null, null]))
        .reduce((max, win) => max[0] > win[0] ? max : win, [0, null, null, null]);

    console.log('First win');

    let check = [...boards[firstWin[1]].map(l => [...l])];
    for(let n = 0; n < firstWin[0]+1; n++){
        for(let i = 0; i < 5; i++) {
            for(let j = 0; j < 5; j++) {
                if(check[i][j] === numbersCalled[n]) {
                    check[i][j] = 0;
                }
            }
        }
    }
    let sumOfUnused = check.flat().reduce((sum,n) => sum + n, 0);

    console.log(firstWin, sumOfUnused, firstWin[2]*sumOfUnused);

    console.log('Last win');

    check = [...boards[lastWin[1]].map(l => [...l])];
    for(let n = 0; n < lastWin[0]+1; n++){
        for(let i = 0; i < 5; i++) {
            for(let j = 0; j < 5; j++) {
                if(check[i][j] === numbersCalled[n]) {
                    check[i][j] = 0;
                }
            }
        }
    }

    sumOfUnused = check.flat().reduce((sum,n) => sum + n, 0);

    console.log(lastWin, sumOfUnused, lastWin[2]*sumOfUnused);
});