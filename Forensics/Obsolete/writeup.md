# Writeup

We are provided a network capture file. Upon ananlysis of the provided file with a tool like Wireshark, it beccomes apparent that the provided network traffic doesn't provide any sort of meaning.

The question on the other hand provides a little clue as to what might be hidden inside. It alludes to the **first forms of electronic communication** which references the telegraph and by extension, the Morse Code encoding.

As we observe, there are TCP connections which stand for " _ " in the encoding because of their longer transport times and the UDP connections substitute for the ' . ' for the shorter connection times. The DNS connections act as spaces.

It can either be decoded by hand, or with a script that recognizes the particular transport formats and substitutes them accordingly, as is provided [here](includes/script.sh)
