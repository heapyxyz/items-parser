import json, os, vdf
from .lang import Lang, CS2Lang, CSGOLang

rarities = ["default", "common", "uncommon", "rare", "mythical", "legendary", "ancient", "immortal", "unusual"]

class Items():
    def __init__(self, lang: Lang, prefix: str):
        print(f"Loading {prefix.upper()} items file...")

        self._lang = lang
        self._file = os.getcwd() + "/items/" + prefix + "_items.txt"
        self._data = self._parse()

        print(f"Saving {prefix}_weapons.json...")
        self.weapons: dict = self._get_weapons()
        with open(os.getcwd() + f"/output/{prefix}_weapons.json", "w") as f:
            f.write(json.dumps(self.weapons, indent = 4))

        print(f"Saving {prefix}_kits.json...")
        self.paint_kits: dict = self._get_paint_kits()
        with open(os.getcwd() + f"/output/{prefix}_kits.json", "w") as f:
            f.write(json.dumps(self.paint_kits, indent = 4))

        print(f"Saving {prefix}_loot.json...")
        self.loot: dict = self._get_loot()
        with open(os.getcwd() + f"/output/{prefix}_loot.json", "w") as f:
            f.write(json.dumps(self.loot, indent = 4))

    def _parse(self):
        with open(self._file, "r") as f:
            data = f.read()

        return vdf.loads(data)
    
    def _get_weapons(self) -> dict:
        data = self._data["items_game"]["items"]
        weapons = {}

        for item in data:
            item_data = data[item]
            weapons[item_data["name"]] = item

        return weapons
    
    def _get_loot(self) -> dict:
        data = self._data["items_game"]["client_loot_lists"]
        loot_list = {}

        for loot in data:
            loot_split = loot.split("_")

            if not loot_split[-1] in rarities:
                continue

            for x in data[loot]:
                paint_kit_split = x.replace("[", "").split("]")

                if len(paint_kit_split) != 2:
                    continue

                paint_kit = paint_kit_split[0]
                item = paint_kit_split[1]

                if item not in loot_list:
                    loot_list[item] = {}

                if paint_kit in self.paint_kits:
                    loot_list[item][paint_kit] = self.paint_kits[paint_kit]

        return loot_list
    
    def _get_paint_kits(self) -> dict:
        data = self._data["items_game"]["paint_kits"]        
        kits = {}

        for kit in data:
            kit_data = data[kit]

            # Useless paint kit, for example "9001" -> "workshop_default"
            if not "description_string" in kit_data:
                continue

            paint_kit = {}
            paint_kit["index"] = kit
            paint_kit["tag"] = self._lang.get(kit_data["description_tag"])
            paint_kit["lowest_float"] = float(kit_data["wear_remap_min"] if "wear_remap_min" in kit_data else 0.0)
            paint_kit["highest_float"] = float(kit_data["wear_remap_max"] if "wear_remap_max" in kit_data else 1.0)

            kits[kit_data["name"]] = paint_kit

        return kits

class CS2Items(Items):
    def __init__(self, lang: CS2Lang):
        super().__init__(lang, "cs2")

class CSGOItems(Items):
    def __init__(self, lang: CSGOLang):
        super().__init__(lang, "csgo")