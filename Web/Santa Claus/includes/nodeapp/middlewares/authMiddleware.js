const config = require("config");
const jwt = require("jsonwebtoken");

function authMiddleware(req, res, next) {
	if (req.cookies.jwt) {
		const token = req.cookies.jwt;
		jwt.verify(
			token,
			config.get("jwtSecret"),
			{ algorithms: ["HS256"] },
			function (err, user) {
				if (err) {
					console.log(err);
					res.sendStatus(403);
				}
				req.email = user.email;
				next();
			}
		);
	} else {
		next();
	}
}

module.exports = authMiddleware;
