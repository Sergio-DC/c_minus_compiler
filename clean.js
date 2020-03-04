var readline = require('readline');
var fs = require('fs');

const writeStream = fs.createWriteStream("./clean_csv/output/matrix_csv.txt",{ encoding: "utf8"});

var myInterface = readline.createInterface({
  input: fs.createReadStream('./clean_csv/matrix_csv.csv'),
  output: writeStream
});

var lineno = 0;
var appendFile = '';
myInterface.on('line', function (line) {
    if(lineno != 0)
        line = line.replace(/,/g," ");
    else {
      line = line.replace(/,/g,"_");
      line = line.replace(/"_"/,",");
      line = line.replace(/_/, " ");
      console.log(line);
    }
    lineno++;
    writeStream.write(line + "\n");
});