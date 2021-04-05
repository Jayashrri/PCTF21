const router = require("express").Router();
const { Post } = require("../models");

router.get("/", async (req, res) => {
	if (req.name === "admin") {
		let posts = await Post.find({ isReported: true }).sort("-updated");
		res.render("admin", { name: req.name, posts: posts });
	} else {
		res.redirect("/");
	}
});

router.post("/", async (req, res) => {
	if (req.name === "admin") {
		const { postid } = req.body;
		await Post.findByIdAndUpdate(
			{ _id: postid },
			{ isReported: false },
			{ new: true },
			(err, doc) => {
				if (err) {
					res.status(500).send("ERROR REPORTING");
				} else {
					res.redirect("/allposts");
				}
			}
		);
	} else {
		res.redirect("/");
	}
});

module.exports = router;
