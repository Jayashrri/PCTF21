const config = require("../config");
const jwt = require("jsonwebtoken");
const { User } = require("../models");

const jwtrouter = async (req, res, next) => {
	if (req.cookies.auth) {
		const token = req.cookies.auth;
		await jwt.verify(
			token,
			config.jwtsecret,
			{ algorithms: ["HS256"] },
			async (err, user) => {
				if (err) {
					console.log(err);
					res.cookie("auth", "", { maxAge: 0, httpOnly: true });
					res.sendStatus(403);
				} else {
					const { name, password } = user;

					await User.findOne(
						{ name: name, password: password },
						async (err, userdetails) => {
							if (err) {
								res.cookie("auth", "", {
									maxAge: 0,
									httpOnly: true,
								});
								res.sendStatus(403);
							} else if (userdetails) {
								req.id = userdetails._id;
								req.name = name;
								req.password = password;
							} else {
								console.log("No user found");
								res.cookie("auth", "", {
									maxAge: 0,
									httpOnly: true,
								});
								res.sendStatus(403);
							}
						}
					);
				}
			}
		);
	}
	next();
};

module.exports = jwtrouter;
