Visiting the site, it claims to be innocent. But the reports tell otherwise. Something fishy is going on, right?

### Case 1:

There are two clues as to what is happening: 'Google news' and 'Slow internet'. 

In Google News, news articles these days are served from Google's [AMP cache CDN](https://developers.google.com/amp/cache) especially when internet speeds are slow in Chrome. Searching a bit, it can be found that CDN caching is done by a bot with user agent 'Google-AMPHTML' or in general 'Googlebot/2.1'. Now if we try to access the site with the bot's user agent we get 'Hi impostor!'. So we're in the right track, but the server figured out that the user-agent is spoofed and it isn't the actual bot that's making the request. However we can workaround that by sending the request through the bot itself. This can be done by calculating the AMP cache URL of the site (which can be done [here](https://amp.dev/documentation/guides-and-tutorials/learn/amp-caches-and-cors/amp-cache-urls/)). Accessing the AMP cache, we get the first part of the flag.

![](https://i.imgur.com/6EI4pVS.png)

### Case 2:

This is quite similar to the Case 1 of the previous chall. Now by finding the user-agent of the feedburner bot (FeedBurner/1.0) and spoofing the request, you can get the second part of the flag.

![](https://i.imgur.com/iTz3csY.png)

### Case 3:

The clues are that it is an Android phone and the client visited the site using Chrome. Also the region given is Asia. Given slow internet, Chrome will try to load the site using [Google Weblight](https://developers.google.com/search/docs/advanced/mobile/web-light). The fetch process is done by a bot as well. So spoofing the user-agent of the bot ('googleweblight'), we get 'Hi impostor!'. So again, we're in the right track, but the server figured out that the user-agent is spoofed. We can work around that by visiting the site through googleweblight itself. Use the URL format mentioned [here](https://developers.google.com/search/docs/advanced/mobile/web-light) and you'll get the final part of the flag.

![](https://i.imgur.com/LgqLW5C.png)

### PS
If you were to go by the hints, simply googling the 2nd and/or 3rd paragraph of the hint will give away the idea.
***
![](https://i.imgur.com/1W2Knf4.png)
***
![](https://i.imgur.com/ehs2JjS.png)
***
![](https://i.imgur.com/JMRs5Km.png)
***

### The flag
The complete flag is: p_ctf{Z2PrFFCkHwMDxHcdFN8LBnvl0VGlQW}


### Learn more
1. AMP in general: [https://amp.dev](https://amp.dev)
2. Google's AMP Cache: [https://developers.google.com/amp/cache](https://developers.google.com/amp/cache)
3. Google Web Light: [https://developers.google.com/search/docs/advanced/mobile/web-light](https://developers.google.com/search/docs/advanced/mobile/web-light)
4. Google Web Light: [https://en.wikipedia.org/wiki/Google_Web_Light](https://en.wikipedia.org/wiki/Google_Web_Light). You can see why the clue for the region makes sense.

