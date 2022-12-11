import { promises as fs } from 'fs';

let data = (await fs.readFile('./input11.txt', 'utf8'))
    // let data = (await fs.readFile('./test11.txt', 'utf8'))
    .split('\n\n')
    .map(m => {
        const re = /Monkey (?<index>\d+):\n  Starting items: (?<items>[\d, ]+)\n  Operation: (?<operation>[^\n]+)\n  Test: divisible by (?<divisor>\d+)\n    If true: throw to monkey (?<iftrue>\d+)\n    If false: throw to monkey (?<iffalse>\d+)/mg;
        const p = re.exec(m);
        return {
            items: p.groups.items.split(',').map(d => parseInt(d)),
            operation: old => {
                let vnew;
                eval(`v${p.groups.operation}`);
                return vnew;
            },
            divisor: parseInt(p.groups.divisor),
            iftrue: parseInt(p.groups.iftrue),
            iffalse: parseInt(p.groups.iffalse),
            monkeyBusiness: 0
        }
    });


let smallestCommonDenominator = data.map(d => d.divisor).reduce((p, d) => p * d);

for(let i = 0; i < 10000; i++) {
    for(let j = 0; j < data.length; j++) {
        while(data[j].items.length > 0) {
            const item = data[j].items.shift();
            const newValue = data[j].operation(item) % smallestCommonDenominator;
            const target = (newValue % data[j].divisor === 0) ? data[j].iftrue : data[j].iffalse;
            data[target].items.push(newValue);
            data[j].monkeyBusiness++;
        }
    }
}

const monkeyBusinesses = (data.map(d => d.monkeyBusiness).sort((l,r) => r - l));

console.log(monkeyBusinesses[0] * monkeyBusinesses[1]);
