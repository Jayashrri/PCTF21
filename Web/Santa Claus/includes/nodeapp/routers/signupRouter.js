const router = require("express").Router();
const { User } = require("../model/models");
const bcrypt = require("bcrypt");
const config = require("config");

router.get("/", (req, res) => {
	if (req.email) {
		res.redirect("/jobs");
	} else {
		res.render("signup");
	}
});

router.post("/", async (req, res) => {
	const { email, password } = req.body;

	//Validate email
	var emailRegex = /^[-!#$%&'*+\/0-9=?A-Z^_a-z{|}~](\.?[-!#$%&'*+\/0-9=?A-Z^_a-z`{|}~])*@[a-zA-Z0-9](-*\.?[a-zA-Z0-9])*\.[a-zA-Z](-?[a-zA-Z0-9])+$/;
	function isEmailValid(email) {
		if (!email) return false;

		if (email.length > 254) return false;

		var valid = emailRegex.test(email);
		if (!valid) return false;

		// Further checking of some things regex can't handle
		var parts = email.split("@");
		if (parts[0].length > 64) return false;

		var domainParts = parts[1].split(".");
		if (
			domainParts.some(function (part) {
				return part.length > 63;
			})
		)
			return false;

		return true;
	}

	if (!isEmailValid(email)) {
		res.sendStatus(404);
	}

	await User.findOne({ email }, async (err, user) => {
		if (err) {
			console.log(err);
			res.status(400).send("ERROR");
		}
		if (user) {
			res.render("signup", { userExists: true });
		}

		bcrypt.hash(
			password,
			config.get("bcrypt.saltRounds"),
			async function (err, hash) {
				if (err) {
					console.log(err);
					res.sendStatus(400);
				}

				const newUser = new User({
					email,
					password: hash,
				});
				await newUser
					.save()
					.then(() => res.render("signup", { signedUp: true }))
					.catch((err) => console.log(err));
			}
		);
	}).catch((err) => console.log(err));
});

module.exports = router;
