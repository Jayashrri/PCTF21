const { WASI } = require("@wasmer/wasi");
const nodeBindings = require("@wasmer/wasi/lib/bindings/node");
const fs = require("fs");

process.on('message', async (message) => {
    try {
        await run(message.compilationId, message.code);
        console.log('\n\nCode ran successfully!');
    } catch(e) {
        console.log('\n\n' + e.stack.split('\n').slice(0, 2).join('\n'));
    }
    process.exit(0);
});

const run = async (compilationId, code) => {
    let wasi = new WASI({
        preopenDirectories: {
            '.': 'temp/' + compilationId + '/sandbox'
        },
        args: [],
        env: {},
        bindings: {
            ...(nodeBindings.default || nodeBindings),
            fs: fs
        }
    });
    
    let wasmBytes = new Uint8Array(fs.readFileSync('./temp/' + compilationId + '/main.wasm')).buffer;
    let wasmModule = await WebAssembly.compile(wasmBytes);
    let instance = await WebAssembly.instantiate(wasmModule, {
        ...wasi.getImports(wasmModule)
    });

    wasi.start(instance);
}