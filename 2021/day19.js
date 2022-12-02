import {promises as fs} from 'fs';

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

let maxBeacons = Math.max(...sensors.map(s => s.length));

const beaconCounts = sensors.map(s => s.length);

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

let sensorPairMatches = gpu.createKernel(function(l, r, limit) {
    let i = 0;
    let j = 0;
    let matches = 0;
    while(i < limit && j < limit && l[this.thread.y][i] !== 0 && r[this.thread.x][j]!== 0) {
        if(l[this.thread.y][i] === r[this.thread.x][j]) {
            matches++;
            j++;
            i++;
        } else if (l[this.thread.y][i] > r[this.thread.x][j]) {
            i++
        } else {
            j++;
        }
    }
    return matches;
}).setOutput([sensors[0].length, sensors[0].length]);

const vectorMinus = (a,b) => {
    return a.map((av,i) => av - b[i]);
}

const findRotation = (l,r) => {
    for(let i = 0; i < 2; i++) {
        for (let j = i + 1; j < 3; j++) {
            if (l[i] === l[j]) {
                throw 'SUBMARINE ERROR: Identical distances detected, need to be smarter';
            }
        }
    }

    let nonZero = 0;
    let matrix = Array(3).fill(0).map(l => Array(3).fill(0))
        .map((_, i) => l.map((v, j) => {
            if(Math.abs(l[i]) === Math.abs(r[j])) {
                nonZero++;
                return l[i]/r[j];
            } else {
                return 0;
            }
        }));

    if(nonZero !== 3) throw 'SUBMARINE ERROR: Rotation detection failed';
    return matrix;
}

const rotateBeacons = (matrix, beacons) => {

    const rotateKernel = gpu.createKernel(function (matrix, beacons) {
        return beacons[this.thread.y][0] * matrix[this.thread.x][0] +
            beacons[this.thread.y][1] * matrix[this.thread.x][1] +
            beacons[this.thread.y][2] * matrix[this.thread.x][2];
    }).setOutput([3,beacons.length]);

    return rotateKernel(matrix,beacons).map(l => [...l])
}

const shiftBeacons = (vector, beacons) => {
    const shiftKernel = gpu.createKernel(function (vector, beacons) {
        return beacons[this.thread.y][this.thread.x] + vector[this.thread.x];
    }).setOutput([3,beacons.length]);
    return shiftKernel(vector, beacons).map(l => [...l]);
}

const rebase = (s2) => ({
    to: (s1) => {

        const pairMatches = sensorPairMatches(distances[s1], distances[s2], maxBeacons).map(l => [...l]);

        const matchCandiadates = pairMatches
            .flatMap((l, i) =>
                l.map((v,j) => ([i,j,v]))
            )
            .filter(item => item[2] > 10)
            .map(l => l.slice(0,2));

        const beacons1 = sensors[s1].slice(0, beaconCounts[s1]);
        const beacons2 = sensors[s2].slice(0, beaconCounts[s2]);

        if(matchCandiadates.length === 0) {
            return null;
        }

        const [v1, v2] = [
            vectorMinus(beacons1[matchCandiadates[0][0]], beacons1[matchCandiadates[1][0]]),
            vectorMinus(beacons2[matchCandiadates[0][1]], beacons2[matchCandiadates[1][1]])]

        const rotationMatrix = findRotation(v1, v2);
        const rotatedBeacons = rotateBeacons(rotationMatrix, beacons2);
        const shiftVector = vectorMinus(beacons1[matchCandiadates[0][0]], rotatedBeacons[matchCandiadates[0][1]]);

        return beacons => {
            return shiftBeacons(shiftVector, rotateBeacons(rotationMatrix, beacons));
        }
    }
})

let toBeProcessed = [0];
let found = { 0: { sensorId: 0, from: null, transform: item => item, sensorPosition: [0,0,0] } }

while(toBeProcessed.length > 0) {
    let s1 = toBeProcessed.pop();
    sensors.forEach((beacons, s2) => {
        if(found[s2]) return;

        const transform = rebase(s2).to(s1);
        if(!transform) return;

        found[s2] = { sensorId: s2, from: s1, transform: item => found[s1].transform(transform(item)) };
        toBeProcessed.push(s2);
    });
}

let allBeacons = {}
Object.values(found).forEach(({sensorId, transform}) => {
    const tranformedBeacons = transform(sensors[sensorId].slice(0, beaconCounts[sensorId]));
    tranformedBeacons.forEach((beacon, beaconId) => {
        allBeacons[beacon.join(',')] = allBeacons[beacon.join(',')] || [];
        allBeacons[beacon.join(',')].push({sensorId, beaconId})
    });
});
console.log("Part 1:",Object.keys(allBeacons).length);

let allSensors = Object.values(found).map(({transform}) => transform([[0, 0, 0]])[0]);

const calculateManhattanDistances = (points) => {
    const manhattanKernel = gpu.createKernel(function (points) {
        return Math.abs(points[this.thread.x][0] - points[this.thread.y][0]) +
            Math.abs(points[this.thread.x][1] - points[this.thread.y][1]) +
            Math.abs(points[this.thread.x][2] - points[this.thread.y][2]);
    }).setOutput([points.length, points.length])

    return manhattanKernel(points).map(l => [...l]);
}
const sensorDistances = calculateManhattanDistances(allSensors);

console.log("Part 2:", Math.max(...sensorDistances.flat()));




