# Writeup

We are provided a network capture file. Upon ananlysis of the provided file with a tool like Wireshark, it becomes apparent that the provided network traffic doesn't provide any sort of meaning.

The question on the other hand provides a little clue as to what might be hidden inside. It alludes to the **first forms of electronic communication** which references the telegraph and by extension, the Morse Code encoding.

WIth that info in hand, we can observe that the network traffic follows a bizzare but recognizable pattern. They seem to only contain **TCP**, **UPD** and **DNS** connections. 

Now we need to connect this to the telegraph clue from before. So, a telegraph message, in morse code, consists of " _ ", " . " and spaces. Now, the substitution follows the facts with the network protocols being used. We substitute TCP connections with a " _ " because of their longer transmmission times, the UDP connections with a " . " because of their shorter transmmission times. Since we are only left with the spaces, the DNS connections are substituted.

It can either be decoded by hand, or with a script that recognizes the particular transport formats and substitutes them accordingly, as is provided [here](SolnStuff/script.sh), to get the appropriate morse code of the message. This can then be translated with the help of an online morse code converter like [this](https://morsecode.world/international/translator.html)

## Running the script

![script.sh run](SolnStuff/script.png)
