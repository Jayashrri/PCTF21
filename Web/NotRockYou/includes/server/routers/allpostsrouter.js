const router = require("express").Router();
const { Post } = require("../models");

router.get("/", async (req, res) => {
	if (!req.name) {
		res.redirect("/");
	} else if (req.name === "admin") {
		res.redirect("/admin");
	} else {
		let posts = await Post.find({ isReported: false }).sort("-created");
		res.render("allposts", { name: req.name, posts: posts });
	}
});

router.post("/", async (req, res) => {
	if (!req.name) {
		res.redirect("/");
	}
	const { postid } = req.body;
	await Post.findByIdAndUpdate(
		{ _id: postid },
		{ isReported: true },
		{ new: true },
		(err, doc) => {
			if (err) {
				res.status(500).send("ERROR REPORTING");
			} else {
				res.redirect("/allposts");
			}
		}
	);
});

module.exports = router;
