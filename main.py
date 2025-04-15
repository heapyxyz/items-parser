import parser

if __name__ == "__main__":
    print("CS2/CS:GO Items Parser")
    print("GitHub: @ClutchCommunity")

    cs2_lang = parser.CS2Lang()
    cs2_items = parser.CS2Items(cs2_lang)

    csgo_lang = parser.CSGOLang()
    csgo_items = parser.CSGOItems(csgo_lang)