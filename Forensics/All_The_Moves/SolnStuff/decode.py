import chess

with open("./stuff.txt", "r") as f:
    for i in f:
        board = chess.Board(i)
        print(board)
