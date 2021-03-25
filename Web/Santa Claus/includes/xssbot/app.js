const zombie = require("zombie");
const mongoose = require("mongoose");
const config = require("./config");
const jwt = require("jsonwebtoken");
let accessToken = jwt.sign({ email: config.adminEmail }, config.jwtSecret, {
	algorithm: "HS256",
});

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

const visitor = async () => {
	console.log(`Visitor Called ${new Date().toISOString()}`);
	Payload.findOne({ visited: false })
		.then((doc) => {
			if (!doc) {
				console.log("###### BOT WAITING FOR 5 SECS ######");
				setTimeout(() => {
					visitor();
				}, 5000);
			} else {
				console.log("Chosen doc:");
				console.log(doc);
				const baseURL = config.baseURL;
				let bot = new zombie();
				bot.visit(`${baseURL}`);
				console.log(`Setting Cookie ${accessToken}`);
				bot.setCookie("jwt", accessToken);
				bot.visit(
					`${baseURL}/finalpreview?name=${doc.name}&dob=${doc.dob}&education=${doc.education}&job=${doc.job}&submit=Submit`,
					() => {
						console.log(
							`URL visited: ${baseURL}/finalpreview?name=${doc.name}&dob=${doc.dob}&education=${doc.education}&job=${doc.job}&submit=Submit`
						);
						Payload.findByIdAndUpdate(
							{ _id: doc._id },
							{ visited: true },
							{ new: true },
							(err, doc) => {
								console.log("Updated Doc:");
								console.log(doc);
								visitor();
							}
						);
					}
				);
			}
		})
		.catch((err) => {
			console.log(err);
			process.exit(1);
		});
};
visitor();
