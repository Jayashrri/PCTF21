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
const WEBLIGHT_RE = new RegExp('.*googleweblight.*');
const FEEDBURNER_RE = new RegExp('.*FeedBurner\/1.0.*');
const AMP_RE = new RegExp('.*Google\-AMPHTML.*');

router.get('/', rateLimiter, speedLimiter, async function (req, res, next) {
  if (req.headers.referer == 'https://www.google.com') {
    res.sendFile(path.join(__dirname, 'pages/google_response.html'));
  } else if (GOOGLEBOT_RE.test(req.headers['user-agent'])) {
    res.sendFile(path.join(__dirname, 'pages/google_spam.html'));
  } else if (req.headers.referer == 'https://t.co') {
    res.sendFile(path.join(__dirname, 'pages/twitter_scam.html'));
  } else if (AMP_RE.test(req.headers['user-agent'])) {
    const ip = req.ip;
    if (ip) {
      if (ip.substr(0, 7) == "::ffff:") {
        ip = ip.substr(7)
      }
      try {
        googlebot = await reverseDNSLookup(ip, 'google.com', 'googlebot.com');
      } catch (e) {
        googlebot = false;
      }
      if (googlebot) {
        res.sendFile(path.join(__dirname, 'pages/amp_news.html'));
      } else {
        res.send('Hi impostor! Now buy Google lol');
      }
    } else {
      res.send('Who are you?');
    }
  } else if (WEBLIGHT_RE.test(req.headers['user-agent'])) {
    const ip = req.ip;
    if (ip) {
      if (ip.substr(0, 7) == "::ffff:") {
        ip = ip.substr(7)
      }
      try {
        googlebot = await reverseDNSLookup(ip, 'google.com', 'googlebot.com');
      } catch (e) {
        googlebot = false;
      }
      if (googlebot) {
        res.sendFile(path.join(__dirname, 'pages/weblight.html'));
      } else {
        res.send('Hi impostor!');
      }
    } else {
      res.send('Who are you?');
    }
  } else if (FEEDBURNER_RE.test(req.headers['user-agent'])) {
    res.sendFile(path.join(__dirname, 'pages/feed.xml'));
  } else {
    res.sendFile(path.join(__dirname, 'index.html'));
  }
});



module.exports = router;
