
import {GPU} from "gpu.js";

const gpu = new GPU();

// target area: x=20..30, y=-10..-5
// const targetArea = [[20,30], [-10,-5]];
// target area: x=248..285, y=-85..-56
const targetArea = [[248,285], [-85,-56]];

let initialXVelocity = [0, targetArea[0][1]+1];
let initialYVelocity = [targetArea[1][0], targetArea[1][1]+targetArea[0][1]+1];

console.log("Range scanned:", initialXVelocity, initialYVelocity);

let findHighPoints = gpu.createKernel(function(targetArea, miny) {
    let vy = this.thread.y + miny;
    let vx = this.thread.x;
    let x = 0;
    let y = 0;
    let maxy = 0;

    while(x < targetArea[0][1] && y > targetArea[1][0]) {
        x += vx;
        y += vy;
        if(vx > 0) { vx--; } else if(vx < 0) { vx++; }
        vy--;
        maxy = Math.max(y, maxy);

        if(x >= targetArea[0][0]
            && x <= targetArea[0][1]
            && y >= targetArea[1][0]
            && y <= targetArea[1][1]) {
            return maxy;
        }
    }
    return -1;
}).setOutput([
    initialYVelocity[1]-initialYVelocity[0],
    initialXVelocity[1]]
)

let highPoints = findHighPoints(targetArea, initialYVelocity[0])
    .map(l => Array.from(l))
    .flat();

console.log("Highest shoot:", Math.max(...highPoints));

console.log("Number of options hitting the target: ",
    highPoints.map(d => d < 0 ? 0 : 1).reduce((s,v) => s+v, 0));