const router = require("express").Router();

const { Post } = require("../models");

router.get("/", async (req, res) => {
	if (!req.name) {
		res.redirect("/");
	} else if (req.name === "admin") {
		res.redirect("/admin");
	} else {
		let posts = await Post.find({ user: req.name }).sort("-created");
		posts = posts.map((post, index, p) => {
			return {
				...post._doc,
				number: p.length - index,
			};
		});
		res.render("myposts", { name: req.name, posts: posts });
	}
});

router.post("/", async (req, res) => {
	if (!req.name) {
		res.redirect("/");
	}
	const { content } = req.body;

	const newPost = new Post({
		content: content,
		isReported: false,
		user: req.name,
	});
	await newPost
		.save()
		.then(() => {
			res.redirect("/myposts");
		})
		.catch((err) => {
			console.log(err);
			res.send("Error Creating Post");
		});
});

module.exports = router;
