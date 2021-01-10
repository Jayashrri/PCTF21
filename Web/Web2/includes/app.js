const express = require("express");
const path = require("path");
const session = require("express-session");
const cookieparser = require("cookie-parser");
const mongoose = require("mongoose");
const config = require("config");
const authMiddleware = require("./middlewares/authMiddleware");

const app = new express();

const PORT = config.get("PORT");
//Body Parser
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

//EJS
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

//Public
app.use(express.static(path.join(__dirname, "public")));

//Session
app.use(
	session({
		secret: config.get("sessionSecret"),
		resave: false,
		saveUninitialized: true,
		cookie: { httpOnly: false, secure: false, maxAge: 600000 },
	})
);

//Cookie Parser
app.use(cookieparser(config.get("sessionSecret")));

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
	if (req.email === "admin@admin.com") res.render("admin");
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
		if (req.email === "admin@admin.com") res.redirect("/");
		else next();
	},
	jobsRouter
);

//Preview Route
app.get("/finalpreview", (req, res) => {
	res.render("finalPreview", { data: req.body });
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
