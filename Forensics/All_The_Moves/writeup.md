# Writeup

We are provided with a file with what looks to be just a bunch of random strings in lines. They are not encoded in any commonly used encoding types. We now turn our attention to the question. It makes a reference to some mysterious MVL person. On searching for that name, we are led to the chess GM, Maxime Vachier Lagrave.

So, now we have view as to that the encoding is something related to chess. On searching for chess board notation, we find the FEN notation, which the encoding used for the data here. Now, with that knowledge in mind, we can then plug this into a chess site like [lichess](https://lichess.org), and on doing that, we can see that each of these lines represent characters represnted by the pieces on the board.

Here is an example for the first one

![first line image](includes/one.png)

Hence, each of these are decoded and then the final flag is reached.
