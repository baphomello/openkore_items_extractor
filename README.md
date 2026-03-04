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

**tableKore Extractor** parses these files, strips RO color codes (like `^0000FF` and `^000000`) from descriptions, and writes clean output files ready to drop into OpenKore.

```
iteminfo.lub      →  itemParser.py  →  writers.py  →  items.txt
                                                    →  itemsdescriptions.txt
                                                    →  itemslotcounttable.txt

skillinfolist.lub →  skillParser.py →  writers.py  →  skillssp.txt
```

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
tableKore_extractor/
├── main.py          # CLI entry point — run this
├── itemParser.py    # Reads iteminfo.lub, returns Item dataclasses
├── skillParser.py   # Reads skillinfolist.lub, returns skill SP data
└── writers.py       # Writes all output table files
```

Each file has a single responsibility and can be imported independently if you want to integrate the parsers into a larger project.

---

## After a server update

1. Open GRF Editor (or your preferred extractor)
2. Locate `System/iteminfo.lub` and `data/.../skillinfolist.lub` in your client
3. Run `python main.py --items --descriptions --slots --skillssp`
4. Extract `itemslottable.txt`, `mapnametable.txt` and `resnametable.txt` from the GRF and rename/merge as needed
5. Copy all output files to `tables/<server>/` in your OpenKore installation

That's it.

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
