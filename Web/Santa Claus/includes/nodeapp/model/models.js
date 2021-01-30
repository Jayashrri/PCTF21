const mongoose = require("mongoose");

const userSchema = new mongoose.Schema(
	{
		email: {
			type: String,
			required: true,
		},
		password: {
			type: String,
			required: true,
		},
		submissions: [mongoose.Schema.Types.ObjectId],
	},
	{
		timestamps: { createdAt: "created", updatedAt: "updated" },
	}
);

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

const User = mongoose.model("User", userSchema);
const Payload = mongoose.model("Payload", payloadSchema);

module.exports = {
	User,
	Payload,
};
