Visiting the site, it claims to be innocent. But the reports tell otherwise. Something fishy is going on, right?

### Case 1:

This case is modeled around something that happens a lot these days where you could see google search results like:

![](https://i.imgur.com/MQl9u0k.png) 

If you'd click such links you'd be forwarded to some malware site or some site stuffed with ads, but if you drop the exact URL into online malware analysis sandboxes like [Hybrid Analysis](https://www.hybrid-analysis.com/submissions/quick-scan/urls), you'll get a negative result. 

How does that work? The referer in the request sent to the site will give away whether you were there in the site by clicking a search result and thus it loads the malicious site only if the referer is the same as the one you'd get by clicking a google search result. 

How does this page even rank higher in search? Well, let's check out the cached version offered by google search by clicking:

![](https://i.imgur.com/hrn8ZDf.png)

We see this:

![](https://i.imgur.com/jakPd4A.png)

Ah yes, some [Spamdexing](https://en.wikipedia.org/wiki/Spamdexing) going on there.

Now coming back to the challenge, change your user agent to 'googlebot' to visit the site as googlebot and see why it ranks higher in search. There you get the first part of the flag.

![](https://i.imgur.com/YaYBBOy.png)

Now to see the popup page itself, clearly nothing can be seen if we visit the site directly. Search for something in Google and you'll find that when a link is clicked, the request made to the actual url has its referer header set to 'https://www.google.com'. Try to visit the site with the referer header set to 'https://www.google.com' and you'll get the popup site. And there you get the second part of the flag.

![](https://i.imgur.com/Z8l3rBZ.png)

### Case 2:

This is one of those twitter bitcoin scams. But however as we know already, visiting the site directly reveals nothing. If you notice, any link shared via twitter will be shortened automatically to t.co/hash. Visit some url from a tweet and observe the referer in the request. It's 'https://t.co'. Now visit the site with referer set to 'https://t.co' and you get the page and the third part of the flag.

![](https://i.imgur.com/FssRUPx.png)

### The flag:
The complete flag is: p_ctf{tKJPGkE2nojV7UvYETRZyiFej8wejb}


