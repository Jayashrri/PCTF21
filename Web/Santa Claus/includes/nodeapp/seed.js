const mongoose = require("mongoose");
const { User } = require("./model/models");
const bcrypt = require("bcrypt");
const config = require("config");

mongoose
	.connect(config.get("mongoString"), {
		useUnifiedTopology: true,
		useNewUrlParser: true,
		useFindAndModify: false,
	})
	.then(async () => {
		console.log("Connected to DB");
		bcrypt.hash(
			config.get("adminPassword"),
			config.get("bcrypt.saltRounds"),
			async function (err, hash) {
				console.log(`Hash ${hash}`);
				if (err) {
					console.log("Error Generating hash");
					console.log(err);
					process.exit(1);
				}
				const admin = config.get("adminEmail");
				console.log(`Admin is ${admin}`);
				await User.findOneAndUpdate(
					{ email: config.get("adminEmail") },
					{ password: hash },
					{
						upsert: true,
						new: true,
					},
					() => {
						console.log("Admin creds loaded");
						process.exit(0);
					}
				);
			}
		);
	})
	.catch((err) => {
		console.log("Error connecting to DB");
		console.log(err);
		process.exit(1);
	});
