import re
from pathlib import Path

from itemParser import Item

_COLOR_CODE = re.compile(r'\^[0-9a-fA-F]{6}')
_SEPARATOR  = '_______________________'


def _strip_color_codes(text: str) -> str:
    return _COLOR_CODE.sub('', text)


def write_items(items: list[Item], path: str | Path) -> None:
    lines = (f"{item.id}#{item.name}#" for item in items)
    Path(path).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"✓ {len(items)} items  →  {path}")


def write_descriptions(items: list[Item], path: str | Path) -> None:
    blocks = []
    for item in items:
        if not item.description:
            continue

        lines = []
        for line in item.description:
            clean = _strip_color_codes(line)
            lines.append('--------------------------' if clean.startswith('___') else clean)

        blocks.append(f"{item.id}#\n" + '\n'.join(lines) + "\n#")

    Path(path).write_text('\n'.join(blocks) + '\n', encoding='utf-8')
    print(f"✓ {len(blocks)} descriptions  →  {path}")


def write_slot_count(items: list[Item], path: str | Path) -> None:
    slotted = [item for item in items if item.slot_count > 0]
    lines   = (f"{item.id}#{item.slot_count}#" for item in slotted)
    Path(path).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"✓ {len(slotted)} slotted items  →  {path}")

def write_skills_sp(skills: list, path: str | Path) -> None:
    blocks = []
    for handle, sp_values in skills:
        lines = [f"{handle}#"] + [f"{v}#" for v in sp_values] + ["@"]
        blocks.append('\n'.join(lines))
    Path(path).write_text('\n'.join(blocks) + '\n', encoding='utf-8')
    print(f"✓ {len(blocks)} skills  →  {path}")