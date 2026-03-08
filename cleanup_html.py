#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path

project_dir = Path(__file__).parent
html_files = sorted(project_dir.glob('*.html'))

print("="*70)
print("CLEANING UP DUPLICATE data-i18n ATTRIBUTES")
print("="*70 + "\n")

for html_file in html_files:
    print(f"Processing: {html_file.name}")
    
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Trouver et nettoyer les doublons data-i18n
    # Pattern: data-i18n="key1" ... data-i18n="key2"
    # Garder seulement le premier
    
    def remove_duplicate_i18n(match):
        """Enlever les doublons data-i18n sur la même ligne"""
        line = match.group(0)
        # Trouver tous les data-i18n="..."
        i18n_matches = re.findall(r'data-i18n="[^"]*"', line)
        if len(i18n_matches) > 1:
            # Garder seulement le premier data-i18n
            line = line.replace(i18n_matches[1], "", 1)
            if len(i18n_matches) > 2:
                for extra in i18n_matches[2:]:
                    line = line.replace(extra, "", 1)
        return line
    
    # Appliquer le nettoyage
    original = content
    content = re.sub(r'(<[^>]*?\bdata-i18n="[^"]*"[^>]*data-i18n="[^"]*"[^>]*?>)', remove_duplicate_i18n, content)
    
    # Aussi nettoyer les espaces en trop
    content = re.sub(r'(\sdata-i18n="[^"]*")\s+(data-i18n)', r'\1 \2', content)
    
    if content != original:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  -> Cleaned up duplicates")
    else:
        print(f"  -> No duplic ates found")

# Aussi nettoyer les attributs data-i18n sur des éléments qui ne doivent pas les avoir
print("\n" + "="*70)
print("REMOVING INCORRECT data-i18n ATTRIBUTES")
print("="*70 + "\n")

for html_file in html_files:
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    
    # Ne pas mettre data-i18n sur le logo (a.logo)
    content = re.sub(r'(<a class="logo"[^>]*?)data-i18n="[^"]*"([^>]*?>)', r'\1\2', content)
    
    if content != original:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{html_file.name}: Removed incorrect attributes")

print("\n" + "="*70)
print("COMPLETE: Cleanup done")
print("="*70)
