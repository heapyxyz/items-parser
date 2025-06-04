# items-parser
`items-parser` is a CS2/CS:GO `items_game.txt` file parser. The script extracts game's information, such as weapon skins, gloves, keychains, or stickers to a JSON file. While this repository includes pre-generated output, you can run the script yourself if you need to parse a different version of the files or want the absolute latest data before this repository is updated.

## Prerequisites
- Python 3.3 or newer
- [Source2Viewer](https://valveresourceformat.github.io/) (a tool for exploring Valve's VPK archives)
- Python modules:
  - `vdf`

## Usage
### Preparing `items_game.txt` File
- **CS2:** To get CS2's `items_game.txt` file, use [Source2Viewer](https://valveresourceformat.github.io/). Expand "[730] Counter-Strike 2 ..." and open `game/csgo/pak01_dir.vpk`. Navigate to `scripts/items` and you should be able to see `items_game.txt` file. Right-click it and select "Export as is" to the `items/` folder within this project. Rename the exported file to (for example) `cs2.txt`.
- **CS:GO:** Install the `csgo_legacy` beta on Steam. Then, browse CS:GO's local files and copy `csgo/scripts/items/items_game.txt` to the `items/` folder within this project. Rename the copied file to (for example) `csgo.txt`.

### Changing the Language
- **CS2:** To get CS2's language file, use [Source2Viewer](https://valveresourceformat.github.io/). Expand "[730] Counter-Strike 2 ..." and open `game/csgo/pak01_dir.vpk`. Navigate to `resource` and you should be able to see `csgo_<LANGUAGE>.txt` files. Right-click the one you want to use and select "Export as is" to the `lang/` folder within this project. Rename the exported file to (for example) `cs2.txt`.
- **CS:GO:** Install the `csgo_legacy` beta on Steam. Then, browse CS:GO's local files and copy `csgo/resource/csgo_<LANGUAGE>.txt` to the `lang/` folder within this project. Rename the copied file to (for example) `csgo.txt`.

### Getting the Output
Output gets written to the `output/` folder.

1.  **Install Dependencies:**
    ```bash
    pip install vdf==3.4

    # Or, if you are in the project's root folder
    pip install -r requirements.txt
    ```

2.  **Run the Parser:**
    ```bash
    # Make sure you are in the project's root folder
    python main.py
    ```
