#!/usr/bin/env python3
"""
main.py — Generates OpenKore table files from RO client data files

Usage:
    python main.py --items
    python main.py --descriptions
    python main.py --slots
    python main.py --skillssp
    python main.py --items --descriptions --slots --skillssp
    python main.py --items --iteminput "C:/Ragnarok/System/iteminfo.lub"
    python main.py --skillssp --skillinput "C:/Ragnarok/data/luafiles514/lua files/skillinfoz/skillinfolist.lub"

Flags:
    --iteminput  / -i   Path to iteminfo.lub        (default: C:/Ragnarok/System/iteminfo.lub)
    --skillinput / -si  Path to skillinfolist.lub   (default: data/luafiles514/lua files/skillinfoz/skillinfolist.lub)
    --items      / -n   Generate items.txt
    --descriptions / -d   Generate itemsdescriptions.txt
    --slots      / -s   Generate itemslotcounttable.txt
    --skillssp   / -sp  Generate skillssp.txt
"""

import argparse
from pathlib import Path

from itemParser  import ItemInfoParser
from skillParser import SkillInfoParser
from writers     import write_items, write_descriptions, write_slot_count, write_skills_sp

DEFAULT_ITEM_INPUT  = Path('C:/Ragnarok/System/iteminfo.lub')
DEFAULT_SKILL_INPUT = Path('data/luafiles514/lua files/skillinfoz/skillinfolist.lub')


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--iteminput',    '-i',  type=Path, default=Path('iteminfo.lub'))
    p.add_argument('--skillinput',   '-si', type=Path, default=Path('skillinfolist.lub'))
    p.add_argument('--items',        '-n',  action='store_true', help='Generate items.txt')
    p.add_argument('--descriptions', '-d',  action='store_true', help='Generate itemsdescriptions.txt')
    p.add_argument('--slots',        '-s',  action='store_true', help='Generate itemslotcounttable.txt')
    p.add_argument('--skillssp',     '-sp', action='store_true', help='Generate skillssp.txt')
    return p.parse_args()


def resolve(path: Path, default: Path) -> Path:
    if path.exists():
        return path
    if default.exists():
        print(f"Using default: {default}")
        return default
    raise FileNotFoundError(f"File not found: {path}\nUse the appropriate --input flag to specify the correct path.")


def main():
    args = parse_args()

    if not any([args.items, args.descriptions, args.slots, args.skillssp]):
        print("Nothing to do. Use --items, --descriptions, --slots, --skillssp, or any combination.")
        return

    if any([args.items, args.descriptions, args.slots]):
        items = ItemInfoParser(resolve(args.iteminput, DEFAULT_ITEM_INPUT)).parse()
        print(f"Parsed {len(items)} items from {args.iteminput.name}")

        if args.items:
            write_items(items, 'items.txt')
        if args.descriptions:
            write_descriptions(items, 'itemsdescriptions.txt')
        if args.slots:
            write_slot_count(items, 'itemslotcounttable.txt')

    if args.skillssp:
        skills = SkillInfoParser(resolve(args.skillinput, DEFAULT_SKILL_INPUT)).parse()
        print(f"Parsed {len(skills)} skills from {args.skillinput.name}")
        write_skills_sp(skills, 'skillssp.txt')


if __name__ == '__main__':
    main()