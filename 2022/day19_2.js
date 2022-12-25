import { promises as fs } from 'fs';

const re = /Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian./;

let blueprints = (await fs.readFile('./input19.txt', 'utf8'))
// let blueprints = (await fs.readFile('./test19.txt', 'utf8'))
    .split('\n')
    .slice(0, 3)
    .map(l => re.exec(l))
    .map(l => l.map(d => parseInt(d)))
    .map(l => {
        return [
            [l[2],    0,    0],
            [l[3],    0,    0],
            [l[4], l[5],    0],
            [l[6],    0, l[7]]
        ]
    });

console.log(blueprints);

const produce = (previous, robotId, costs) => {
    let next = [...previous];
    if(robotId !== undefined) {
        next[robotId]++;
        for (let i = 0; i < costs.length; i++) {
            next[4 + i] -= costs[i]
        }
    }
    for(let i = 0; i < 4; i++) {
        next[4+i] += previous[i];
    }
    return next;
}
const enoughResources = (resources, costs) => {
    for(let i = 0; i < costs.length; i++) {
        if(resources[4+i] < costs[i]) {
            return false;
        }
    }
    return true;
}

const toKey = (status) => status.join('_');

const isRobotUseful = (maxConsumed, robots, resources, maxTime) => {
    for(let t = 0; t < maxTime; t++) {
        if(maxConsumed * t > resources + robots * t) {
            return true;
        }
    }
    return false;
}

const calculateForBluePrint = (blueprint, i) => {
    let outcomes = {
        "1_0_0_0_0_0_0_0": [1, 0, 0, 0, 0, 0, 0, 0]
    };
    const maxConsumed = Array(3).fill(0).map((_,i) => Math.max(...blueprint.map(b=> b[i])));
    console.log(maxConsumed);

    let maxGeode = 0;

    let maxTime = 32;
    for (let time = 0; time < maxTime; time++) {
        let nextOutcomes = {};
        let largestMinimumPotential = 0;

        Object.values(outcomes).forEach(previous => {


            // Produce a robot
            // Always prefer geode robot when possible to create
            if(enoughResources(previous, blueprint[3])) {
                let next = produce(previous, 3, blueprint[3]);
                maxGeode = Math.max(next[7], maxGeode);
                largestMinimumPotential = Math.max(largestMinimumPotential, next[7] + next[3] * (maxTime - time))
                nextOutcomes[toKey(next)] = next;
            } else {
                for(let i = 0; i < 3; i++) {
                    const useful = isRobotUseful(maxConsumed[i], previous[i], previous[i+4], maxTime - time);
                    if(enoughResources(previous, blueprint[i]) && useful){
                        let next = produce(previous, i, blueprint[i]);
                        maxGeode = Math.max(next[7], maxGeode);
                        largestMinimumPotential = Math.max(largestMinimumPotential, next[7] + next[3] * (maxTime - time))
                        nextOutcomes[toKey(next)] = next;
                    }
                }

                // No robot produced
                let next = produce(previous);
                maxGeode = Math.max(next[7], maxGeode);
                largestMinimumPotential = Math.max(largestMinimumPotential, next[7] + next[3] * (maxTime - time));
                nextOutcomes[toKey(next)] = next;
            }

        });
        outcomes = Object.values(nextOutcomes).filter(o =>
            o[7] + o[3] * (maxTime - time) + (maxTime - time) * (maxTime - time - 1) / 2 >= largestMinimumPotential
        ).reduce((os, o) => {
            os[toKey(o)] = o;
            return os;
        }, {});

        console.log("Blueprint:", (i+1), "Time:", time, "Fanout:", Object.keys(outcomes).length, "Max produced:", maxGeode);
    }
    return maxGeode;
}

let maximums = blueprints.map((blueprint, i)  => calculateForBluePrint(blueprint, i));
console.log("Maximums:", maximums);

console.log("Result:", maximums.reduce((r, v, i) => r * v));