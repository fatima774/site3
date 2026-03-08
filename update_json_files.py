#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from bs4 import BeautifulSoup
import re
import shutil
from datetime import datetime

project_dir = Path(__file__).parent
lang_dir = project_dir / "assets" / "lang"

# Charger les nouveaux mappings
with open(project_dir / "mapping_report.json", "r", encoding="utf-8") as f:
    report = json.load(f)

new_keys = report["new_keys"]

# Charger les JSON existants
with open(lang_dir / "fr.json", "r", encoding="utf-8") as f:
    fr_data = json.load(f)

with open(lang_dir / "en.json", "r", encoding="utf-8") as f:
    en_data = json.load(f)

with open(lang_dir / "es.json", "r", encoding="utf-8") as f:
    es_data = json.load(f)

print("="*70)
print("ADDING NEW KEYS TO fr.json")
print("="*70 + "\n")

# Ajouter les nouvelles clés à fr.json
added_count = 0
for key, value in new_keys.items():
    if key not in fr_data:
        fr_data[key] = value
        en_data[key] = value  # Placeholder pour l'anglais
        es_data[key] = value  # Placeholder pour l'espagnol
        added_count += 1
        print(f"[+] {key}")

print(f"\nTotal keys added: {added_count}")

# Sauvegarder les fichiers JSON mis à jour
print("\nSaving JSON files...")
with open(lang_dir / "fr.json", "w", encoding="utf-8") as f:
    json.dump(fr_data, f, ensure_ascii=False, indent=2)
print("  fr.json saved")

with open(lang_dir / "en.json", "w", encoding="utf-8") as f:
    json.dump(en_data, f, ensure_ascii=False, indent=2)
print("  en.json saved")

with open(lang_dir / "es.json", "w", encoding="utf-8") as f:
    json.dump(es_data, f, ensure_ascii=False, indent=2)
print("  es.json saved")

print("\n" + "="*70)
print("COMPLETE: New keys added to all language files")
print("="*70)
