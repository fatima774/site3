#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from bs4 import BeautifulSoup
import re

project_dir = Path(__file__).parent
lang_dir = project_dir / "assets" / "lang"

# Charger les JSON existants
with open(lang_dir / "fr.json", "r", encoding="utf-8") as f:
    fr_data = json.load(f)

# Dictionnaire pour tracer les mappings
mappings = {}

# Listes de clés existantes dans fr.json
known_keys = set(fr_data.keys())

# Fonction pour trouver la meilleure clé correspondante
def find_best_key_match(text):
    """Essaie de trouver une clé JSON qui correspond au texte"""
    text_lower = text.lower().strip()
    
    # Vérifier les correspondances exactes et proches
    for key, value in fr_data.items():
        value_lower = value.lower().strip()
        # Correspondance exacte
        if value_lower == text_lower:
            return key
        # Correspondance partielle (pour les textes courts)
        if len(text) > 20 and value_lower.startswith(text_lower[:20]):
            return key
    
    return None

# Fonction pour générer une nouvelle clé
def generate_unique_key(text):
    """Génère une clé unique pour un nouveau texte"""
    # Créer une clé base
    base_key = re.sub(r'[^a-z0-9 ]', '', text.lower())
    base_key = re.sub(r'\s+', '_', base_key).strip('_')[:45]
    
    counter = 1
    key = base_key
    while key in known_keys:
        key = f"{base_key}_{counter}"
        counter += 1
    
    return key

# Parcourir tous les fichiers HTML
html_files = sorted(project_dir.glob('*.html'))
new_keys_needed = {}

print("="*70)
print("MAPPING KEYS FOR ALL HTML FILES")
print("="*70 + "\n")

for html_file in html_files:
    print(f"[FILE] {html_file.name}")
    
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content,  'html.parser')
    
    # Extraire tous les textes visibles et leurs clés
    file_mappings = {}
    
    # Title
    title = soup.find('title')
    if title:
        text = title.get_text(strip=True)
        has_key = title.get('data-i18n')
        if not has_key:
            key = find_best_key_match(text)
            if not key:
                key = generate_unique_key(text)
                new_keys_needed[key] = text
                print(f"   Title: NEW KEY '{key}'")
            else:
                print(f"   Title: existing key '{key}'")
            file_mappings[f"{html_file.name}:title"] = (text, key)
    
    # H1-H6
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        for el in soup.find_all(tag):
            text = el.get_text(strip=True)
            if text and len(text) > 3 and text not in ['Menu']:
                has_key = el.get('data-i18n')
                if not has_key:
                    key = find_best_key_match(text)
                    if not key:
                        key = generate_unique_key(text)
                        if key not in new_keys_needed:
                            new_keys_needed[key] = text
                            print(f"   <{tag}>: NEW KEY '{key}'")
                    file_mappings[f"{html_file.name}:{tag}"] = (text, key)
    
    # P elements
    for el in soup.find_all('p'):
        text = el.get_text(strip=True)
        if text and len(text) > 15:
            has_key = el.get('data-i18n')
            if not has_key:
                key = find_best_key_match(text)
                if not key:
                    key = generate_unique_key(text)
                    if key not in new_keys_needed:
                        new_keys_needed[key] = text
    
    # Labels and buttons
    for selector_tag in ['button', 'label', 'a']:
        for el in soup.find_all(selector_tag):
            text = el.get_text(strip=True)
            if text and len(text) > 3 and text not in ['Menu', 'Accueil']:
                has_key = el.get('data-i18n')
                if not has_key:
                    key = find_best_key_match(text)
                    if not key:
                        key = generate_unique_key(text)
                        if key not in new_keys_needed:
                            new_keys_needed[key] = text
    
    print()

print("\n" + "="*70)
print(f"NEW KEYS NEEDED: {len(new_keys_needed)}")
print("="*70)
for key, value in sorted(new_keys_needed.items()):
    print(f"  {key}: {value[:60]}")

# Sauvegarder le report
print("\n" + "="*70)
print("SAVED TO: mapping_report.json")
print("="*70)

report = {
    "total_new_keys": len(new_keys_needed),
    "new_keys": new_keys_needed
}

with open(project_dir / "mapping_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"Total new keys needed: {len(new_keys_needed)}")
