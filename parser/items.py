import json, os, vdf
from .lang import Lang


class Items:
    def __init__(self, name: str):
        self._lang = Lang(name)

        print(f'Parsing "{name}" items file...')

        self._file = os.getcwd() + f"/items/{name}.txt"
        self._data = self._parse()

        self._rarities = self._get_rarities()
        self._medals = {}
        self._agents = {"ct": {}, "t": {}}
        self._gloves = {}
        self._glove_bases = {}
        self._containers = {}
        self._passes = {}
        self._items = self._get_items()
        self._paint_kits = self._get_paint_kits()
        self._sticker_kits = self._get_sticker_kits()
        self._keychains = self._get_keychains()
        self._music_kits = self._get_music_kits()

        self._loot = self._get_loot()
        with open(os.getcwd() + f"/output/{name}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(self._loot, indent=4))
            print(f"Saved to output/{name}.json")

    def _parse(self):
        with open(self._file, "r", encoding="utf-8") as f:
            data = f.read()

        return vdf.loads(data)

    def _get_rarities(self) -> list:
        # fallback in case someone gets rid off "rarities" key
        if "rarities" not in self._data["items_game"]:
            return [
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

        return list(self._data["items_game"]["rarities"].keys())

    def _get_items(self) -> dict:
        if "items" not in self._data["items_game"]:
            return {}

        data = self._data["items_game"]["items"]
        items = {}

        for index in data:
            item_data = data[index]
            item_name = item_data["name"]
            items[item_name] = index

            if "item_name" not in item_data:
                continue

            item_tag: str = item_data["item_name"]
            if item_tag.startswith(("#CSGO_Collectible", "#CSGO_TournamentJournal")):
                medal = {
                    "index": index,
                    "tag": self._lang.get(item_tag),
                }

                self._medals[item_name] = medal

            if "prefab" not in item_data:
                continue

            prefab = item_data["prefab"]
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
            elif "season_pass" in prefab:
                ticket = {
                    "index": index,
                    "tag": self._lang.get(item_tag),
                }

                self._passes[item_name] = ticket
            elif prefab in [
                "weapon_case",
                "weapon_case_base",
                "weapon_case_souvenirpkg",
                "weapon_case_selfopening_collection",
                "sticker_capsule",
                "patch_capsule",
                "graffiti_box",
            ]:
                container = {
                    "index": index,
                    "tag": self._lang.get(item_tag),
                    "type": {
                        "weapon_case": "case",
                        "weapon_case_base": "capsule",
                        "weapon_case_souvenirpkg": "souvenir",
                        "weapon_case_selfopening_collection": "collection",
                        "sticker_capsule": "sticker",
                        "patch_capsule": "patch",
                        "graffiti_box": "graffiti",
                    }.get(prefab, "case"),
                }

                if "associated_items" in item_data:
                    container["key"] = next(iter(item_data["associated_items"]))

                self._containers[item_name] = container
            elif prefab == "hands_paintable":
                glove_base = {
                    "index": index,
                    "tag": self._lang.get(item_tag),
                }

                self._glove_bases[item_name] = glove_base

        return items

    def _get_paint_kits(self) -> dict:
        if "paint_kits" not in self._data["items_game"]:
            return {}

        if "paint_kits_rarity" not in self._data["items_game"]:
            return {}

        data = self._data["items_game"]["paint_kits"]
        rarity_data = self._data["items_game"]["paint_kits_rarity"]
        kits = {}

        for index in data:
            kit_data = data[index]
            kit_name = kit_data["name"]

            if "description_string" not in kit_data:
                continue

            is_glove = "vmt_path" in kit_data or kit_data.get(
                "composite_material_path", ""
            ).startswith("gloves/paints/")

            if is_glove:
                paint_kit = {
                    "index": index,
                    "tag": self._lang.get(kit_data["description_tag"]),
                    "rarity": (
                        rarity_data[kit_name] if kit_name in rarity_data else "default"
                    ),
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
        if "sticker_kits" not in self._data["items_game"]:
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
        if "keychain_definitions" not in self._data["items_game"]:
            return {}

        data = self._data["items_game"]["keychain_definitions"]
        keychains = {}
        name_to_rarity = {}

        for index in data:
            keychain_data = data[index]
            keychain_name = keychain_data["name"]

            if "item_rarity" in keychain_data:
                rarity = keychain_data["item_rarity"]
                name_to_rarity[keychain_name] = rarity
            elif "base" in keychain_data:
                rarity = name_to_rarity.get(keychain_data["base"], "default")
            else:
                rarity = "default"

            keychain = {
                "index": index,
                "tag": self._lang.get(keychain_data["loc_name"]),
                "rarity": rarity,
            }

            keychains[keychain_name] = keychain

        return keychains

    def _map_glove_base(self, kit_name: str) -> str:
        if kit_name.startswith("glove_driver_"):
            return "slick_gloves"

        if kit_name.startswith("glove_sport_"):
            return "sporty_gloves"

        if kit_name.startswith("glove_specialist_"):
            return "specialist_gloves"

        if kit_name.startswith("bloodhound_hydra_"):
            return "studded_hydra_gloves"

        if kit_name.startswith("bloodhound_"):
            return "studded_bloodhound_gloves"

        if kit_name.startswith("slick_"):
            return "slick_gloves"

        if kit_name.startswith("sporty_"):
            return "sporty_gloves"

        if kit_name.startswith("handwrap_"):
            return "leather_handwraps"

        if kit_name.startswith("motorcycle_"):
            return "motorcycle_gloves"

        if kit_name.startswith("specialist_"):
            return "specialist_gloves"

        if kit_name.startswith("operation10_"):
            return "studded_brokenfang_gloves"

        return ""

    def _get_gloves(self) -> dict:
        gloves = {}

        for base_name, base_data in self._glove_bases.items():
            gloves[base_name] = {
                "index": base_data["index"],
                "tag": base_data["tag"],
                "paint_kits": {},
            }

        for kit_name, kit_data in self._gloves.items():
            base_name = self._map_glove_base(kit_name)

            if not base_name or base_name not in gloves:
                continue

            gloves[base_name]["paint_kits"][kit_name] = kit_data

        return gloves

    def _get_music_kits(self) -> dict:
        if "music_definitions" not in self._data["items_game"]:
            return {}

        data = self._data["items_game"]["music_definitions"]
        kits = {}

        for index in data:
            kit_data = data[index]
            kit_name = kit_data["name"]

            kit = {
                "index": index,
                "tag": self._lang.get(kit_data["loc_name"]),
            }

            kits[kit_name] = kit

        return kits

    def _get_loot(self) -> dict:
        if "client_loot_lists" not in self._data["items_game"]:
            return {}

        data = self._data["items_game"]["client_loot_lists"]
        loot_list = {
            "medals": self._medals,
            "agents": self._agents,
            "gloves": self._get_gloves(),
            "containers": self._containers,
            "passes": self._passes,
            "skins": {},
            "stickers": {},
            "patches": {},
            "keychains": self._keychains,
            "music_kits": {},
        }

        for set in data:
            set_split = set.split("_")

            for loot in data[set]:
                if type(loot) != str:
                    continue

                loot_split = loot.replace("[", "").split("]")

                if len(loot_split) != 2:
                    continue

                kit = loot_split[0]
                loot_type = loot_split[1]

                if loot_type == "musickit":
                    if kit in self._music_kits:
                        loot_list["music_kits"][kit] = self._music_kits[kit]

                    continue

                if set_split[-1] not in self._rarities:
                    continue

                if loot_type not in self._items:
                    continue

                if loot_type.startswith("weapon_"):
                    if loot_type not in loot_list["skins"]:
                        loot_list["skins"][loot_type] = {}

                    loot_list["skins"][loot_type][kit] = self._paint_kits[kit]
                elif loot_type == "sticker":
                    loot_list["stickers"][kit] = self._sticker_kits[kit]
                elif loot_type == "patch":
                    loot_list["patches"][kit] = self._sticker_kits[kit]

        return loot_list
