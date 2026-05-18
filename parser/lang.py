import os, vdf


class Lang:
    def __init__(self, name: str):
        print(f'Parsing "{name}" language file...')

        file = os.getcwd() + f"/lang/{name}.txt"
        with open(file, "r", encoding="utf-8") as f:
            data = f.read()

        vdf_data = vdf.loads(data)
        self._data = {k.lower(): v for k, v in vdf_data["lang"]["Tokens"].items()}

    def get(self, key: str):
        key = key.replace("#", "")
        return self._data.get(key.lower())
