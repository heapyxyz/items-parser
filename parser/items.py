import json, os, vdf
from .lang import Lang, CS2Lang, CSGOLang

rarities = [
    "default",
    "common",
    "uncommon",
    "rare",
    "mythical",
    "legendary",
    "ancient",
    "immortal",
    "unusual",
]


class Items:
    def __init__(self, lang: Lang, prefix: str):
        print(f"Parsing {prefix.upper()} items file...")

        self._lang = lang
        self._file = os.getcwd() + f"/items/{prefix}_items.txt"
        self._data = self._parse()

        self._medals = {}
        self._agents = {"ct": {}, "t": {}}
        self._gloves = {}
        self._items = self._get_items()
        self._paint_kits = self._get_paint_kits()
        self._sticker_kits = self._get_sticker_kits()
        self._keychains = self._get_keychains()

        self._loot = self._get_loot()
        with open(os.getcwd() + f"/output/{prefix}.json", "w") as f:
            f.write(json.dumps(self._loot, indent=4))
            print(f"Saved to output/{prefix}.json")

    def _parse(self):
        with open(self._file, "r") as f:
            data = f.read()

        return vdf.loads(data)

    def _get_items(self) -> dict:
        if not "items" in self._data["items_game"]:
            return {}

        data = self._data["items_game"]["items"]
        items = {}

        for index in data:
            item_data = data[index]
            item_name = item_data["name"]
            items[item_name] = index

            if "item_name" in item_data:
                item_tag: str = item_data["item_name"]
                if item_tag.startswith("#CSGO_Collectible"):
                    medal = {
                        "index": index,
                        "tag": self._lang.get(item_tag),
                    }

                    self._medals[item_name] = medal

            if "prefab" in item_data:
                prefab: str = item_data["prefab"]
                if prefab == "customplayertradable":
                    agent = {
                        "index": index,
                        "tag": self._lang.get(item_tag),
                        "rarity": (
                            item_data["item_rarity"]
                            if "item_rarity" in item_data
                            else "default"
                        ),
                    }

                    agent_team = (
                        "ct"
                        if "counter-terrorists" in item_data["used_by_classes"]
                        else "t"
                    )
                    self._agents[agent_team][item_name] = agent

        return items

    def _get_paint_kits(self) -> dict:
        if not "paint_kits" in self._data["items_game"]:
            return {}

        if not "rarity_data" in self._data["items_game"]:
            return {}

        data = self._data["items_game"]["paint_kits"]
        rarity_data = self._data["items_game"]["paint_kits_rarity"]
        kits = {}

        for index in data:
            kit_data = data[index]
            kit_name = kit_data["name"]

            if not "description_string" in kit_data:
                continue

            if "vmt_path" in kit_data:
                # Not happy with how it works, will group by glove types later (Bloodhound, Specialist, etc.)
                paint_kit = {
                    "index": index,
                    "tag": self._lang.get(kit_data["description_tag"]),
                }

                self._gloves[kit_name] = paint_kit
            else:
                paint_kit = {
                    "index": index,
                    "tag": self._lang.get(kit_data["description_tag"]),
                    "lowest_float": float(
                        kit_data["wear_remap_min"]
                        if "wear_remap_min" in kit_data
                        else 0.0
                    ),
                    "highest_float": float(
                        kit_data["wear_remap_max"]
                        if "wear_remap_max" in kit_data
                        else 1.0
                    ),
                    "rarity": (
                        rarity_data[kit_name] if kit_name in rarity_data else "default"
                    ),
                }

                kits[kit_name] = paint_kit

        return kits

    def _get_sticker_kits(self) -> dict:
        if not "sticker_kits" in self._data["items_game"]:
            return {}

        data = self._data["items_game"]["sticker_kits"]
        stickers = {}

        for index in data:
            sticker_data = data[index]
            sticker_name = sticker_data["name"]

            sticker = {
                "index": index,
                "tag": self._lang.get(sticker_data["item_name"]),
                "rarity": (
                    sticker_data["item_rarity"]
                    if "item_rarity" in sticker_data
                    else "default"
                ),
            }

            stickers[sticker_name] = sticker

        return stickers

    def _get_keychains(self) -> dict:
        if not "keychain_definitions" in self._data["items_game"]:
            return {}

        data = self._data["items_game"]["keychain_definitions"]
        keychains = {}

        for index in data:
            keychain_data = data[index]
            keychain_name = keychain_data["name"]

            keychain = {
                "index": index,
                "tag": self._lang.get(keychain_data["loc_name"]),
                "rarity": keychain_data["item_rarity"],
            }

            keychains[keychain_name] = keychain

        return keychains

    def _get_loot(self) -> dict:
        if not "client_loot_lists" in self._data["items_game"]:
            return {}

        data = self._data["items_game"]["client_loot_lists"]
        loot_list = {
            "medals": self._medals,
            "agents": self._agents,
            "gloves": self._gloves,
            "skins": {},
            "stickers": {},
            "patches": {},
            "keychains": self._keychains,
        }

        for set in data:
            set_split = set.split("_")

            if not set_split[-1] in rarities:
                continue

            for loot in data[set]:
                loot_split = loot.replace("[", "").split("]")

                if len(loot_split) != 2:
                    continue

                kit: str = loot_split[0]
                type: str = loot_split[1]

                if not type in self._items:
                    continue

                if type.startswith("weapon_"):
                    if not type in loot_list["skins"]:
                        loot_list["skins"][type] = {}

                    loot_list["skins"][type][kit] = self._paint_kits[kit]
                elif type == "sticker":
                    loot_list["stickers"][kit] = self._sticker_kits[kit]
                elif type == "patch":
                    loot_list["patches"][kit] = self._sticker_kits[kit]

        return loot_list


class CS2Items(Items):
    def __init__(self, lang: CS2Lang):
        super().__init__(lang, "cs2")


class CSGOItems(Items):
    def __init__(self, lang: CSGOLang):
        super().__init__(lang, "csgo")
