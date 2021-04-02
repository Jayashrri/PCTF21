const { spawn } = require("child_process");
const kill = require("tree-kill");
const config = require("./config");
const mongoose = require("mongoose");
const fs = require("fs");
const jwt = require("jsonwebtoken");
let accessToken = jwt.sign({ email: config.adminEmail }, config.jwtSecret, {
	algorithm: "HS256",
});

//////////////////// SCHEMA /////////////////////////////////
const payloadSchema = new mongoose.Schema(
	{
		name: {
			type: String,
			required: true,
		},
		dob: {
			type: String,
			required: true,
		},
		education: {
			type: String,
			required: true,
		},
		job: {
			type: String,
			required: true,
		},
		visited: {
			type: Boolean,
			required: true,
		},
		email: {
			type: String,
		},
	},
	{
		timestamps: { createdAt: "created", updatedAt: "updated" },
	}
);

const Payload = mongoose.model("Payload", payloadSchema);
/////////////////////////////////////////////

/////////////MONGOOSE////////////////////////
mongoose
	.connect(config.mongoString, {
		useNewUrlParser: true,
		useUnifiedTopology: true,
		useFindAndModify: false,
	})
	.then(() => {
		console.log("Bot Connected to MongoDB");
	})
	.catch((err) => {
		console.log(err);
		process.exit(1);
	});
///////////////////////////////////////////

const main = async () => {
	const payload = await Payload.findOne({ visited: false });
	console.log(`PAYLOAD ${payload}`);
	if (!payload) {
		fs.writeFile("state", "0", function (err) {
			if (err) return console.log(err);
			console.log("No payloads found");
			process.exit(0);
		});
	} else {
		fs.writeFile("state", "1", function (err) {
			if (err) return console.log(err);
			console.log("Payloads found");
		});

		const seconds = config.seconds;
		const baseURL = config.baseURL;
		const fullURL = `${baseURL}/finalpreview?name=${payload.name}&dob=${payload.dob}&education=${payload.education}&job=${payload.job}&submit=Submit`;

		var child = spawn("npm", [
			"run",
			"debug",
			baseURL,
			fullURL,
			accessToken,
		]);
		const timeOut = setTimeout(() => {
			console.log("Timeout");
			try {
				console.log(`Process: ${child.pid} killing`);
				kill(child.pid);
			} catch (e) {
				console.log(`KILL ERROR ${child.pid} ## ${e}`);
			}
		}, seconds * 1000);

		await Payload.findByIdAndUpdate(
			{ _id: payload._id },
			{ visited: true },
			{ new: true },
			(err, payload) => {
				if (err) console.log(err);

				console.log("Updated payload:");
				console.log(payload);
			}
		);

		child.on("err", (err) => {
			console.log(`Error ${child.pid} ###  ${err}`);
		});

		child.on("exit", () => {
			console.log(`Stopped ${child.pid} ${seconds} `);
			clearTimeout(timeOut);
		});
		child.on("close", () => {
			console.log(`Closed ${child.pid} ### ${seconds} `);
			clearTimeout(timeOut);
			process.exit(0);
		});

		child.stdout.on("data", (data) =>
			console.log(`Data of ${child.pid} ### ${data.toString()}`)
		);
	}
};

main();
