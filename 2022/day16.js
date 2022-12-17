import { promises as fs } from 'fs';

// let data = (await fs.readFile('./input16.txt', 'utf8'))
let data = (await fs.readFile('./test16.txt', 'utf8'))
    .split('\n')
    .map(l => /Valve (?<name>\w+) has flow rate=(?<rate>\d+); tunnel(s)? lead(s)? to valve(s)? (?<tunnels>.*)/.exec(l))
    .map(l => ({ name: l.groups.name, rate: parseInt(l.groups.rate), tunnels: l.groups.tunnels.split(', ') }))
    .reduce((s, v) => {
        s[v.name] = {rate: v.rate, tunnels: v.tunnels};
        return s;
    }, {});

const nodes = Object.keys(data);
Object.keys(data).forEach(k => {
    data[k].distances = nodes.reduce((s, v) => {
        s[v] = -1;
        return s;
    }, {});
    data[k].tunnels.forEach(t => {
        data[k].distances[t] = 1;
    })
});

let ready = false;
while(!ready) {
    ready = true;
    nodes.forEach(i => {
        nodes.forEach(j => {
            if (data[i].distances[j] === -1) {
                ready = false;
                const candidates = data[i].tunnels.map(k => data[k].distances[j]).filter(d => d >= 0);
                if(candidates.length > 0) {
                    data[i].distances[j] = Math.min(...candidates) + 1
                }
            }
        })
    });
}

console.log(JSON.stringify(data));

let totalRemainingRate = Object.values(data).map(v => v.rate).reduce((s,v) => s + v, 0);
let closedVales = Object.entries(data)
    .filter(v => v[1].rate > 0)
    .map(([k,v]) => ({name:k, rate:v.rate}))
    .sort((l,r) => r.rate - l.rate)

// console.log(totalRemainingRate);
// console.log(closedVales);

const multiPerson = (closedValves, currentValves, busyFor, flowSoFar, totalRemainingTime, totalRemainingRate) => {
    let freePerson = busyFor.findIndex(v => v === 0)
    if(freePerson !== -1) {
        let maxFlow = flowSoFar;
        const cutoff = flowSoFar + totalRemainingRate * totalRemainingTime;
        for(let i = 0; i < closedValves.length; i++) {
            if(maxFlow > cutoff) {
                break;
            }
            const name = closedValves[i].name;

            let nextValves = [...currentValves];
            nextValves[freePerson] = name;

            let nextBusyFor = [...busyFor];
            nextBusyFor[freePerson] = data[currentValves[freePerson]].distances[name] + 1;

            const timeLeftAfterReaching = totalRemainingTime - nextBusyFor[freePerson];
            let flow = flowSoFar + data[name].rate * timeLeftAfterReaching;

            let subFlow = multiPerson(
                [...closedValves.slice(0,i), ...closedValves.slice(i+1)],
                nextValves,
                nextBusyFor,
                flow,
                totalRemainingTime,
                totalRemainingRate - data[currentValves[freePerson]].rate
            );
            maxFlow = Math.max(maxFlow, subFlow);
        }
        return maxFlow;
    } else {
        const skip = Math.min(...busyFor);
        return multiPerson(closedValves, currentValves, busyFor.map(v => v-skip), flowSoFar, totalRemainingTime - skip, totalRemainingRate);
    }

}

console.log(multiPerson(closedVales, ['AA'], [0], 0, 30, totalRemainingRate));
//console.log(multiPerson(closedVales, ['AA','AA'], [0,0], 0, 26, totalRemainingRate));