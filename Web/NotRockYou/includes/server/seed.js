const mongoose = require("mongoose");
const { User } = require("./models");
const config = require("./config");

mongoose
	.connect(config.mongostring, {
		useUnifiedTopology: true,
		useNewUrlParser: true,
		useFindAndModify: false,
	})
	.then(async () => {
		console.log("Connected to DB");
		await User.findOneAndUpdate(
			{ name: "admin" },
			{ password: config.adminpassword },
			{
				upsert: true,
				new: true,
			},
			() => {
				console.log("Admin creds loaded");
				process.exit(0);
			}
		);
	})
	.catch((err) => {
		console.log("Error connecting to DB");
		console.log(err);
		process.exit(1);
	});
