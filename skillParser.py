import re
from pathlib import Path


class SkillInfoParser:
    _BLOCK    = re.compile(r'\[SKID\.(\w+)\]\s*=\s*\{(.*?)\n\t\}', re.DOTALL)
    _SPAMOUNT = re.compile(r'SpAmount\s*=\s*\{([^}]*)\}')

    def __init__(self, path: str | Path):
        self._text = Path(path).read_text(encoding='utf-8', errors='replace')

    def parse(self) -> list[tuple[str, list[int]]]:
        skills = []
        for m in self._BLOCK.finditer(self._text):
            handle   = m.group(1)
            sp_match = self._SPAMOUNT.search(m.group(2))
            if not sp_match:
                continue
            values = [int(v.strip()) for v in sp_match.group(1).split(',')
                      if v.strip().lstrip('-').isdigit()]
            # Skip NPC/mob skills where all SP values are 0
            if not values or all(v == 0 for v in values):
                continue
            skills.append((handle, values))
        return skills