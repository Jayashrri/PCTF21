Visiting the site, it claims to be innocent. But the reports tell otherwise. Something fishy is going on, right?

### Case 1:

This is a typical case of SEO spam where people trick googlebot to rank higher in google search. Change your user agent to 'googlebot' to visit the site as googlebot and see why it ranks higher in search. There you get the first part of the flag.

Now to see the popup page itself, clearly nothing can be seen if we visit the site directly. But we can speculate that it has something to do with google search. Search for something in Google and you'll find that when a link is clicked, the request made to the actual url has its referer header set to 'https://www.google.com'. Try to visit the site with the referer header set to 'https://www.google.com' and you'll get the popup site. And there you get the second part of the flag.

### Case 2:

This is one of those twitter bitcoin scams. But however as we know already, visiting the site directly reveals nothing. If you notice, any link shared via twitter will be shortened automatically to t.co/hash. Visit some url from a tweet and observe the referer in the request. It's 'https://t.co'. Now visit the site with referer set to 'https://t.co' and you get the page and the third part of the flag.

The complete flag is: p_ctf{tKJPGkE2nojV7UvYETRZyiFej8wejb}


