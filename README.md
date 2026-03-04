# tableKore Extractor

> Generate [OpenKore](https://github.com/OpenKore/openkore) table files directly from your Ragnarok Online client — always in sync, never outdated.

---

Ragnarok Online servers constantly add new items, update names, and expand their item pool. Maintaining `items.txt`, `itemsdescriptions.txt` and other table files by hand is tedious and error-prone. **tableKore Extractor** automates this entirely: it reads data files straight from your RO client and generates ready-to-use OpenKore table files in seconds.

No more copy-pasting. No more "Unknown Item (12345)". Every update, just run one command.

---

## What it generates

| File                     | Description                                       |
| ------------------------ | ------------------------------------------------- |
| `items.txt`              | Item IDs and display names in OpenKore format     |
| `itemsdescriptions.txt`  | Full item descriptions, clean and color-code-free |
| `itemslotcounttable.txt` | Number of card slots per equippable item          |

---

## Requirements

- Python 3.10+
- `iteminfo.lub` from your RO client's GRF or `System/` folder

---

## Usage

```bash
# Generate all files at once (recommended)
python main.py --items --descriptions --slots

# Generate only items.txt
python main.py --items

# Generate only itemsdescriptions.txt
python main.py --descriptions

# Generate only itemslotcounttable.txt
python main.py --slots

# Specify a custom path to iteminfo.lub
python main.py --items --descriptions --slots --input "C:/Ragnarok/System/iteminfo.lub"
```

The generated files will appear in the same directory. Copy them to your OpenKore `tables/<server>/` folder.

---

## How it works

RO clients store item data in a Lua file called `iteminfo.lub` inside the GRF or in the `System/` folder. This file contains the names and descriptions that the **client itself uses** — meaning it's always accurate, always up to date, and always in the language your server runs.

**tableKore Extractor** parses this file, extracts the `identifiedDisplayName` and `identifiedDescriptionName` for each item, strips RO color codes (like `^0000FF` and `^000000`) from descriptions, and writes clean output files ready to drop into OpenKore.

```
iteminfo.lub  →  parser.py  →  writers.py  →  items.txt
                                           →  itemsdescriptions.txt
                                           →  itemslotcounttable.txt
```

---

## Getting itemslots.txt from the GRF

The `itemslots.txt` file — which tells OpenKore which equipment slot each item occupies (weapon, armor, headgear, etc.) — cannot be generated from `iteminfo.lub`. This data lives server-side and is not exposed to the client.

However, most RO clients ship a file called `data/itemslottable.txt` inside their GRF that contains exactly this information. To extract it:

1. Open **GRF Editor** and load your client's `data.grf`
2. Search for `data/itemslottable.txt`
3. Right-click → **Extract**
4. Rename the extracted file to `itemslots.txt`
5. Copy it to `tables/<server>/` in your OpenKore installation

This file already uses the same `ID#value#` format as OpenKore, so no conversion is needed.

---

## Getting maps.txt from the GRF

The `maps.txt` file — which maps internal map filenames to their display names — can be extracted directly from the GRF as well. Look for `data/mapnametable.txt` inside your client's GRF:

1. Open **GRF Editor** and load your client's GRF (check additional GRFs too, as some servers ship an updated version in a separate patch file)
2. Search for `data/mapnametable.txt`
3. Right-click → **Extract**
4. Rename the extracted file to `maps.txt`
5. Copy it to `tables/<server>/` in your OpenKore installation

The file uses the format `mapname.rsw#Display Name#` per line, which OpenKore reads directly. Comments (lines starting with `//`) and blank lines are ignored automatically.

---

## Project structure

```
tableKore Extractor/
├── main.py      # CLI entry point — run this
├── parser.py    # Reads iteminfo.lub, returns Item dataclasses
└── writers.py   # Writes items.txt, itemsdescriptions.txt and itemslotcounttable.txt
```

Each file has a single responsibility and can be imported independently if you want to integrate the parser into a larger project.

---

## After a server update

1. Open GRF Editor (or your preferred extractor)
2. Locate `System/iteminfo.lub` in your client folder
3. Run `python main.py --items --descriptions --slots`
4. Copy the output files to `tables/<server>/` in your OpenKore installation

That's it.

---

## Contributing

Contributions are welcome! Some ideas if you want to help:

- **Support for other servers** — the parser works with any server that uses the standard `iteminfo.lub` format. If yours uses a different structure, open an issue with a sample and we'll add support.
- **Monster and map table generators** — the same approach applies to `monsterinfo.lub`, `accessoryid.lub`, and others.
- **Output format options** — some OpenKore forks use slightly different table formats.
- **Tests** — unit tests for the parser and writers would be a great addition.

To contribute, fork the repo, make your changes, and open a pull request. Keep the code clean, single-responsibility, and consistent with the existing style.

---

## License

[MIT](LICENSE) — do whatever you want with it.
