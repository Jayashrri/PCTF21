Visiting the site, it claims to be innocent. But the reports tell otherwise. Something fishy is going on, right?

### Case 1:

This is a typical case of SEO spam where people trick googlebot to rank higher in google search. Change your user agent to 'googlebot' to visit the site as googlebot and see why it ranks higher in search. There you get the first part of the flag.

Now to see the popup page itself, clearly nothing can be seen if we visit the site directly. But we can speculate that it has something to do with google search. Search for something in Google and you'll find that when a link is clicked, the request made to the actual url has its referer header set to 'https://www.google.com'. Try to visit the site with the referer header set to 'https://www.google.com' and you'll get the popup site. And there you get the second part of the flag.

### Case 2:

This is one of those twitter bitcoin scams. But however as we know already, visiting the site directly reveals nothing. If you notice, any link shared via twitter will be shortened automatically to t.co/hash. Visit some url from a tweet and observe the referer in the request. It's 'https://t.co'. Now visit the site with referer set to 'https://t.co' and you get the page and the third part of the flag.

### Case 3:

There are two clues as to what is happening: 'Google news' and 'Slow internet'. 

Using the first clue, Google news is generally aggregated by the googlebots these days. So we can try to access the page with googlebot's useragent like before. However, no luck this time.
Coming to the second clue, news articles these days are served from Google's [AMP cache CDN](https://amp.dev) when internet speeds are slow. Searching a bit, it can be found that it this CDN caching is done by a bot with user agent 'Google-AMPHTML'. Now if we try to access the site with the bot's user agent we get 'Hi impostor! Now buy Google lol'. So we're in the right track, but the server figured out that the user-agent is spoofed and it isn't the actual bot that's making the request. However we can workaround that by sending the request through the bot itself. This can be done by calculating the AMP cache URL of the site (which can be done [here](https://amp.dev/documentation/guides-and-tutorials/learn/amp-caches-and-cors/amp-cache-urls/)). Accessing the AMP cache, we get the fourth part of the flag.

### Case 4:

This is quite similar to the Case 1. Now by finding the user-agent of the feedburner bot (FeedBurner/1.0) and spoofing the request, you can get the fifth part of the flag.

### Case 5:

The clues are that it is an Android phone and the client visited the site using Chrome. Given slow internet, Chrome will try to load the site using [Google Weblight](https://developers.google.com/search/docs/advanced/mobile/web-light). The fetch process is done by a bot as well. So spoofing the user-agent of the bot ('googleweblight'), we get 'Hi impostor! Now buy Google lol'. So again, we're in the right track, but the server figured out that the user-agent is spoofed. We can work around that by visiting the site through googleweblight itself. Use the URL format mentioned [here](https://developers.google.com/search/docs/advanced/mobile/web-light) and you'll get the final part of the flag.

The complete flag is: p_ctf{tKJPGkE2nojV7UvYETRZyiFej8wejbZ2PrFFCkHwMDxHcdFN8LBnvl0VGlQW}


