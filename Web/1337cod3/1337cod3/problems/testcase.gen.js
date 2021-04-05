const fs = require("fs");

// --- TEST GENERATOR FOR DEBUGGING ONLY ---
const genInput = () => {
    let input = "";
    for (let i = 0; i < 100; i++) {
        input += Math.random() + "\n"
    }
    fs.writeFileSync('./problems/input.txt', input);
}

// --- TEST GENERATOR FOR DEBUGGING ONLY ---
const genOutput = () => {
    let output = "";
    for (let i = 0; i < 100; i++) {
        output += Math.random() + "\n"
    }
    fs.writeFileSync('./problems/output.txt', output);
}

const genTestCases = () => {
    genInput();
    genOutput();
}

module.exports = genTestCases;