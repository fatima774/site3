#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from bs4 import BeautifulSoup
import re

# Chemin du projet
project_dir = Path(__file__).parent
lang_dir = project_dir / "assets" / "lang"
html_dir = project_dir

# Charger les fichiers JSON
with open(lang_dir / "fr.json", "r", encoding="utf-8") as f:
    fr_data = json.load(f)

# Fonction pour extraire texte visible du HTML
def get_visible_text_elements(html_file):
    """Extrait les éléments texte visibles d'une page HTML"""
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Récupérer tous les éléments texte
        elements = []
        
        # Title
        title = soup.find('title')
        if title:
            text = title.get_text(strip=True)
            has_i18n = title.get('data-i18n')
            elements.append({
                'tag': 'title',
                'text': text,
                'has_i18n': bool(has_i18n),
                'i18n_key': has_i18n,
                'element': title
            })
        
        # H1, H2, H3
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            for el in soup.find_all(tag):
                text = el.get_text(strip=True)
                if text and text not in ['Menu', '📍']:
                    has_i18n = el.get('data-i18n')
                    elements.append({
                        'tag': tag,
                        'text': text,
                        'has_i18n': bool(has_i18n),
                        'i18n_key': has_i18n,
                        'element': el
                    })
        
        # P (paragraphes)
        for el in soup.find_all('p'):
            text = el.get_text(strip=True)
            if text and len(text) > 10:  # Ignorer les très courts
                has_i18n = el.get('data-i18n')
                elements.append({
                    'tag': 'p',
                    'text': text[:80] + ('...' if len(text) > 80 else ''),
                    'full_text': text,
                    'has_i18n': bool(has_i18n),
                    'i18n_key': has_i18n,
                    'element': el
                })
        
        # Boutons
        for el in soup.find_all(['button', 'a'], class_=re.compile(r'btn|cta')):
            text = el.get_text(strip=True)
            if text and text not in ['Menu']:
                has_i18n = el.get('data-i18n')
                elements.append({
                    'tag': el.name,
                    'text': text,
                    'has_i18n': bool(has_i18n),
                    'i18n_key': has_i18n,
                    'element': el
                })
        
        # Labels
        for el in soup.find_all('label'):
            text = el.get_text(strip=True)
            if text:
                has_i18n = el.get('data-i18n')
                elements.append({
                    'tag': 'label',
                    'text': text,
                    'has_i18n': bool(has_i18n),
                    'i18n_key': has_i18n,
                    'element': el
                })
        
        return elements
    except Exception as e:
        print(f"Erreur en lisant {html_file}: {e}")
        return []

# Fonction pour générer une clé i18n cohérente
def generate_key(text):
    """Génère une clé i18n à partir du texte"""
    # Minuscules, remplacer les espaces par underscores, retirer charactères spéciaux
    key = re.sub(r'[^a-z0-9 ]', '', text.lower())
    key = re.sub(r'\s+', '_', key).strip('_')
    # Limiter à 50 caractères
    return key[:50]

# Analyser tous les fichiers HTML
html_files = sorted(project_dir.glob('*.html'))
print("="*70)
print("ANALYSE DES FICHIERS HTML")
print("="*70 + "\n")

total_elements = 0
missing_i18n = 0

for html_file in html_files:
    print(f"\n[FILE] {html_file.name}")
    print("-" * 70)
    
    elements = get_visible_text_elements(html_file)
    
    if not elements:
        print("   (No text elements found)")
        continue
    
    has_script = "app.js" in html_file.read_text(encoding='utf-8')
    print(f"   JS script loaded: {'YES' if has_script else 'NO'}")
    
    missing = []
    for el in elements:
        total_elements += 1
        if not el['has_i18n']:
            missing_i18n += 1
            key = el['i18n_key'] or generate_key(el['text'])
            missing.append({
                'tag': el['tag'],
                'text': el['text'],
                'key': key
            })
    
    if missing:
        print(f"   Elements without data-i18n: {len(missing)}")
        for m in missing[:5]:
            print(f"      - <{m['tag']}> \"{m['text']}\" -> {m['key']}")
        if len(missing) > 5:
            print(f"      ... and {len(missing) - 5} others")
    else:
        print(f"   OK: All elements have data-i18n")

print("\n" + "="*70)
print("RESUME GLOBAL")
print("="*70)
print(f"HTML files analyzed: {len(html_files)}")
print(f"Total text elements: {total_elements}")
print(f"Elements without data-i18n: {missing_i18n}")
print(f"i18n coverage: {((total_elements - missing_i18n) / total_elements * 100):.1f}%" if total_elements > 0 else "N/A")
