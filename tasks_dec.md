# Plan de Développement : Décodeur PWA (Caméra iPhone)

Ce document détaille les étapes pour construire une Progressive Web App (PWA) capable de scanner la vidéo encodée via la caméra de l'iPhone et d'afficher les sous-titres en temps réel.

## Architecture Technique
- **Type :** PWA (Progressive Web App) installable.
- **Framework :** HTML5 / Vanilla JS (pour la performance maximale).
- **Accès Caméra :** API `navigator.mediaDevices.getUserMedia`.
- **Traitement d'image :** Canvas API (analyse pixel par pixel).
- **Déploiement :** Vercel (HTTPS requis pour l'accès caméra).

---

## Phase 1 : Structure du Projet & Manifest PWA
*Objectif : Rendre l'application installable sur iPhone (Add to Home Screen).*

- [ ] **Nettoyage :** Supprimer l'ancien `index.html` de test vidéo.
- [ ] **Structure de base :** Créer `index.html`, `style.css`, `app.js`.
- [ ] **Manifest PWA (`manifest.json`) :**
    - Nom : "Decoder IHM".
    - Display : `standalone` (plein écran, sans barre d'URL).
    - Icônes : Nécessaires pour iOS.
- [ ] **Service Worker (`sw.js`) :** Pour la mise en cache et le fonctionnement hors-ligne (requis pour PWA).
- [ ] **Meta Tags iOS :** `<meta name="apple-mobile-web-app-capable" content="yes">`.

## Phase 2 : Accès Caméra (Flux Vidéo)
*Objectif : Afficher le flux de la caméra arrière sur l'écran.*

- [ ] **Demande de permissions :** Gérer `getUserMedia({ video: { facingMode: "environment" } })`.
- [ ] **Élément Vidéo :** Afficher le flux dans une balise `<video>` en `autoplay` et `playsinline`.
- [ ] **Gestion des erreurs :** Gérer le refus de permission ou l'absence de caméra.
- [ ] **Canvas de traitement :** Créer un canvas caché synchronisé avec la taille du flux vidéo.

## Phase 3 : Algorithme de Décodage (Vision par Ordinateur)
*Objectif : Lire la grille 12x12 depuis le flux caméra.*

- [ ] **Synchronisation :** Boucle `requestAnimationFrame` pour capturer les images.
- [ ] **Lecture de la Grille :**
    - Diviser l'image caméra en 12x12 zones.
    - *Défi :* La caméra ne sera pas parfaitement alignée avec l'écran.
    - *Solution V1 (Naïve) :* L'utilisateur doit aligner manuellement la vidéo dans un cadre dessiné sur l'écran.
- [ ] **Extraction des Bits :**
    - Calculer la luminosité moyenne au centre de chaque case (zone 5x5 ou 10x10 pixels).
    - Appliquer un seuil adaptatif (si luminosité > seuil => 1, sinon 0).
- [ ] **Reconstruction ASCII :**
    - Convertir les 144 bits en 18 caractères (Latin-1).
    - Filtrer les caractères invalides/bruit.

## Phase 4 : Interface Utilisateur (UI)
*Objectif : Une interface simple et lisible.*

- [ ] **Overlay de Guidage :** Dessiner une grille semi-transparente par-dessus la caméra pour aider l'utilisateur à cadrer l'écran.
- [ ] **Zone de Sous-titres :** Bandeau noir en bas de l'écran affichant le texte décodé.
- [ ] **Indicateurs de performance :** (Optionnel) Afficher les FPS ou un indicateur de "signal détecté".

## Phase 5 : Optimisation & Robustesse
*Objectif : Réduire le scintillement et les erreurs.*

- [ ] **Lissage Temporel :** Ne mettre à jour le sous-titre que si le même texte est détecté sur plusieurs frames consécutives (ex: 3 frames identiques).
- [ ] **Seuil Dynamique :** Calculer la luminosité moyenne de l'image pour ajuster le seuil de détection (jour vs nuit).

## Phase 6 : Déploiement & Test
- [ ] **Configuration Vercel :** S'assurer que le projet sert bien les fichiers statiques.
- [ ] **Test iOS :** Vérifier l'accès caméra sur Safari mobile.
- [ ] **Validation :** Tester en filmant l'écran de l'ordinateur jouant la vidéo encodée.
