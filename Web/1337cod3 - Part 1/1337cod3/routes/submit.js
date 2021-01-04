var express = require('express');
const rateLimit = require("express-rate-limit");
const cryptoRandomString = require('crypto-random-string');
const { fork, spawn } = require('child_process');
const fs = require("fs");
const genTestCases = require('../problems/testcase.gen');
const kill = require('tree-kill');
const slowDown = require('express-slow-down');

var router = express.Router();

const rateLimiter = rateLimit({
  windowMs: 30 * 1000,
  max: 1,
  message: "Only one submission is allowed per 30 seconds. Try again later or sUbScRiBe tO pReMiUm"
});

const speedLimiter = slowDown({
  windowMs: 60 * 1000,
  delayAfter: 1,
  delayMs: 500,
  skipFailedRequests: true
});

const cleanup = (dir) => {
  fs.rmdirSync(dir, { recursive: true });
}

router.post('/', rateLimiter, speedLimiter, async (req, res) => {
  let compilationId = cryptoRandomString({ length: 10 });
  let tempDir = './temp/' + compilationId;
  let sandboxDir = tempDir + '/sandbox';
  return (new Promise(function (resolve, reject) {
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir);
    }
    if (!fs.existsSync(sandboxDir)) {
      fs.mkdirSync(sandboxDir);
    }
    fs.writeFileSync(`${tempDir}/main.c`, req.body.code);

    const compiler = spawn('/home/node/wasi-sdk-12.0/bin/clang', [
      '--sysroot=/home/node/wasi-sdk-12.0/share/wasi-sysroot',
      `${tempDir}/main.c`, '-o', `${tempDir}/main.wasm`
    ], {
      detached: true,
    });

    let compileTimeout = setInterval(() => {
      clearInterval(compileTimeout);
      kill(compiler.pid, 'SIGKILL');
      reject('TLE - Compilation timed out!');
    }, 1000);

    let savedOutput = '';
    compiler.stdout.on('data', (data) => savedOutput += data.toString());
    compiler.stderr.on('data', (data) => savedOutput += data.toString());
    compiler.on('exit', function (code) {
      clearInterval(compileTimeout);
      if (code == 0) {
        resolve(compilationId);
      } else {
        reject('Compilation Failed: <br><br><pre>' + savedOutput + '</pre>');
      }
    });

  })).then(
    (compilationId) => new Promise(function (resolve, reject) {
      genTestCases();
      fs.copyFile('./problems/input.txt', sandboxDir + '/input.txt', () => { });
      const child = fork(__dirname + '/../run.js', { silent: true });
      child.send({
        compilationId: compilationId,
        code: req.body
      });

      let runTimeout = setInterval(() => {
        clearInterval(runTimeout);
        kill(child.pid, 'SIGKILL');
        reject('TLE - Execution timed out!');
      }, 1000);

      let savedOutput = '';
      child.stdout.on('data', (data) => savedOutput += data.toString());
      child.stderr.on('data', (data) => savedOutput += data.toString());
      child.on('exit', () => {
        clearInterval(runTimeout);
        if (!fs.existsSync(sandboxDir + '/output.txt')) {
          savedOutput += '\nOutput file not found!';
        } else {
          let userOutput = fs.readFileSync(sandboxDir + '/output.txt').toString();
          let solution = fs.readFileSync('./problems/output.txt').toString();
          if (userOutput == solution) {
            savedOutput += "\nAC - Here's your flag: [REDACTED]";
          } else {
            savedOutput += "\nWA - Wrong solution";
          }
        }
        resolve('<pre>' + savedOutput + '</pre>');
      });
    })
      .then(
        (message) => {
          cleanup(tempDir);
          res.send(message);
        }
      )
  ).catch(
    (message) => {
      cleanup(tempDir);
      res.send(message);
    }
  );
});

module.exports = router;