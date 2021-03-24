const Express = require("express");
const app = new Express();
const config = require("./config");
const jwt = require("jsonwebtoken");
const mongoose = require("mongoose");
const cookieparser = require("cookie-parser");
const { User, Post } = require("./models");
const path = require("path");

const PORT = config.PORT || 8000;

const jwtrouter = require("./routers/jwtrouter");
const homeloginrouter = require("./routers/homeloginrouter");
const registerrouter = require("./routers/registerrouter");
const postsrouter = require("./routers/postsrouter");
const allpostsrouter = require("./routers/allpostsrouter");
const adminrouter = require("./routers/adminrouter");
const logoutrouter = require("./routers/logoutrouter");

app.use(Express.json());
app.use(Express.urlencoded({ extended: true }));

app.use(cookieparser());

app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

mongoose
	.connect(config.mongostring, {
		useUnifiedTopology: true,
		useNewUrlParser: true,
		useFindAndModify: false,
	})
	.then(() => {
		console.log("Connected to DB");
	})
	.catch((err) => {
		console.log("Error connecting to DB");
		console.log(err);
		process.exit(1);
	});

app.use(jwtrouter);
app.use("/", homeloginrouter);
app.use("/register", registerrouter);
app.use("/myposts", postsrouter);
app.use("/allposts", allpostsrouter);
app.use("/admin", adminrouter);
app.use("/logout", logoutrouter);

app.listen(PORT, () => {
	console.log(`App is listening on port ${PORT}`);
});
