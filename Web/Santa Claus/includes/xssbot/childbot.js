const zombie = require("zombie");

const baseURL = process.argv[2];
const fullURL = process.argv[3];
const accessToken = process.argv[4];
const UA = "hello from pctf";
let bot = new zombie({ userAgent: UA });

bot.visit(`${baseURL}`);

console.log(`Setting Cookie ${accessToken}`);
bot.setCookie("jwt", accessToken);

bot.visit(fullURL, () => {
	console.log(`URL visited: ${fullURL}`);
});
