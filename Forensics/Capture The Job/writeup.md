# Capture The Job

We have two packet capture files. Let us look at them one by one:

## 1.pcap

On opening the file in Wireshark and following the TCP stream, we can see that it is the traffic of a login page without SSL and the credentials being captured as well. On looking at the ARP packets, we notice abnormalities:

![ARP](https://imgur.com/J1HufHA.png)

* The same MAC address has been assigned to different IPs.
* The same IP has two different MAC address entries (Packet No. 56 and 64)

This is indicative of a Man in the Middle ARP Spoofing attack performed to capture the credentials. On searching the web one can find out that ARP Spoofing has the MITRE ATT&CK sub-technique ID of `T1557.002` which is the first part of the flag.

## 2.pcap

On opening the file in Wireshark, we notice a lot of anomalous behaviour:

![Keep-Alive](https://imgur.com/MPxI8Qp.png)

* A large number of requests from different ports have been made in a short amount of time. All of these have unusual headers. This indicates a DoS attack.
* They all have a repetitive pattern of making a three-way handshake and then sending a keep-alive signal.
* All such packets end with a single CRLF (0d 0a) rather than two CRLFs to indicate end of request. Hence, the server keeps waiting for the requests to be complete.
* After around 5 seconds, a second wave of such keep-alive requests are being made.

All these point to the Slow Loris attack. So according to the flag format, the second part of the flag would be `slowloris`.
