#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from pathlib import Path

project_dir = Path(__file__).parent
lang_dir = project_dir / "assets" / "lang"

# Éléments manquants identifiés et leurs mappings
missing_translations = {
    "email_required": "Email*",
    "phone_required": "Téléphone*",
    "what_not_included": "Ce qui n'est pas inclus :",
    "immersion_complete_small_group": "Immersion complète en petit groupe.",
    "flexibility_and_personalization": "Flexibilité et personnalisation pour répondre à vos besoins.",
    "calendar_label": "Calendrier",
    "formation_french_immersion": 'La formation est conçue pour offrir un "bain de français", 30 heures par semaine.',
    "fun_practical_classes": "Des cours ludiques basés sur la pratique orale à partir de documents authentiques, ponctués d'explications grammaticales. Individualisation de l'enseignement et attention aux personnes présentant des troubles DYS ou neuro atypiques.",
    "convivial_lunches": "Des déjeuners favorisant la conversation informelle, pris avec la professeure dans le centre-ville de Foix, adaptés aux contraintes alimentaires de chacun. Parfois rejoints par des amis pour écouter différents accents.",
    "real_situation_outings": "Des sorties permettant de parler dans des situations réelles de communication en découvrant la ville et ses environs.",
    "program_will_be_reduced": "Le stage et le prix sont maintenus, mais le programme sera légèrement réduit : 25h de cours au lieu de 30h.",
    "cefr_profiles_description": "Les niveaux correspondent aux profils suivants. Les indications entre parenthèses (A2, B1, etc.) renvoient aux niveaux du CECR (Cadre Européen Commun de Référence pour les Langues).",
    "about_p1": "Après des études de Langues et Civilisation Espagnoles à Bordeaux III, Madrid et Séville, obtention du CAPES, et des années d'enseignement en tant que professeure, j'ai choisi de m'installer définitivement dans les Pyrénées de l'Ariège en 2004."
}

# Charger les JSON
with open(lang_dir / "fr.json", "r", encoding="utf-8") as f:
    fr_data = json.load(f)

with open(lang_dir / "en.json", "r", encoding="utf-8") as f:
    en_data = json.load(f)

with open(lang_dir / "es.json", "r", encoding="utf-8") as f:
    es_data = json.load(f)

print("="*70)
print("ADDING MISSING TRANSLATIONS")
print("="*70 + "\n")

added = 0
for key, value in missing_translations.items():
    if key not in fr_data:
        fr_data[key] = value
        en_data[key] = value  # Placeholder
        es_data[key] = value  # Placeholder
        added += 1
        print(f"[+] {key}")

print(f"\nTotal added: {added}")

# Sauvegarder
print("\nSaving files...")
with open(lang_dir / "fr.json", "w", encoding="utf-8") as f:
    json.dump(fr_data, f, ensure_ascii=False, indent=2)

with open(lang_dir / "en.json", "w", encoding="utf-8") as f:
    json.dump(en_data, f, ensure_ascii=False, indent=2)

with open(lang_dir / "es.json", "w", encoding="utf-8") as f:
    json.dump(es_data, f, ensure_ascii=False, indent=2)

print("Done!")
