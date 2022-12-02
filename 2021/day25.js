import { promises as fs } from 'fs';

import {GPU} from "gpu.js";
const gpu = new GPU();

let rawData = await fs.readFile('./input25.txt', 'utf8');
// let rawData = await fs.readFile('./test25_1.txt', 'utf8');
// let rawData = await fs.readFile('./test25_2.txt', 'utf8');

const mapping = {
    '.': 0,
    '>': 1,
    'v': 2
}

const reverseMapping = ['.','>','v'];

const printBoard = board => console.log('\n' + board.map(l => l.map(c => reverseMapping[c]).join('')).join('\n'));

let board = rawData.split('\n').map(l => l.split('').map(c => mapping[c]));

printBoard(board);

const moveRightKernel = gpu.createKernel(function(board,sizeX, sizeY) {
    if(board[this.thread.y][this.thread.x] === 0) {
        const moveFromX = (this.thread.x + sizeX - 1) % sizeX;
        return board[this.thread.y][moveFromX] === 1 ? 1 : 0;
    }
    if(board[this.thread.y][this.thread.x] === 1) {
        const moveToX = (this.thread.x + 1) % sizeX;
        return board[this.thread.y][moveToX] === 0 ? 0 : 1;
    }
    if(board[this.thread.y][this.thread.x] === 2) return 2;
}).setOutput([board[0].length, board.length]);

const moveRight = (board) => {
    return moveRightKernel(board, board[0].length, board.length).map(l => [...l]);
}

const moveDownKernel = gpu.createKernel(function(board,sizeX, sizeY) {
    if(board[this.thread.y][this.thread.x] === 0) {
        const moveFromY = (this.thread.y + sizeY - 1) % sizeY;
        return board[moveFromY][this.thread.x] === 2 ? 2 : 0;
    }
    if(board[this.thread.y][this.thread.x] === 1) return 1
    if(board[this.thread.y][this.thread.x] === 2) {
        const moveToY = (this.thread.y + 1) % sizeY;
        return board[moveToY][this.thread.x] === 0 ? 0 : 2;
    }
}).setOutput([board[0].length, board.length]);

const moveDown = (board) => {
    return moveDownKernel(board, board[0].length, board.length).map(l => [...l]);
}

const equalLines = gpu.createKernel(function(l,r,sizeX) {
    const y = this.thread.x;
    let result = 0;
    for(let x = 0; x < sizeX; x++) {
        result += l[y][x] !== r[y][x] ? 1 : 0;
    }
    return result;
}).setOutput([board.length]);

const equalBoards = (l, r) => {
    return equalLines(l, r, l[0].length).reduce((sum, v) => sum + v) === 0;
}

let i = 0;
let previousBoard = board.map(l => l.map(c => 0));
while(!equalBoards(board,previousBoard)) {


    previousBoard = board;
    board = moveDown(moveRight(previousBoard));
    i++;
}

printBoard(board);
console.log(i);