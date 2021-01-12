const router = require("express").Router();

router.get("/", (req, res) => {
	res.render("submitSite");
});

router.post("/", (req, res) => {
	res.status(200).json({ status: "ok" });
});

module.exports = router;
