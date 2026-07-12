from pathlib import Path

p = Path("elosam/app.py")
s = p.read_text(encoding="utf-8")

replacements = {
    "Miss\u00c3\u00a3o": "Miss\u00e3o",
    "miss\u00c3\u00a3o": "miss\u00e3o",
    "Decis\u00c3\u00a3o": "Decis\u00e3o",
    "fam\u00c3\u00adlia": "fam\u00edlia",
    "Organiza\u00c3\u00a7\u00c3\u00b5es": "Organiza\u00e7\u00f5es",
    "ORGANIZA\u00c3\u0087\u00c3\u0095ES": "ORGANIZA\u00c7\u00d5ES",
    "\u00e2\u20ac\u201d": "\u2014",
    "\u00e2\u20ac\u201c": "\u2013",
}

for old, new in replacements.items():
    s = s.replace(old, new)

p.write_text(s, encoding="utf-8")

print("REPARO CONCLUIDO")
