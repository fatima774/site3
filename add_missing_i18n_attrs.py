#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path

project_dir = Path(__file__).parent

# Mappings des textes manquants aux clés
text_key_mappings = {
    "Email*": "email_required",
    "Téléphone*": "phone_required",
    "Ce qui n'est pas inclus :": "what_not_included",
    "Immersion complète en petit groupe.": "immersion_complete_small_group",
    "Flexibilité et personnalisation pour répondre à vos besoins.": "flexibility_and_personalization",
    "Calendrier": "calendar_label",
    'La formation est conçue pour offrir un "bain de français", 30 heures par semaine.': "formation_french_immersion",
    "Des cours ludiques basés sur la pratique orale à partir de documents authentiques, ponctués d'explications grammaticales. Individualisation de l'enseignement et attention aux personnes présentant des troubles DYS ou neuro atypiques.": "fun_practical_classes",
    "Des déjeuners favorisant la conversation informelle, pris avec la professeure dans le centre-ville de Foix, adaptés aux contraintes alimentaires de chacun. Parfois rejoints par des amis pour écouter différents accents.": "convivial_lunches",
    "Des sorties permettant de parler dans des situations réelles de communication en découvrant la ville et ses environs.": "real_situation_outings",
    "Le stage et le prix sont maintenus, mais le programme sera légèrement réduit : 25h de cours au lieu de 30h.": "program_will_be_reduced",
    "Les niveaux correspondent aux profils suivants. Les indications entre parenthèses (A2, B1, etc.) renvoient aux niveaux du CECR (Cadre Européen Commun de Référence pour les Langues).": "cefr_profiles_description",
}

def add_i18n_to_html(file_path, mappings):
    """Ajoute data-i18n aux éléments HTML"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    for text, key in mappings.items():
        escaped_text = re.escape(text)
        
        # Pattern pour label
        pattern = f'(<label[^>]*?)>({escaped_text})(</label>)'
        replacement = f'\\1 data-i18n="{key}">\\2\\3'
        content = re.sub(pattern, replacement, content)
        
        # Pattern pour h3
        pattern = f'(<h3[^>]*?)>({escaped_text})(</h3>)'
        replacement = f'\\1 data-i18n="{key}">\\2\\3'
        content = re.sub(pattern, replacement, content)
        
        # Pattern pour p
        pattern = f'(<p[^>]*?)>({escaped_text})(</p>)'
        replacement = f'\\1 data-i18n="{key}">\\2\\3'
        content = re.sub(pattern, replacement, content)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

html_files = sorted(project_dir.glob('*.html'))

print("="*70)
print("ADDING data-i18n ATTRIBUTES FOR MISSING ELEMENTS")
print("="*70 + "\n")

for html_file in html_files:
    add_i18n_to_html(html_file, text_key_mappings)
    print(f"Updated: {html_file.name}")

print("\n" + "="*70)
print("COMPLETE: All missing data-i18n attributes added")
print("="*70)
