#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

project_dir = Path(__file__).parent
lang_dir = project_dir / "assets" / "lang"

# Charger les fichiers JSON
with open(lang_dir / "fr.json", "r", encoding="utf-8") as f:
    fr_data = json.load(f)

with open(lang_dir / "en.json", "r", encoding="utf-8") as f:
    en_data = json.load(f)

with open(lang_dir / "es.json", "r", encoding="utf-8") as f:
    es_data = json.load(f)

# Identifiez les clés manquantes dans fr.json
missing_keys_fr = set(en_data.keys()) | set(es_data.keys()) - set(fr_data.keys())

print("="*70)
print("ADDING MISSING FRENCH TRANSLATIONS")
print("="*70 + "\n")

# Traductions françaises pour les clés manquantes
french_translations = {
    "courses_immersion_desc": "Un programme tout compris avec cours particuliers (15 heures), activités et excursions. Apprenez en vivant avec votre professeure. Venez rencontrer mes voisins et amis, découvrir les vins et vignobles de la région. Nous visiterons ensemble les thermes et nagerons à la magnifique piscine de Foix ! En été, nous cultiverons le jardin et cuisinerons les produits biologiques de saison. En hiver, profitez de l'ambiance blanche des stations de ski ! La chambre, à l'étage de ma maison à Foix, est équipée de salle de bain et WC privatifs. Vous pourrez aussi profiter de mon jardin.",
    "courses_immersion_title": "Immersion chez la professeure",
    "inscription_age": "Âge : Les participants doivent être âgés de plus de 18 ans.",
    "inscription_cancellation": "Annulation : Jusqu'à 3 mois avant le début de la formation, le montant sera remboursé après déduction d'un montant de 70 €. En cas d'annulation entre 3 mois et 30 jours avant le début du cours, la moitié du montant sera remboursé. En cas d'annulation à moins de 30 jours, le montant ne sera pas remboursé.",
    "inscription_insurance": "Assurance : Il est conseillé d'avoir une police d'assurance comprenant une assistance voyage.",
    "inscription_payment": "Inscription : 30 % du coût de la formation doit être payé à l'inscription, le reste doit être payé au plus tard le premier jour du cours. Les frais bancaires sont entièrement à la charge de ceux qui s'inscrivent.",
    "inscription_title": "Conditions d'inscription pour les cours de français",
    "prices_immersion_1week": "1200 € / 1 semaine",
    "prices_immersion_2weeks": "2300 € / 2 semaines",
    "prices_immersion_included": "Inclus pour une semaine : logement, repas, 15 heures de cours particuliers, activités, promenade.",
    "prices_immersion_not_included": "Non inclus : entrées au cinéma, musées, grottes et repas au restaurant.",
    "prices_immersion_room": "La chambre, à l'étage de ma maison à Foix, est équipée de salle de bain et WC privatifs. Vous pourrez aussi profiter de mon jardin.",
    "prices_immersion_title": "Immersion chez la professeure",
}

added = 0
for key, value in french_translations.items():
    if key not in fr_data:
        fr_data[key] = value
        added += 1
        print(f"[+] {key}")

print(f"\nTotal keys added to fr.json: {added}")

# Sauvegarder
with open(lang_dir / "fr.json", "w", encoding="utf-8") as f:
    json.dump(fr_data, f, ensure_ascii=False, indent=2)

print("\nfr.json saved successfully")
print(f"New total: {len(fr_data)} keys")

print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

fr_keys = set(fr_data.keys())
en_keys = set(en_data.keys())
es_keys = set(es_data.keys())

missing_en = fr_keys - en_keys
missing_es = fr_keys - es_keys

print(f"Keys in fr not in en: {len(missing_en)}")
print(f"Keys in fr not in es: {len(missing_es)}")

if len(missing_en) == 0 and len(missing_es) == 0:
    print("\n✓ All three JSON files are now in PERFECT SYNC!")
else:
    print("\n⚠️  Some keys are still missing")

print("="*70)
