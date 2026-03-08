#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from bs4 import BeautifulSoup
import re

project_dir = Path(__file__).parent
lang_dir = project_dir / "assets" / "lang"

print("="*70)
print("COMPREHENSIVE SITE TEXT EXTRACTION & ANALYSIS")
print("="*70 + "\n")

# Charger les JSON existants
with open(lang_dir / "fr.json", "r", encoding="utf-8") as f:
    fr_data = json.load(f)

with open(lang_dir / "en.json", "r", encoding="utf-8") as f:
    en_data = json.load(f)

with open(lang_dir / "es.json", "r", encoding="utf-8") as f:
    es_data = json.load(f)

fr_keys = set(fr_data.keys())
en_keys = set(en_data.keys())
es_keys = set(es_data.keys())

print("CURRENT JSON STATE:")
print(f"  fr.json: {len(fr_keys)} keys")
print(f"  en.json: {len(en_keys)} keys")
print(f"  es.json: {len(es_keys)} keys")
print(f"  Keys in en/es but NOT in fr: {len((en_keys | es_keys) - fr_keys)}")
print()

# Extra keys not in French
extra_in_en_es = (en_keys | es_keys) - fr_keys
if extra_in_en_es:
    print("EXTRA KEYS IN en.json/es.json (not in fr.json):")
    for key in sorted(list(extra_in_en_es)[:20]):
        en_val = en_data.get(key, "N/A")
        es_val = es_data.get(key, "N/A")
        print(f"  {key}")
        print(f"    EN: {en_val[:60] if en_val != 'N/A' else 'N/A'}")
        print(f"    ES: {es_val[:60] if es_val != 'N/A' else 'N/A'}")
    if len(extra_in_en_es) > 20:
        print(f"  ... and {len(extra_in_en_es) - 20} more")
print()

# Extract all HTML text elements
print("SCANNING HTML FILES FOR TEXTS:")
print("-" * 70)

html_files = sorted(project_dir.glob('*.html'))
all_texts = {}

for html_file in html_files:
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all data-i18n elements
    i18n_elements = soup.find_all(attrs={"data-i18n": True})
    
    texts_in_file = {}
    for el in i18n_elements:
        key = el.get('data-i18n')
        text = el.get_text(strip=True)
        
        # Store the text
        if key and text:
            texts_in_file[key] = text
            if key not in all_texts:
                all_texts[key] = text
    
    print(f"  {html_file.name:25} | {len(texts_in_file)} data-i18n elements")

print()
print("="*70)
print(f"TOTAL UNIQUE i18n KEYS IN HTML: {len(all_texts)}")
print()

# Compare with fr.json
missing_in_fr = set(all_texts.keys()) - fr_keys
extra_in_fr = fr_keys - set(all_texts.keys())

print(f"KEYS IN HTML but NOT IN fr.json: {len(missing_in_fr)}")
if missing_in_fr:
    for key in sorted(list(missing_in_fr)[:10]):
        print(f"  ⚠️  {key}: \"{all_texts[key][:50]}\"")
    if len(missing_in_fr) > 10:
        print(f"  ... and {len(missing_in_fr) - 10} more")

print()
print(f"KEYS IN fr.json but NOT IN HTML: {len(extra_in_fr)}")
if extra_in_fr:
    for key in sorted(list(extra_in_fr)[:10]):
        val = fr_data[key]
        print(f"  ℹ️  {key}: \"{val[:50]}\"")
    if len(extra_in_fr) > 10:
        print(f"  ... and {len(extra_in_fr) - 10} more")

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
