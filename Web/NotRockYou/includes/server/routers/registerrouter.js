const router = require("express").Router();

const { User } = require("../models");

router.get("/", async (req, res) => {
	if (req.name) {
		res.redirect("/myposts");
	} else res.render("register");
});

router.post("/", async (req, res) => {
	const { name, password } = req.body;

	await User.findOne({ name }, async (err, user) => {
		if (err) {
			res.status(400).send("REGISTER ERROR. TRY AFTER SOMETIME");
		}
		if (user) {
			res.render("register", {
				existingUser: true,
			});
		} else {
			const newuser = new User({
				name,
				password,
			});
			await newuser
				.save()
				.then(() => {
					res.render("register", {
						registered: true,
					});
				})
				.catch((err) => {
					console.log(err);
					res.send("ERROR CREATING USER");
				});
		}
	});
});

module.exports = router;
