import os, vdf


class Lang:
    def __init__(self, name: str):
        print(f'Parsing "{name}" language file...')

        self._file = os.getcwd() + f"/lang/{name}.txt"
        self._data = self._parse()

    def _parse(self):
        with open(self._file, "r") as f:
            data = f.read()

        return vdf.loads(data)

    def get(self, key: str):
        key = key.replace("#", "")
        data = self._data["lang"]["Tokens"]

        for data_key, data_value in data.items():
            if str(data_key).lower() == key.lower():
                return data_value

        return None
