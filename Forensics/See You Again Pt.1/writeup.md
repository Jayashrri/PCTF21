# See You Again Pt.1

One approach to starting this would be to try and e-mail the given address, as instant reply suggests the possibility of an Out-Of-Office AutoReply. Doing that gives us an email with the following reply:

```txt
I'm busy working on a project called jakegodfreyb4c43717/Wifi-Project. Hence I'll be slow in replying to you. Sorry. 
```

The naming style indicates it could be a Github repository, so we can try looking into it and see if we can branch from there. The repo contains some PPTs and a packet capture file from his home router. On opening the capture file, we can see WiFi traffic with just the 4-way handshake being captured.

The relevant part to us is the MAC address. Thanks to [WiGLE](wigle.net), we can try and find the location of the device from its MAC address if we're lucky. On entering the MAC address and zooming into the obtained location, we get its co-ordinates.

![wigle-ss](https://imgur.com/5rmHJwh.png)
