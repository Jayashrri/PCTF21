const router = require("express").Router();

router.get("/", async (req, res) => {
	res.cookie("auth", "", { maxAge: 0, httpOnly: true });
	res.redirect("/");
});

module.exports = router;
