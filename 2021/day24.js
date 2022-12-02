import {promises as fs} from 'fs';

import {GPU} from "gpu.js";

const gpu = new GPU();

let rawData = await fs.readFile('./input24.txt', 'utf8');
// let rawData = await fs.readFile('./test24.txt', 'utf8');

let instructions = rawData.split('\n').map(l => l.split(' '));

const varNames = 'wxyz'.split('');

let inputIndex = 0;
let codeInstructions = instructions.map(instruction => {
   const a = `vars[${instruction[1].charCodeAt(0)-119}]`;
   const btmp = instruction[2] ? instruction[2] : 0;
   const b = varNames.includes(btmp) ? `vars[${instruction[2].charCodeAt(0)-119}]` : parseInt(btmp);

   switch (instruction[0]) {
      case 'inp':
         return `${a} = input[${inputIndex++}];`;
      case 'add':
         return `${a} += ${b};`;
      case 'mul':
         return `${a} *= ${b};`;
      case 'div':
         return `${a} = Math.trunc(${a}/${b});`;
      case 'mod':
         return `${a} = ${a} % ${b}`;
      case 'eql':
         return `${a} = (${a} === ${b} ? 1 : 0);`;
   }

   return '';
});

// console.log(codeInstructions);

let code = '\tlet vars = Array(4).fill(0);\n' +
    codeInstructions.map(l => '\t' +l).join('\n') +
    '\n\treturn vars;\n';

console.log(code);

const aluFunc = Function("input", code);
const val = 13579246899999;
const result = aluFunc(val.toString().split('').map(d => parseInt(d)));
console.log(result);

// for(let i = 1000; i < 9999; i++) {
//    let val = 11111111110000 + i;
//    let input = val.toString().split('').map(d => parseInt(d));
//    console.log(i, aluFunc(input));
// }


// for(let i = 99999999999999; i > 99998999999999; i--) {
//    if(i % 1000 === 0) console.log(i);
//    if(i.toString(10).split('').includes('0')) continue;
//    const result = aluFunc(i.toString().split('').map(d => parseInt(d)))
//    if(result[3] === 0) {
//       console.log(i, result);
//       break;
//    }
// }

/*

let possibleValues = {'0,0,0,0': ''};
codeInstructions.forEach((instruction,instructionIndex) => {
   console.log(instructionIndex, instruction, Object.keys(possibleValues).length);
   let nextPossibleValues = {}
   Object.entries(possibleValues).forEach(([varsRaw, inputRaw]) => {
      let vars = varsRaw.split(',').map(d => parseInt(d));
      let originalInput = inputRaw.split('').map(d => parseInt(d));
      if(instructions[instructionIndex][0] === 'inp') {
         for(let j = 1; j < 10; j++) {
            let input = [...originalInput, j];

            eval(instruction);
            let current = nextPossibleValues[vars.join(',')];
            if(current === undefined || parseInt(current) < input) {
               if(Math.abs(vars[3]) < 350) {
                  nextPossibleValues[vars.join(',')] = input.join('');
               }
            }
         }
      } else {
         let input = originalInput;
         eval(instruction);
         if(Math.abs(vars[3]) < 1000) {
            nextPossibleValues[vars.join(',')] = input.join('');
         }
      }
   });
   possibleValues = nextPossibleValues;
});

// console.log(possibleValues);
console.log(Object.keys(possibleValues).length);

let maxValid = Object.entries(possibleValues).reduce((maxValue, [vars,input]) =>
    vars.split(',')[3] === '0' ? Math.max(parseInt(input), maxValue) : maxValue);

console.log(maxValid);
*/


const coefs = [
   [1,14,16],
   [1,11,3],
   [1,12,2],
   [1,11,7],
   [26,-10,13],
   [1,15,6],
   [26,-14,10],
   [1,10,11],
   [26,-4,6],
   [26,-3,5],
   [1,13,11],
   [26,-3,4],
   [26,-9,4],
   [26,-12,6]
];

const step = (input,c0,c1,c2,vars) => {
   vars = Math.trunc(vars/c0);
   const t2 = (vars % 26 + c1) !== input ? 1 : 0; // [0...1]
   vars *= 25 * t2 + 1; // vars * [1, 26]
   vars += (input + c2) * t2; // [1...9] + [0...13] * [0,1]
   return vars
}


const refactor = (input) => {
   return coefs.reduce((v,l,i) => step(input[i], ...l, v), 0);
}

const refactor_again = (input) => {
   let vars = Array(4).fill(0);
   let [w,x,y,z] = [0,0,0,0];


   return 0;

}

/*
const testInput = '99745723659856'.split('').map(d => parseInt(d));
console.log(testInput, refactor(testInput));

let memo = {}
function backtrack(iter, input, vars) {
   if(!!memo[`${iter}_${vars}`]) {
      // console.log('memo used');
      return null;
   }
   memo[`${iter}_${vars}`] = true;
   if(iter === 6) {
      console.log(iter, input, vars, Object.keys(memo).length);
   }
   // if(iter > 7 && Math.abs(vars) > Math.pow(50,14-iter)) {
   //    return null;
   // }
   if(iter === 14) {
      return vars === 0 ? input : null;
   }
   for(let j = 9; j > 0; j--) {
      // if(j !== testInput[iter]) continue;
      const result = backtrack(iter + 1, 10*input + j, step(j, ...coefs[iter], vars));
      if(result !== null) { return result; }
   }
   return null;
}

console.log(backtrack(0, 0, 0));
*/

function getRandomInt(min, max) {
   min = Math.ceil(min);
   max = Math.floor(max);
   return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
}

let failCount = 0;
for(let i = 0; i <1; i++) {
   // let input = '0';
   // while(input.includes('0')) {
   //    input = getRandomInt(Math.pow(10,13), Math.pow(10,14)).toString().split('').map(d => parseInt(d));
   // }
   let input = [];
   let i0 = getRandomInt(1,6);
   input.push(i0);
   let i1 = getRandomInt(7,10);
   input.push(i1);
   let i2 = getRandomInt(2,10);
   input.push(i2);
   let i3 = getRandomInt(4,10);
   input.push(i3);
   input.push((i3-3));
   input.push(9);
   input.push(1);
   let i7 = getRandomInt(1,3);
   input.push(i7);
   input.push((i7+7));
   input.push(i2-1);
   input.push(1);
   input.push(9);
   input.push(i1-6);
   input.push(i0+4);


   if(aluFunc(input)[3] !== refactor_again(input))
   {
      console.log('FALED', input.join(''), aluFunc(input)[3], refactor_again(input));
      failCount++;
   } else {
      console.log('PASSED', input.join(''), refactor_again(input));
   }
}

console.log('FAILS: ', failCount);
