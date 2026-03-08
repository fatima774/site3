#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

# Chemin vers le dossier des langues
lang_dir = Path(__file__).parent / "assets" / "lang"

# Charger les fichiers JSON
with open(lang_dir / "en.json", "r", encoding="utf-8") as f:
    en_data = json.load(f)

with open(lang_dir / "es.json", "r", encoding="utf-8") as f:
    es_data = json.load(f)

# Traductions manuelles de l'espagnol vers l'anglais pour les clés manquantes
translations = {
    "courses_immersion_title": "Immersion at the teacher's house",
    "courses_immersion_desc": "An all-inclusive program with individual lessons (15 hours), activities and excursions. Learn by living with your teacher. Come meet my neighbors and friends, discover the wines and vineyards of the region, walk with me! We will visit the hot springs together and swim in the wonderful Foix swimming pool! In summer, we will tend the vegetable garden together and cook with seasonal organic products. In winter, enjoy the white atmosphere of ski resorts! The room, located on the upper floor of my house in Foix, has a private bathroom. You will also be able to enjoy my garden.",
    "inscription_title": "Registration conditions for French classes",
    "inscription_age": "Age: Participants must be over 18 years old.",
    "inscription_payment": "Registration: 30% of the training cost must be paid at registration, the remainder must be paid at the latest on the first day of class. Bank fees are entirely the responsibility of those registered.",
    "inscription_cancellation": "Cancellation: Up to 3 months before the training begins, the amount will be refunded after deducting an amount of 70 €. In case of cancellation between 3 months and 30 days before the course begins, half of the amount will be refunded. In case of cancellation less than 30 days before, the amount will not be refunded.",
    "inscription_insurance": "Insurance: It is advisable to have an insurance policy that includes travel assistance.",
    "prices_immersion_title": "Immersion at the teacher's house",
    "prices_immersion_1week": "1200 € / 1 week",
    "prices_immersion_2weeks": "2300 € / 2 weeks",
    "prices_immersion_included": "Included for one week: accommodation, meals, 15 hours of individual lessons, activities, walk.",
    "prices_immersion_room": "The room, located on the upper floor of my house in Foix, has a private bathroom. You will also be able to enjoy my garden.",
    "prices_immersion_not_included": "Not included: cinema tickets, museums, caves and restaurant meals.",
}

print("╔════════════════════════════════════════════════════════════════╗")
print("║    AJOUT DES CLÉS MANQUANTES À en.json                       ║")
print("╚════════════════════════════════════════════════════════════════╝\n")

en_keys = set(en_data.keys())
es_keys = set(es_data.keys())
extra_in_es = es_keys - en_keys

print(f"📋 Clés à ajouter: {len(extra_in_es)}\n")

for key in sorted(extra_in_es):
    es_value = es_data[key]
    en_value = translations.get(key, es_value)
    
    en_data[key] = en_value
    print(f"✅ {key}")
    print(f"   ES: {es_value[:75]}")
    print(f"   EN: {en_value[:75]}\n")

# Sauvegarder en.json avec la bonne indentation
with open(lang_dir / "en.json", "w", encoding="utf-8") as f:
    json.dump(en_data, f, ensure_ascii=False, indent=2)

print("="*70)
print("💾 en.json mise à jour avec succès")
print(f"   Total de clés: {len(en_data)}")
print("="*70)
