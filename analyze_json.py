#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
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

print("╔════════════════════════════════════════════════════════════════╗")
print("║         ANALYSE COMPLÈTE DES FICHIERS JSON                    ║")
print("╚════════════════════════════════════════════════════════════════╝")
print(f"\n📊 Nombre de clés:")
print(f"   fr.json: {len(fr_keys)}")
print(f"   en.json: {len(en_keys)}")
print(f"   es.json: {len(es_keys)}")

# Identifier les différences
missing_in_en = fr_keys - en_keys
missing_in_es = fr_keys - es_keys
extra_in_en = en_keys - fr_keys
extra_in_es = es_keys - fr_keys

print(f"\n🔍 Clés manquantes dans en.json (par rapport à fr.json): {len(missing_in_en)}")
if missing_in_en:
    for key in sorted(missing_in_en):
        print(f"   ❌ {key}")

print(f"\n🔍 Clés manquantes dans es.json (par rapport à fr.json): {len(missing_in_es)}")
if missing_in_es:
    for key in sorted(missing_in_es):
        print(f"   ❌ {key}")

print(f"\n🔍 Clés supplémentaires dans en.json (par rapport à fr.json): {len(extra_in_en)}")
if extra_in_en:
    for key in sorted(extra_in_en):
        print(f"   ⚠️  {key}")

print(f"\n🔍 Clés supplémentaires dans es.json (par rapport à fr.json): {len(extra_in_es)}")
if extra_in_es:
    for key in sorted(extra_in_es):
        print(f"   ⚠️  {key}")

# Résumé
print("\n" + "="*70)
print("📋 RÉSUMÉ")
print("="*70)
if not missing_in_en and not missing_in_es:
    print("✅ Tous les fichiers JSON sont EN PARITÉ COMPLÈTE")
    print("   - Aucune clé manquante")
    print("   - Tous les fichiers contiennent les mêmes clés de base de fr.json")
else:
    print("⚠️  Des clés manquent")
