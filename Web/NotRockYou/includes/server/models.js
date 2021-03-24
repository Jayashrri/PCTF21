const mongoose = require("mongoose");

const userSchema = new mongoose.Schema(
	{
		name: {
			type: String,
			required: true,
		},
		password: {
			type: String,
			required: true,
		},
	},
	{
		timestamps: { createdAt: "created", updatedAt: "updated" },
	}
);

const postsSchema = new mongoose.Schema(
	{
		content: {
			type: String,
			required: true,
		},
		user: {
			type: String,
			required: true,
		},
		isReported: {
			type: Boolean,
			required: true,
		},
	},
	{
		timestamps: { createdAt: "created", updatedAt: "updated" },
	}
);

const User = mongoose.model("User", userSchema);
const Post = mongoose.model("Post", postsSchema);
module.exports = { User, Post };
