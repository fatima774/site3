#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from pathlib import Path

# Chemin vers le dossier des langues
lang_dir = Path(__file__).parent / "assets" / "lang"

# Charger les fichiers JSON
with open(lang_dir / "fr.json", "r", encoding="utf-8") as f:
    fr_data = json.load(f)

with open(lang_dir / "en.json", "r", encoding="utf-8") as f:
    en_data = json.load(f)

with open(lang_dir / "es.json", "r", encoding="utf-8") as f:
    es_data = json.load(f)

# Obtenir les clés de chaque fichier
fr_keys = set(fr_data.keys())
en_keys = set(en_data.keys())
es_keys = set(es_data.keys())

# Identifier les clés manquantes
missing_in_en = fr_keys - en_keys
missing_in_es = fr_keys - es_keys

print("╔════════════════════════════════════════════════════════════════╗")
print("║         ANALYSE DES CLÉS MANQUANTES                           ║")
print("╚════════════════════════════════════════════════════════════════╝")
print(f"\n🔍 Clés manquantes dans en.json: {len(missing_in_en)}")
print(f"🔍 Clés manquantes dans es.json: {len(missing_in_es)}")

if missing_in_en:
    print("\n📋 Détail en.json:")
    for key in sorted(missing_in_en):
        print(f"   - {key}")

if missing_in_es:
    print("\n📋 Détail es.json:")
    for key in sorted(missing_in_es):
        print(f"   - {key}")

# Importer googletrans
try:
    from googletrans import Translator
    print("\n✅ googletrans importée avec succès")
except ImportError:
    print("\n❌ googletrans non installée. Installation en cours...")
    os.system("pip install googletrans==4.0.0")
    from googletrans import Translator

translator = Translator()

# Ajouter les clés manquantes à en.json
print("\n" + "="*70)
print("🇬🇧 TRADUCTION VERS L'ANGLAIS")
print("="*70)

for key in sorted(missing_in_en):
    fr_value = fr_data[key]
    # Traduire du français vers l'anglais
    translated = translator.translate(fr_value, src_language='fr', dest_language='en')
    en_value = translated.text
    
    en_data[key] = en_value
    print(f"✅ {key}")
    print(f"   FR: {fr_value[:80]}")
    print(f"   EN: {en_value[:80]}")

# Ajouter les clés manquantes à es.json
print("\n" + "="*70)
print("🇪🇸 TRADUCTION VERS L'ESPAGNOL")
print("="*70)

for key in sorted(missing_in_es):
    fr_value = fr_data[key]
    # Traduire du français vers l'espagnol
    translated = translator.translate(fr_value, src_language='fr', dest_language='es')
    es_value = translated.text
    
    es_data[key] = es_value
    print(f"✅ {key}")
    print(f"   FR: {fr_value[:80]}")
    print(f"   ES: {es_value[:80]}")

# Sauvegarder les fichiers avec la même indentation
print("\n" + "="*70)
print("💾 SAUVEGARDE DES FICHIERS")
print("="*70)

# Sauvegarder en.json
with open(lang_dir / "en.json", "w", encoding="utf-8") as f:
    json.dump(en_data, f, ensure_ascii=False, indent=2)
print("✅ en.json sauvegardé")

# Sauvegarder es.json
with open(lang_dir / "es.json", "w", encoding="utf-8") as f:
    json.dump(es_data, f, ensure_ascii=False, indent=2)
print("✅ es.json sauvegardé")

print("\n" + "="*70)
print("✨ OPÉRATION TERMINÉE AVEC SUCCÈS")
print("="*70)
print(f"\n📊 Résumé:")
print(f"   - Clés ajoutées à en.json: {len(missing_in_en)}")
print(f"   - Clés ajoutées à es.json: {len(missing_in_es)}")
print(f"   - fr.json: inchangé")
