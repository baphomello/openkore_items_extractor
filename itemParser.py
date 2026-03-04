import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Item:
    id:          int
    name:        str
    slot_count:  int       = 0
    description: list[str] = field(default_factory=list)


class ItemInfoParser:
    _BLOCK       = re.compile(r'\[(\d+)\]\s*=\s*\{')
    _NAME        = re.compile(r'identifiedDisplayName\s*=\s*"([^"]+)"')
    _SLOT        = re.compile(r'slotCount\s*=\s*(\d+)')
    _DESC_BLOCK  = re.compile(r'\bidentifiedDescriptionName\s*=\s*\{([^}]*)\}', re.DOTALL)
    _DESC_LINE   = re.compile(r'"([^"]*)"')

    def __init__(self, path: str | Path):
        self._text = Path(path).read_text(encoding='utf-8', errors='replace')

    def parse(self) -> list[Item]:
        blocks    = [(int(m.group(1)), m.start()) for m in self._BLOCK.finditer(self._text)]
        items     = []

        for i, (item_id, start) in enumerate(blocks):
            block = self._text[start: blocks[i + 1][1] if i + 1 < len(blocks) else None]

            name_match = self._NAME.search(block)
            if not name_match:
                continue

            desc_match = self._DESC_BLOCK.search(block)
            slot_match = self._SLOT.search(block)
            desc_lines = self._DESC_LINE.findall(desc_match.group(1)) if desc_match else []

            items.append(Item(
                id          = item_id,
                name        = name_match.group(1).strip(),
                slot_count  = int(slot_match.group(1)) if slot_match else 0,
                description = desc_lines,
            ))

        return items