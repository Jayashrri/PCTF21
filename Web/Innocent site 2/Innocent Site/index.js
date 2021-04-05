var express = require('express');
const rateLimit = require("express-rate-limit");
const slowDown = require('express-slow-down');
const execute = require('async-execute');

const reverseDNSLookup = async (ip) => {
  if (/^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$/.test(ip)) {
    const hostResult = await execute(`host ${ip} 2>&1 || true`);
    console.log(hostResult);
    if (/.*(google\.com|googlebot\.com)[.]?$/.test(hostResult)) {
      const host = hostResult.split(' ').pop();
      const reverseHostResult = await execute(`host ${host} 2>&1 || true`);
      console.log(reverseHostResult);
      if (reverseHostResult.includes(ip)) {
        return true;
      }
    }
  }
  return false;
}

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

const WEBLIGHT_RE = new RegExp('.*googleweblight.*');
const FEEDBURNER_RE = new RegExp('.*FeedBurner\/1.0.*');
const AMP_RE = new RegExp('.*Google\-AMPHTML.*');
const GOOGLE_21 = new RegExp('.*Googlebot/2\.1.*')

router.get('/index.html', function (req, res, next) {
  req.headers['if-none-match'] = '';
  req.headers['if-modified-since'] = '';
  next();
});

router.get('/index.html', rateLimiter, speedLimiter, async function (req, res, next) {
  if (AMP_RE.test(req.headers['user-agent']) || GOOGLE_21.test(req.headers['user-agent'])) {
    console.log(req.headers);
    let ip = req.ip;
    console.log(ip);
    if (ip) {
      if (ip.substr(0, 7) == "::ffff:") {
        ip = ip.substr(7)
      }
      try {
        googlebot = await reverseDNSLookup(ip);
      } catch (e) {
        googlebot = false;
      }
      if (googlebot) {
        res.send(`<!DOCTYPE html>
        <html ⚡>
           <head>
              <meta charset = "utf-8">
              <title>Totally Legit News(TM)</title>
              <script async src="https://cdn.ampproject.org/v0.js"></script>
             <link rel="canonical" href="http://20ce4536d0c4.ngrok.io/index.html">
              <meta name = "viewport" content = "width = device-width, initial-scale = 1.0">
              <script type="application/ld+json">
                {
                  "@context": "http://schema.org",
                  "@type": "NewsArticle",
                  "headline": "New revelation reveals that Sun is the one orbiting Earth",
                  "datePublished": "2021-01-01T12:00:00Z",
                }
              </script>
              <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
           </head>
           <body>
              <header role = "banner">
                 <h2>New revelation reveals that Sun is the one orbiting Earth</h2>
              </header>
              <h4>Exclusive interview with NOSA scientist</h4>
              <article>
                 <section>
                    Holy $hit we've all been lied to for years. Wake up sheeple!!!
                 </section>
                 <section>
                    Sun orbits earth at a distance of 10 million football fields from earth
                 </section>
                 <section>
                    Landmark study by Dr. Legit reveals the basic fact
                 </section>
                 <section>
                    Fake news outlets were quick to dismiss this as a "Flat earth piece of shit"
                 </section>
                 <section>
                    Here's a flag: Part 1/3: p_ctf{Z2PrFFCkHw
                 </section>
                 ` + (new Date()).getTime() + `
              </article>
              <footer>
                 <p>We at Totally Legit News(TM) are dedicated to bringing to you the latest news which may not or may not be not not true</p>
              </footer>
           </body>
        </html>`);
      } else {
        res.send('Hi impostor! <br><br> ' + (new Date()).getTime());
      }
    } else {
      res.send('Who are you?');
    }
  } else if (WEBLIGHT_RE.test(req.headers['user-agent'])) {
    console.log(req.headers);
    let ip = req.ip;
    console.log(ip);
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
        res.send(`<h1>Do you want to be successful in life?</h1>
        <br>
        <h3>Then what are you waiting for? Register for my free webinar! Limited free seats!!!</h3>
        <br>
        <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">Click here to register</a>
        
        <br>
        ` + (new Date()).getTime() + `
        <p>And btw, here's the flag you asked for: Part 3/3: Bnvl0VGlQW}</p>`);
      } else {
        res.send('Hi impostor! <br><br> ' + (new Date()).getTime());
      }
    } else {
      res.send('Who are you?');
    }
  } else if (FEEDBURNER_RE.test(req.headers['user-agent'])) {
    res.send(`<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
    
    <channel>
      <title>The Scientific Feed</title>
      <link>https://aaldhfkdfaafhjdgk.ahjlfk</link>
      <description>News you will never hear anywhere else</description>
      <item>
        <title>Earth is flat</title>
        <link>https://aaldhfkdfaafhjdgk.ahjlfk</link>
        <description>It is proven. No need to prove again we guess.</description>
      </item>
      <item>
        <title>Flags  ` + (new Date()).getTime() + `</title>
        <link>https://aaldhfkdfaafhjdgk.ahjlfk</link>
        <description>Something special about flags: Here's part 2/3: MDxHcdFN8L</description>
      </item>
    </channel>
    
    </rss>`);
  } else {
    res.send('<h1>I\'m another innocent site UwU</h1> <br><br> ' + (new Date()).getTime());
  }
});



module.exports = router;
