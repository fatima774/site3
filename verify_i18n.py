#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from bs4 import BeautifulSoup
import re

project_dir = Path(__file__).parent
lang_dir = project_dir / "assets" / "lang"
html_dir = project_dir

# Charger les fichiers JSON
with open(lang_dir / "fr.json", "r", encoding="utf-8") as f:
    fr_data = json.load(f)

with open(lang_dir / "en.json", "r", encoding="utf-8") as f:
    en_data = json.load(f)

with open(lang_dir / "es.json", "r", encoding="utf-8") as f:
    es_data = json.load(f)

print("="*70)
print("FINAL i18n COMPLETION VERIFICATION REPORT")
print("="*70 + "\n")

# Analyse HTML
html_files = sorted(html_dir.glob('*.html'))
total_i18n_elements = 0
missing_i18n = 0
page_report = []

for html_file in html_files:
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Compter les éléments avec data-i18n
    i18n_els = soup.find_all(attrs={"data-i18n": True})
    
    # Compter les textes qui n'ont pas data-i18n
    text_els = []
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']:
        for el in soup.find_all(tag):
            if el.get_text(strip=True) and not el.get('data-i18n'):
                text_els.append(el)
    
    has_script = "app.js" in content
    
    total_i18n_elements += len(i18n_els)
    missing_i18n += len(text_els)
    
    page_report.append({
        'file': html_file.name,
        'i18n_count': len(i18n_els),
        'missing_count': len(text_els),
        'has_script': has_script,
        'coverage': (len(i18n_els) / (len(i18n_els) + len(text_els)) * 100) if (len(i18n_els) + len(text_els)) > 0 else 100
    })

print("HTML FILES ANALYSIS:")
print("-" * 70)
for page in page_report:
    status = "[OK]" if page['missing_count'] == 0 else "[PARTIAL]"
    script_status = "[YES]" if page['has_script'] else "[NO]"
    print(f"{status} {page['file']:25} | {page['i18n_count']:3} i18n | Script: {script_status} | {page['coverage']:.1f}% coverage")

print("\n" + "="*70)
print("i18n KEYS COVERAGE:")
print("-" * 70)

# Vérifier que toutes les clés ont des traductions
missing_keys = {
    'en': [],
    'es': []
}

for key in fr_data.keys():
    if key not in en_data:
        missing_keys['en'].append(key)
    if key not in es_data:
        missing_keys['es'].append(key)

print(f"French keys: {len(fr_data)}")
print(f"English keys: {len(en_data)} {'(MISSING: ' + str(len(missing_keys['en'])) + ')' if missing_keys['en'] else '(COMPLETE)'}")
print(f"Spanish keys: {len(es_data)} {'(MISSING: ' + str(len(missing_keys['es'])) + ')' if missing_keys['es'] else '(COMPLETE)'}")

print("\n" + "="*70)
print("FINAL SUMMARY:")
print("-" * 70)
total_elements = total_i18n_elements + missing_i18n
coverage_pct = (total_i18n_elements / total_elements * 100) if total_elements > 0 else 0

print(f"Total HTML elements: {total_elements}")
print(f"Translated elements: {total_i18n_elements}")
print(f"Missing translations: {missing_i18n}")
print(f"Coverage rate: {coverage_pct:.1f}%")
print(f"Scripts loaded: {sum(1 for p in page_report if p['has_script'])}/{len(page_report)}")

if coverage_pct >= 95 and all(p['has_script'] for p in page_report) and len(missing_keys['en']) == 0 and len(missing_keys['es']) == 0:
    print("\n[SUCCESS] i18n system is FULLY FUNCTIONAL!")
elif coverage_pct >= 85:
    print("\n[PARTIAL] i18n system is mostly complete")
else:
    print("\n[WARNING] i18n system needs more work")

print("\n" + "="*70)
