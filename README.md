# koreExtractor

> Generate [OpenKore](https://github.com/OpenKore/openkore) table files directly from your Ragnarok Online client — always in sync, never outdated.

---

Ragnarok Online servers constantly add new items, update names, and expand their item pool. Maintaining `items.txt`, `itemsdescriptions.txt` and other table files by hand is tedious and error-prone. **koreExtractor** automates this entirely: it reads data files straight from your RO client and generates ready-to-use OpenKore table files in seconds.

No more copy-pasting. No more "Unknown Item (12345)". Every update, just run one command.

---

## What it generates

| File                     | Description                                       |
| ------------------------ | ------------------------------------------------- |
| `items.txt`              | Item IDs and display names in OpenKore format     |
| `itemsdescriptions.txt`  | Full item descriptions, clean and color-code-free |
| `itemslotcounttable.txt` | Number of card slots per equippable item          |
| `skillssp.txt`           | SP cost per skill level                           |

---

## Requirements

- Python 3.10+
- `iteminfo.lub` from your RO client's GRF or `System/` folder
- `skillinfolist.lub` from `data/luafiles514/lua files/skillinfoz/` inside the GRF

---

## Usage

```bash
# Generate all item-related files at once
python main.py --items --descriptions --slots

# Generate skillssp.txt
python main.py --skillssp

# Generate everything
python main.py --items --descriptions --slots --skillssp

# Specify custom input paths
python main.py --items --descriptions --slots --iteminput "C:/Ragnarok/System/iteminfo.lub"
python main.py --skillssp --skillinput "C:/Ragnarok/data/luafiles514/lua files/skillinfoz/skillinfolist.lub"
```

The generated files will appear in the same directory. Copy them to your OpenKore `tables/<server>/` folder.

### All flags

| Flag             | Short | Description                       | Default                           |
| ---------------- | ----- | --------------------------------- | --------------------------------- |
| `--iteminput`    | `-i`  | Path to `iteminfo.lub`            | `C:/Ragnarok/System/iteminfo.lub` |
| `--skillinput`   | `-si` | Path to `skillinfolist.lub`       | `data/.../skillinfolist.lub`      |
| `--items`        | `-n`  | Generate `items.txt`              |                                   |
| `--descriptions` | `-d`  | Generate `itemsdescriptions.txt`  |                                   |
| `--slots`        | `-s`  | Generate `itemslotcounttable.txt` |                                   |
| `--skillssp`     | `-sp` | Generate `skillssp.txt`           |                                   |

---

## How it works

RO clients store item and skill data in Lua files inside the GRF or in the `System/` folder. These files contain the exact data the **client itself uses** — meaning they're always accurate, always up to date, and always in the language your server runs.

**koreExtractor** parses these files, strips RO color codes (like `^0000FF` and `^000000`) from descriptions, and writes clean output files ready to drop into OpenKore.

```
iteminfo.lub      →  itemParser.py  →  writers.py  →  items.txt
                                                    →  itemsdescriptions.txt
                                                    →  itemslotcounttable.txt

skillinfolist.lub →  skillParser.py →  writers.py  →  skillssp.txt
```

---

## Fixing unidentified item names

Private servers often introduce new items before their client data is fully populated. When that happens, `iteminfo.lub` only has a generic placeholder like "Unidentified Weapon" or "Unidentified Armor" instead of the real name — which means OpenKore can't identify those items correctly.

`fixUnidentified.py` exists to bridge that gap. It compares your server's `items.txt` against a reference file from another server (such as iRO) and replaces every placeholder name with the proper one wherever a match is found. Items that are truly exclusive to your server and unknown to the reference are left untouched.

This is not a one-time task. As servers add new items weekly, running `fixUnidentified.py` after each `main.py` run is part of the regular maintenance workflow for keeping OpenKore tables accurate.

```bash
python fixUnidentified.py --source items_myserver.txt --reference items_iRO.txt --output items.txt
```

| Flag       | Description                      | Default          |
| ---------- | -------------------------------- | ---------------- |
| `--laro`   | Your server's `items.txt`        | `items_laRO.txt` |
| `--iro`    | Reference `items.txt` (e.g. iRO) | `items_iRO.txt`  |
| `--output` | Fixed output file                | `items.txt`      |

---

## Getting files from the GRF

Some table files cannot be generated from Lua sources — their data is stored directly inside the client's GRF and can be extracted as-is, with no conversion needed. Use **GRF Editor** to open each `.grf` file and extract them.

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
koreExtractor/
├── main.py              # CLI entry point — run this
├── itemParser.py        # Reads iteminfo.lub, returns Item dataclasses
├── skillParser.py       # Reads skillinfolist.lub, returns skill SP data
├── writers.py           # Writes all output table files
└── fixUnidentified.py   # Weekly maintenance: patches items.txt using a reference server
```

Each file has a single responsibility and can be imported independently if you want to integrate the parsers into a larger project.

---

## Weekly maintenance workflow

After each server update that adds new items:

1. Extract the latest `iteminfo.lub` from your client's GRF or `System/` folder
2. Run `python main.py --items --descriptions --slots --skillssp`
3. Run `python fixUnidentified.py --source items_myserver.txt --reference items_iRO.txt --output items.txt`
4. Copy the output files to `tables/<server>/` in your OpenKore installation

---

## Contributing

Contributions are welcome! Some ideas if you want to help:

- **Support for other servers** — the parsers work with any server that uses the standard `iteminfo.lub` and `skillinfolist.lub` formats. If yours uses a different structure, open an issue with a sample and we'll add support.
- **More table generators** — the same approach applies to `monsterinfo.lub`, `accessoryid.lub`, and others.
- **Output format options** — some OpenKore forks use slightly different table formats.
- **Tests** — unit tests for the parsers and writers would be a great addition.

To contribute, fork the repo, make your changes, and open a pull request. Keep the code clean, single-responsibility, and consistent with the existing style.

---

## License

[MIT](LICENSE) — do whatever you want with it.
