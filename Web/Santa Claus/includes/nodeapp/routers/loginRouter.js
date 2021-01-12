const router = require("express").Router();
const { User } = require("../model/models");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const config = require("config");

router.get("/", (req, res) => {
	if (req.email) res.redirect("/jobs");
	else res.render("login", { user: req.email });
});

router.post("/", async (req, res) => {
	if (req.email) res.redirect("/jobs");
	const { email, password } = req.body;
	await User.findOne({ email }, (err, user) => {
		if (!user) {
			res.render("login", { noUser: true, user: req.email });
		} else {
			bcrypt.compare(password, user.password, function (err, result) {
				if (err) {
					console.log(err);
					res.status(400).send("Error");
				}
				if (result) {
					let accessToken = jwt.sign(
						{ email: email },
						config.get("jwtSecret"),
						{ algorithm: "HS256" }
					);
					res.cookie("jwt", accessToken, {
						maxAge: config.get("cookieExpTime"),
					});
					res.redirect("/jobs");
				} else {
					res.send("wring pass");
				}
			});
		}
	}).catch((err) => console.log(err));
});

module.exports = router;
