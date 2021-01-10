const router = require("express").Router();
const { User, Payload } = require("../model/models");

router.get("/", (req, res) => {
	if (!req.email) {
		res.render("jobslogin", { user: req.email });
	} else {
		res.render("jobs");
	}
});

router.post("/", async (req, res) => {
	if (!req.email) {
		res.redirect("/login");
	}

	const { name, dob, education, job } = req.body;
	const newPayload = new Payload({
		name,
		dob,
		education,
		job,
		visited: false,
	});
	await newPayload
		.save()
		.then((savedDoc) => {
			User.findOneAndUpdate(
				{ email: req.email },
				{
					$addToSet: { submissions: savedDoc._id },
				},
				{
					new: true,
				},
				(err, doc) => {
					if (err) console.log(err);
					else res.redirect("/jobs/success");
				}
			);
		})
		.catch((err) => console.log(err));
});

router.get("/success", (req, res) => {
	res.render("applicationSuccess");
});

module.exports = router;
