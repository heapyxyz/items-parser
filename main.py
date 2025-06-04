import parser
import os

if __name__ == "__main__":
    print("CS2/CS:GO Items Parser")
    print("GitHub: @ClutchCommunity")

    for file in os.listdir("items"):
        if not file.endswith(".txt"):
            continue

        filename = file.split(".")[0]

        if not os.path.exists(f"lang/{filename}.txt"):
            print(f'Missing "lang/{filename}.txt"!')

        items = parser.Items(filename)
