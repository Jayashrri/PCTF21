from hashlib import md5

def play(keywords: list) -> None:
    print("Here, have some toys:")
    for keyword in keywords:
        print(md5(keyword.encode()).digest().hex())
