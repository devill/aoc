import { promises as fs } from 'fs';

let rawData = await fs.readFile('./input16.txt', 'utf8');

class Operator {
    constructor(lengthType, len, version, operatorType, tokens) {
        this.lengthType = lengthType;
        this.len = len;
        this.version = version;
        this.operatorType = operatorType;
        this.tokens = tokens;
    }

    getValue() {
        let values = this.tokens.map(t => t.getValue());
        switch (this.operatorType) {
            case 0:
                return values.reduce((s,t) => s+t, 0);
            case 1:
                return values.reduce((s,t) => s*t, 1);
            case 2:
                return Math.min(...values);
            case 3:
                return Math.max(...values);
            case 5:
                return values[0] > values[1] ? 1 : 0;
            case 6:
                return values[0] < values[1] ? 1 : 0;
            case 7:
                return values[0] === values[1] ? 1 : 0;
        }
        return 0;
    }

    getVersionSum() {
        return this.tokens.reduce((s,t) => s + t.getVersionSum(), this.version);
    }
}

class Literal {
    constructor(version, packetType, val) {
        this.version = version;
        this.packetType = packetType;
        this.val = val;
    }

    getValue() {
        return this.val;
    }

    getVersionSum() {
        return this.version;
    }
}

class Packet {
    constructor(packetData) {
        this.data = packetData
        this.readHead = 0;
    }

    readFixedLength(len) {
        let num = parseInt(this.data.slice(this.readHead,this.readHead+len).join(''), 2);
        this.readHead += len;
        return num;
    }

    readLiteral(version, packetType) {
         let val = 0;
         let originalReadHead = this.readHead;
         while(this.data[this.readHead] === 1) {
             val *= 16;
             this.readHead++;
             val += this.readFixedLength(4);
         }
        val *= 16;
        this.readHead++;
        val += this.readFixedLength(4);
        return new Literal(version, packetType, val);
    }

    readOperator(version,operatorType) {
        let lengthType = this.data[this.readHead];
        this.readHead++;
        let tokens = [];
        let len;
        if(lengthType === 0) {
            len = this.readFixedLength(15);
            let limit = this.readHead + len;
            while(this.readHead < limit) {
                tokens.push(this.tokenize())
            }
        } else {
            len = this.readFixedLength(11);
            for(let i = 0; i < len; i++) {
                tokens.push(this.tokenize())
            }
        }
        return new Operator(lengthType, len, version, operatorType, tokens);
    }

    tokenize(){
        let version = this.readFixedLength(3);
        let packetType = this.readFixedLength(3);

        if(packetType === 4) {
            return this.readLiteral(version, packetType);
        } else {
            return this.readOperator(version, packetType);
        }
    }
}

let data = rawData
    .split('\n')
    .map(packet =>
        packet
            .split('')
            .flatMap(n => parseInt(n, 16).toString(2).padStart(4,'0')
                .split('')
                .map(d => parseInt(d))
            )
    )
    .map(packet => new Packet(packet));


data.forEach(packet => {
    let tree = packet.tokenize();
    console.log(tree.getVersionSum(), tree.getValue());

});
