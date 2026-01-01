# Encoder - Nouvelle Approche (Grille 40x8)

Ce dossier contient les scripts pour l'encodage des sous-titres dans la vidéo selon la nouvelle approche "Grille Plein Écran".

## Spécifications Techniques

### 1. La Grille (Matrice de Données)
- **Dimensions :** 40 colonnes x 8 lignes.
- **Capacité :** 40 caractères par image (suffisant pour une ligne de sous-titre standard).
- **Total Cellules :** 320 cellules ("flacons").

### 2. Encodage des Données
- **Format :** ASCII Étendu (Latin-1 / ISO-8859-1) pour supporter les accents français.
- **Structure :**
  - Chaque **Colonne** représente 1 caractère.
  - Chaque **Ligne** représente 1 bit de ce caractère (du bit de poids fort au bit de poids faible, ou inversement à définir).
  - **Ligne 0 :** Bit 7 (MSB)
  - ...
  - **Ligne 7 :** Bit 0 (LSB)

### 3. Représentation Visuelle
- **Bit 1 :** Cellule "Pleine" (Couleur/Blanc/Visible).
- **Bit 0 :** Cellule "Vide" (Transparent/Noir).
- La grille est superposée à la vidéo originale.

### 4. Fichiers
- `encode.py` : Script principal (à venir).
- `requirements.txt` : Dépendances (opencv-python, numpy, ffmpeg-python).
