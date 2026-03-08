#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
import re

project_dir = Path(__file__).parent
lang_dir = project_dir / "assets" / "lang"

# Charger les mappings
with open(project_dir / "mapping_report.json", "r", encoding="utf-8") as f:
    report = json.load(f)

new_keys = report["new_keys"]

# Charger fr.json
with open(lang_dir / "fr.json", "r", encoding="utf-8") as f:
    fr_data = json.load(f)

# Créer un index inverse text -> key
text_to_key = {}
for key, value in fr_data.items():
    text_to_key[value] = key

# Générer les patterns regex pour chaque texte
print("="*70)
print("GENERATING REGEX PATTERNS FOR HTML REPLACEMENTS")
print("="*70 + "\n")

html_files = sorted(project_dir.glob('*.html'))
patterns = {}

for html_file in html_files:
    print(f"[FILE] {html_file.name}")
    
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    file_patterns = []
    
    # Pour les titres
    for key, value in new_keys.items():
        # Pattern pour <h1> ... </h1>
        patterns_to_check = [
            (f"(<h1[^>]*>)({re.escape(value)})(</h1>)", f'\\1 data-i18n="{key}">{value}</h1>', 'h1'),
            (f"(<h2[^>]*>)({re.escape(value)})(</h2>)", f'\\1 data-i18n="{key}">{value}</h2>', 'h2'),
            (f"(<h3[^>]*>)({re.escape(value)})(</h3>)", f'\\1 data-i18n="{key}">{value}</h3>', 'h3'),
            (f"(<h4[^>]*>)({re.escape(value)})(</h4>)", f'\\1 data-i18n="{key}">{value}</h4>', 'h4'),
            (f"(<p[^>]*>)({re.escape(value)})(</p>)", f'\\1 data-i18n="{key}">{value}</p>', 'p'),
            (f"(<label[^>]*>)({re.escape(value)})(</label>)", f'\\1 data-i18n="{key}">{value}</label>', 'label'),
            (f"(<span[^>]*>)({re.escape(value)})(</span>)", f'\\1 data-i18n="{key}">{value}</span>', 'span'),
        ]
        
        for pattern, replacement, tag in patterns_to_check:
            if re.search(pattern, content):
                file_patterns.append({
                    'tag': tag,
                    'key': key,
                    'text': value[:50],
                    'pattern': pattern,
                    'replacement': replacement,
                    'count': len(re.findall(pattern, content))
                })
    
    if file_patterns:
        print(f"  Found {len(file_patterns)} potential replacements:")
        for p in file_patterns[:3]:
            print(f"    - <{p['tag']}> key='{p['key']}' (x{p['count']})")
        if len(file_patterns) > 3:
            print(f"    ... and {len(file_patterns) - 3} more")
    else:
        print(f"  No patterns found")
    
    patterns[html_file.name] = file_patterns
    print()

# Sauvegarder les patterns
import json as json_module
with open(project_dir / "replacement_patterns.json", "w", encoding="utf-8") as f:
    # Convertir les patterns en quelque chose de sérialisable  
    serializable = {}
    for filename, file_patterns in patterns.items():
        serializable[filename] = [
            {
                'tag': p['tag'],
                'key': p['key'],
                'text': p['text'],
                'count': p['count']
            }
            for p in file_patterns
        ]
    json_module.dump(serializable, f, ensure_ascii=False, indent=2)

print("\n" + "="*70)
print("Patterns saved to replacement_patterns.json")
print("="*70)
