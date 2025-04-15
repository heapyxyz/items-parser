import os, vdf

class Lang():
    def __init__(self, prefix: str):
        print(f"Loading {prefix.upper()} language file...")

        self._file = os.getcwd() + "/lang/" + prefix + "_lang.txt"
        self._data = self._parse()

    def _parse(self):
        with open(self._file, "r") as f:
            data = f.read()

        return vdf.loads(data)
    
    def get(self, key: str):
        key = key.replace("#", "")
        data = self._data["lang"]["Tokens"]

        for data_key, data_value in data.items():
            if data_key.lower() == key.lower():
                return data_value

        return None
    
class CS2Lang(Lang):
    def __init__(self):
        super().__init__("cs2")

class CSGOLang(Lang):
    def __init__(self):
        super().__init__("csgo")