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
python main.py --items --descriptions --slots --iteminput "C:/Ragnarok/System/iteminfo.lub"
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

## Getting files from the GRF

Some table files cannot be generated from `iteminfo.lub` — their data is stored directly inside the client's GRF and can be extracted as-is, with no conversion needed. Use **GRF Editor** to open each `.grf` file and extract them.

> **Tip:** Servers often ship multiple GRF files (e.g. `data.grf`, `patch.grf`). Always check all of them — patch GRFs load after `data.grf` and override its contents, so they tend to have the most up-to-date and server-specific data. If a file exists in both, prefer the one from the patch GRF.

| OpenKore file      | GRF path                 | Notes                                         |
| ------------------ | ------------------------ | --------------------------------------------- |
| `itemslots.txt`    | `data/itemslottable.txt` | Rename after extracting                       |
| `maps.txt`         | `data/mapnametable.txt`  | Rename after extracting                       |
| `resnametable.txt` | `data/resnametable.txt`  | Merge from all GRFs if found in more than one |

All three files use the same `value#value#` format that OpenKore reads directly. Comments (lines starting with `//`) and blank lines are ignored automatically.

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
4. Extract `itemslottable.txt`, `mapnametable.txt` and `resnametable.txt` from the GRF and rename/merge as needed
5. Copy all output files to `tables/<server>/` in your OpenKore installation

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
