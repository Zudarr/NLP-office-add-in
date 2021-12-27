const child_process = require('child_process').spawn;

exports.runPython = function(inputDoc){
    var process = child_process('python',['../PythonCode/NLP.py',inputDoc]);
    process.stdout.on('data',data =>{
        return data;
    })
}
