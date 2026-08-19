import parser
import os

if __name__ == "__main__":
    print("CS2/CS:GO Items Parser")
    print("https://github.com/heapyxyz/items-parser")

    for file in os.listdir(os.getcwd() + "/parser/items"):
        if not file.endswith(".txt"):
            continue

        filename = file.split(".")[0]

        if not os.path.exists(os.getcwd() + f"/parser/lang/{filename}.txt"):
            print(f'Missing "parser/lang/{filename}.txt"!')
            continue

        items = parser.Items(filename)
