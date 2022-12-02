import { promises as fs } from 'fs';

import {GPU} from "gpu.js";

const gpu = new GPU();


// let rawData = await fs.readFile('./input19.txt', 'utf8');
let rawData = await fs.readFile('./test19.txt', 'utf8');

rawData = rawData.split('\n');

let sensors = [];

for(let i = 0; i < rawData.length; i++) {
    if(rawData[i].slice(0,3) === '---') {
        sensors.push([]);
    } else if(rawData[i] === '') {
    } else {
        sensors[sensors.length - 1].push(rawData[i].split(',').map(d => parseInt(d)));
    }
}

console.log(sensors.length);

let maxBeacons = Math.max(...sensors.map(s => s.length));

for(let i = 0; i < sensors.length; i++) {
    while(sensors[i].length < maxBeacons) {
        sensors[i].push([0,0,0]);
    }
}


let beaconDistancePairs = gpu.createKernel(function(sensors) {
    let sensorId = this.thread.z;
    let s1 = this.thread.y;
    let s2 = this.thread.x;
    let distance = 0;
    for(let i = 0; i < 3; i++) {
        distance += Math.pow(sensors[sensorId][s1][i] - sensors[sensorId][s2][i],2);
    }
    return distance;
}).setOutput([sensors[0].length, sensors[0].length, sensors.length]);

let distances = beaconDistancePairs(sensors).map(s => s.map(b => Array.from(b).sort((a,b) => b-a)));
// console.log(distances);

let sensorPairMatches = gpu.createKernel(function(l, r, limit) {
    let i = 0;
    let j = 0;
    let matches = 0;
    while(i < limit && j < limit && l[this.thread.x][i] !== 0 && r[this.thread.y][j]!== 0) {
        if(l[this.thread.x][i] === r[this.thread.y][j]) {
            matches++;
            j++;
            i++;
        } else if (l[this.thread.x][i] > r[this.thread.y][j]) {
            i++
        } else {
            j++;
        }
    }
    return matches;
}).setOutput([sensors[0].length, sensors[0].length]);


let connections = {};
let matchesBySensorPair = Array(sensors.length).fill(0).map(() => Array(sensors.length).fill(0).map(() => []));
for(let s1 = 0; s1 < sensors.length; s1++) {
    for(let s2 = s1 + 1; s2 < sensors.length; s2++) {
        let pairMatches = sensorPairMatches(distances[s1], distances[s2], maxBeacons);
        for(let i = 0; i < pairMatches.length; i++) {
            for(let j = 0; j < pairMatches.length; j++) {
                if(pairMatches[i][j] > 10) {
                    connections[`${s1}_${i}`] = connections[`${s1}_${i}`] || []
                    connections[`${s1}_${i}`].push(`${s2}_${j}`);
                    connections[`${s2}_${j}`] = connections[`${s2}_${j}`] || []
                    connections[`${s2}_${j}`].push(`${s1}_${i}`);
                    matchesBySensorPair[s1][s2].push([i,j,sensors[s1][i],sensors[s2][j]])
                    matchesBySensorPair[s2][s1].push([i,j,sensors[s2][j],sensors[s1][i]])
                }
            }
        }
    }
}

// console.log(distances[0]);

console.log(matchesBySensorPair[0]);

let [m1, m2] = [0,1]
for(let i = 0; i < 3; i++) {
    console.log(matchesBySensorPair[0][1][m1][2][i] - matchesBySensorPair[0][1][m2][2][i]);
}
for(let i = 0; i < 3; i++) {
    console.log(matchesBySensorPair[0][1][m1][3][i] - matchesBySensorPair[0][1][m2][3][i]);
}

// let visited = {};
// let count = 0;
// const visit = (node) => {
//     if(visited[node]) return [];
//     visited[node] = true;
//     if(connections[node]) {
//         return [node,...connections[node].flatMap(n => visit(n))];
//     }
//     return [node];
// }
//
// let groups = [];
// for(let s = 0; s < sensors.length; s++) {
//     for(let b = 0; b < sensors[s].length; b++) {
//         if(sensors[s][b].reduce((s,v) => s + Math.abs(v)) > 0 && !visited[`${s}_${b}`]) {
//             count++;
//             groups.push(visit(`${s}_${b}`).map(g => g.split('_').map(d => parseInt(d))));
//         }
//     }
// }
// // console.log(groups);
// console.log(count);
//
// let matchesBySensorPair = Array(sensors.length).fill(0).map(() => Array(sensors.length).fill(0).map(() => []));
// groups.forEach(group =>
//     group.forEach(n1 =>
//         group.forEach(n2 => {
//             matchesBySensorPair[n1[0]][n2[0]].push([n1[1],n2[1]])
//         })
//     )
// );
//
// console.log(matchesBySensorPair[0][0]);

// 317 too low