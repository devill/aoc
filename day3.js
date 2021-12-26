
var fs = require('fs');

fs.readFile('./input3.txt', 'utf8', function (err, rawData) {
    if (err) {
        throw err;
    }
    let data = rawData.split('\n');
    data.pop();

    const filterArray = (array, callback) => {
        let index = 0;
        while(array.length > 1) {
            const m = callback(array.map(i => parseInt(i[index])));
            array = array.filter(l => parseInt(l[index]) === m);
            index++;
        }
        return parseInt(array[0],2);
    }

    let test = ['00100','11110','10110','10111','10101','01111','00111','11100','10000','11001','00010','01010',]

    const sum = (a) => a.reduce((acc,v) => acc+v,0);
    const majority = array => sum(array) * 2 >= array.length ? 1 : 0;
    const minority = array => sum(array) * 2 < array.length ? 1 : 0;
    const v1 = filterArray(data, majority);
    const v2 = filterArray(data, minority);
    console.log(v1,v2,v1*v2);
});


