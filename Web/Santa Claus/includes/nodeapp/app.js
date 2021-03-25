const express = require("express");
const path = require("path");
const cookieparser = require("cookie-parser");
const mongoose = require("mongoose");
const config = require("config");
const authMiddleware = require("./middlewares/authMiddleware");

const app = new express();

const PORT = config.get("PORT") || 8000;

//Body Parser
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

//EJS
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

//Public
app.use(express.static(path.join(__dirname, "public")));

//Cookie Parser
app.use(cookieparser());

//mongoose

mongoose
	.connect(config.get("mongoString"), {
		useNewUrlParser: true,
		useUnifiedTopology: true,
		useFindAndModify: false,
	})
	.then(() => console.log("Connected to MongoDB"))
	.catch((err) => console.log(err));

//AuthMiddleware
app.use(authMiddleware);

//Index Page
app.get(["/", "/index"], (req, res) => {
	if (req.email === config.get("adminEmail"))
		res.render("admin", { flag: config.get("flag") });
	else if (req.email) res.redirect("/jobs");
	else res.render("index");
});

//Routers
const loginRouter = require("./routers/loginRouter");
const signupRouter = require("./routers/signupRouter");
const submitSiteRouter = require("./routers/submitSiteRouter");
const jobsRouter = require("./routers/jobsRouter");

app.use("/login", loginRouter);
app.use("/signup", signupRouter);
app.use("/submitSite", submitSiteRouter);
app.use(
	"/jobs",
	(req, res, next) => {
		if (req.email === config.get("adminEmail")) res.redirect("/");
		else next();
	},
	jobsRouter
);

//Preview Route
app.get("/finalpreview", (req, res) => {
	res.render("finalPreview", { data: req.body });
});

//Job Accept and Reject Routes
app.post("/jobAccept", (req, res) => {
	if (req.email === config.get("adminEmail")) res.json({ accept: "success" });
	else res.json({ accept: "fail" });
});
app.post("/jobReject", (req, res) => {
	if (req.email === config.get("adminEmail")) res.json({ reject: "success" });
	else res.json({ reject: "fail" });
});
//Logout
app.get("/logout", (req, res) => {
	res.cookie("jwt", "", { maxAge: 0 });
	res.redirect("/");
});

//Server
app.listen(PORT, () => {
	console.log(`App listening on PORT: ${PORT}`);
});
