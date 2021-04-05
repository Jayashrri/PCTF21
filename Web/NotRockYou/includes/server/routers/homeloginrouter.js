const router = require("express").Router();
const jwt = require("jsonwebtoken");
const config = require("../config");
const { User } = require("../models");

router.get("/", async (req, res) => {
	if (req.name === "admin") {
		res.redirect("/admin");
	} else if (req.name) {
		res.redirect("/myposts");
	} else res.render("index");
});
router.post("/", async (req, res) => {
	const { name, password } = req.body;
	await User.findOne({ name: name }, async (err, user) => {
		if (err) {
			res.status(404).send("Error Finding User");
		} else if (!user) {
			res.render("index", { notfound: true });
		} else {
			if (password === user.password) {
				let accessToken = jwt.sign(
					{ name: name, password: password },
					config.jwtsecret,
					{
						algorithm: "HS256",
					}
				);
				res.cookie("auth", accessToken, {
					maxAge: config.cookieExpTime,
					httpOnly: true,
				});
				res.redirect("/myposts");
			} else {
				res.render("index", { notfound: true });
			}
		}
	});
});
module.exports = router;
