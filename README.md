# items-parser
`items-parser` is a CS2/CS:GO `items_game.txt` file parser. The script extracts game's items, such as weapon skins, gloves, keychains or stickers to a JSON file. While this repository includes pre-generated output, you can run the script yourself if you need to parse a different version of the files or want the absolute latest data before this repository is updated.

## Parsed Items
- Medals
- Agents (CT/T)
- Gloves (grouped by base type with paint kits)
- Containers (cases, sticker capsules, graffiti boxes)
- Passes
- Weapon skins (grouped by weapon type)
- Stickers
- Patches
- Keychains
- Music kits

## Requirements
- Python 3.3 or newer
- [Source2Viewer](https://valveresourceformat.github.io/) (a tool used for exploring Valve's VPK files)
- Python modules:
  - `vdf`

## Usage
> [!IMPORTANT]  
> **Make sure to convert all `.txt` files to UTF-8 encoding!**

### Preparing `items_game.txt` File
- **CS2:** To get CS2's `items_game.txt` file, use [Source2Viewer](https://valveresourceformat.github.io/). Open **Expand** tab. Expand **Counter-Strike 2** and open `game/csgo/pak01_dir.vpk`. Navigate to `scripts/items/` and you should be able to see `items_game.txt` file. Right-click it and select **Export as is**. Export the file to the `items/` folder within this project as (for example) `cs2.txt`.
- **CS:GO:** Right-click on CS:GO, hover over **Manage** and click on **Browse local files**. Navigate to `csgo/scripts/items/` and you should be able to see `items_game.txt`. Copy the file to the `items/` folder within this project as (for example) `csgo.txt`.

### Changing the Language
- **CS2:** To get CS2's language file, use [Source2Viewer](https://valveresourceformat.github.io/). Open **Expand** tab. Expand **Counter-Strike 2** and open `game/csgo/pak01_dir.vpk`. Navigate to `resource/` and you should be able to see `csgo_<LANGUAGE>.txt` files. Right-click the one you want to use and select **Export as is**. Export the file to the `lang/` folder within this project as (for example) `cs2.txt`.
- **CS:GO:** Right-click on CS:GO, hover over **Manage** and click on **Browse local files**. Navigate to `csgo/resource/` and you should be able to see `csgo_<LANGUAGE>.txt`. Copy the file to the `lang/` folder within this project as (for example) `csgo.txt`.

### Getting the Output
Output gets written to the `output/` folder.

1. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the Parser:**
    ```bash
    python main.py
    ```

## To-Do
- [x] Improve parsing gloves.
- [x] Parse music kits.
- [ ] Save output as SQL, VDF.
