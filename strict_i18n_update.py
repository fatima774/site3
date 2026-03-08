#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
import re

project_dir = Path(__file__).parent
lang_dir = project_dir / "assets" / "lang"

# Charger les mappings
with open(lang_dir / "fr.json", "r", encoding="utf-8") as f:
    fr_data = json.load(f)

# Fonction pour faire le remplacement conservateur
def add_i18n_attribute(html_content, text, key):
    """Ajoute data-i18n à une balise contenant le texte"""
    
    # Escaper les caractères spéciaux du texte pour le regex
    escaped_text = re.escape(text)
    
    # Pattern: <tag [stuff où pas data-i18n]>text</tag>
    # Ajouter data-i18n à la balise
    
    patterns = [
        # <h1>text</h1> ou <h1 ...>text</h1> (mais pas data-i18n)
        (f'(<h1[^>]*?)>({escaped_text})(</h1>)', f'\\1 data-i18n="{key}">\\2\\3'),
        (f'(<h2[^>]*?)>({escaped_text})(</h2>)', f'\\1 data-i18n="{key}">\\2\\3'),
        (f'(<h3[^>]*?)>({escaped_text})(</h3>)', f'\\1 data-i18n="{key}">\\2\\3'),
        (f'(<h4[^>]*?)>({escaped_text})(</h4>)', f'\\1 data-i18n="{key}">\\2\\3'),
        (f'(<h5[^>]*?)>({escaped_text})(</h5>)', f'\\1 data-i18n="{key}">\\2\\3'),
        (f'(<h6[^>]*?)>({escaped_text})(</h6>)', f'\\1 data-i18n="{key}">\\2\\3'),
        (f'(<p[^>]*?)>({escaped_text})(</p>)', f'\\1 data-i18n="{key}">\\2\\3'),
        (f'(<label[^>]*?)>({escaped_text})(</label>)', f'\\1 data-i18n="{key}">\\2\\3'),
        (f'(<title[^>]*?)>({escaped_text})(</title>)', f'\\1 data-i18n="{key}">\\2\\3'),
        (f'(<button[^>]*?)>({escaped_text})(</button>)', f'\\1 data-i18n="{key}">\\2\\3'),
        (f'(<a[^>]*?)>({escaped_text})(</a>)', f'\\1 data-i18n="{key}">\\2\\3'),
        (f'(<span[^>]*?)>({escaped_text})(</span>)', f'\\1 data-i18n="{key}">\\2\\3'),
    ]
    
    didReplace = False
    for pattern, replacement in patterns:
        try:
            # Faire le replacement
            new_content, count = re.subn(pattern, replacement, html_content)
            if count > 0:
                html_content = new_content
                didReplace = True
                break
        except re.error:
            # Si le pattern est invalide, continuer
            continue
    
    return html_content, didReplace

# Parcourir les fichiers HTML
html_files = sorted(project_dir.glob('*.html'))

print("="*70)
print("PROCESSING HTML FILES WITH STRICT i18n ADDITIONS")
print("="*70 + "\n")

for html_file in html_files:
    print(f"Processing: {html_file.name}")
    
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Pour chaque clé/texte dans fr_data
    replacements = 0
    for key, value in fr_data.items():
        # Ne pas traiter les textes vides ou très courts
        if len(value) < 2:
            continue
        
        # Vérifier si data-i18n="key" existe déjà
        if f'data-i18n="{key}"' in content:
            continue
        
        # Essayer le remplacement
        new_content, did_replace = add_i18n_attribute(content, value, key)
        if did_replace:
            content = new_content
            replacements += 1
    
    if replacements > 0:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  -> Added {replacements} data-i18n attributes")
    else:
        print(f"  -> No changes needed")

print("\n" + "="*70)
print("COMPLETE: All HTML files processed")
print("="*70)
