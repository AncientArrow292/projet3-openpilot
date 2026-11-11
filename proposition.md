# Proposition — Projet 3

**Sujet :** Évaluer openpilot (comma.ai) comme aide à la conduite IA open source, comparé à Tesla FSD (Supervised)  
**Membres :** Joshua Leclerc  
**Dépôt GitHub :** https://github.com/AncientArrow292/projet3-openpilot  
**Invitation enseignant envoyée :** Oui (nicolas.payre@cegepsherbrooke.qc.ca)  
**Date :** 2026-11-11

## La Technologie que l'on veut étudier

### Le besoin

Un gestionnaire de flotte (ex. : petite entreprise de livraison) demande au service TI s'il existe une façon d'ajouter de l'aide à la conduite (maintien de voie + régulateur adaptatif) à des véhicules déjà en service, sans remplacer la flotte par des Tesla avec FSD. Avant tout essai sur route, le TI doit valider la technologie dans un environnement contrôlé.

- **Utilisateur cible :** technicien TI qui évalue la solution pour le gestionnaire de flotte.
- **Résultat attendu :** une mise en œuvre fonctionnelle d'openpilot en simulation, des tests mesurables et une recommandation (adoption, adoption sous conditions ou rejet).

### La technologie IA

**openpilot** est un système d'aide à la conduite open source (licence MIT) développé par comma.ai. L'IA est au cœur du système : un modèle de réseau de neurones prend les images de la caméra et prédit directement la trajectoire à suivre (approche « end-to-end »). Les versions récentes ont un modèle entraîné dans un simulateur appris (*world model*) à partir des données de conduite de la flotte. C'est un système de niveau 2 : le conducteur doit rester attentif en tout temps.

**Rôle dans le besoin :** contrôler la direction et la vitesse du véhicule dans la voie, et rendre le contrôle au conducteur quand il ne peut plus gérer la situation.

**Pourquoi ce choix :** c'est un des rares systèmes de conduite assistée par IA dont le code est ouvert, qu'on peut installer et tester soi-même sur un PC, et qui est utilisé par de vrais conducteurs.

### Solution alternative crédible

**Tesla FSD (Supervised)** : système d'aide à la conduite IA fermé, aussi de niveau 2, disponible au Canada par abonnement seulement (achat unique abandonné en février 2026). Fonctionne seulement sur des Tesla compatibles. La comparaison se fera à partir de la documentation (pas d'essai : aucun accès à une Tesla).

### Sources

| # | Source | Lien | Consultée le | Fiabilité |
|---|--------|------|--------------|-----------|
| 1 | Dépôt officiel openpilot (README, SAFETY.md) — **doc officielle** | https://github.com/commaai/openpilot | 2026-11-11 | Élevée : source primaire du développeur, mais présente le produit sous un angle favorable |
| 2 | Notes de version openpilot (RELEASES.md) — **doc officielle** | https://github.com/commaai/openpilot/blob/master/RELEASES.md | 2026-11-11 | Élevée : historique officiel des versions |
| 3 | Guide officiel du simulateur openpilot (MetaDrive) — **doc officielle** | https://github.com/commaai/openpilot/blob/master/openpilot/tools/sim/README.md | 2026-11-11 | Élevée : commandes et contrôles du simulateur; la copie sur docs.comma.ai semble moins à jour que le dépôt |
| 3b | Limites déclarées d'openpilot — **doc officielle** | https://docs.comma.ai/LIMITATIONS/ | 2026-11-11 | Élevée pour ce que l'éditeur reconnaît comme limites; ne remplace pas une étude indépendante |
| 4 | Page officielle Tesla sur Autopilot / FSD | https://www.tesla.com/support/autopilot | 2026-11-11 | Élevée pour les fonctions et limites annoncées; source commerciale |
| 5 | Drive Tesla Canada — guide FSD (prix, disponibilité au Canada) | https://driveteslacanada.ca/news/tesla-fsd-autopilot-canada-guide/ | 2026-11-11 | Moyenne : média spécialisé non officiel, à recouper avec Tesla |

### Mécanisme de veille

- **Outil :** suivi du dépôt GitHub `commaai/openpilot` (Watch → Custom → *Releases*) + flux RSS des versions : `https://github.com/commaai/openpilot/releases.atom`, lu dans un lecteur RSS.
- **Information suivie :** nouvelles versions et changements touchant le modèle de conduite et le simulateur. Ex. : la version 0.11.3 est en préparation (vitesse choisie automatiquement par openpilot selon la scène). Conséquence possible : fixer la version testée pour que les résultats restent comparables.
- **Côté Tesla :** suivi des nouvelles FSD au Canada (Drive Tesla Canada) pour garder à jour le prix et la disponibilité dans la comparaison.
- La trace de veille sera notée dans `journal.md`.

## L'approche du projet

### Inclus / exclu

| Inclus | Exclu |
|--------|-------|
| Installation d'openpilot sur PC Linux | Essai sur route réelle (risque pour la sécurité, et ma Civic 2012 n'est pas compatible) |
| Essais dans le simulateur MetaDrive (pont `tools/sim`) | Achat du matériel comma (comma four, harnais) |
| Relecture d'une route de démonstration publique (`tools/replay`) | Installation ou essai de Tesla FSD |
| Mesure des ressources (CPU, GPU, RAM) | Modification ou ré-entraînement du modèle |
| Comparaison documentée avec Tesla FSD | |

### Environnement d'essai

| Élément | Détail |
|---------|--------|
| Machine | JOSH-PC (PC de bureau personnel, machine physique) |
| CPU / RAM | AMD Ryzen 5 5600G, 32 Go |
| GPU | NVIDIA RTX 3070 (pilote NVIDIA propriétaire) |
| Stockage | Partition Ubuntu dédiée en dual-boot avec Windows, au moins 50 Go libres |
| OS | Ubuntu 24.04 LTS (cible de développement officielle d'openpilot) |
| Logiciels | openpilot (commit noté dans le journal avec `git rev-parse HEAD`), MetaDrive (inclus avec le pont `tools/sim`), Git, Python (`.venv` d'openpilot), `htop`, `nvidia-smi` |

**Pourquoi une machine physique plutôt qu'une VM :** une VM classique n'a pas accès à la carte graphique. Le modèle d'IA et le rendu 3D tourneraient sur le processeur, ce qui fausserait les tests de conduite et de ressources. La RTX 3070 permet de faire rouler la simulation de façon fluide.

**Plan B :** si l'installation échoue sur JOSH-PC, le portable HP ProBook 450 G5 (i5-8250U, 16 Go, iGPU Intel UHD 620, déjà en dual-boot) servira pour le rejeu et la comparaison de ressources (GPU dédié vs intégré).
- **Réseau :** Internet seulement pour l'installation (clonage du dépôt, dépendances, route de démo). Les essais en simulation se font en local.
- **Comptes et accès :** compte GitHub (dépôt du projet). Aucun compte comma requis pour la simulation. Aucun secret dans le dépôt.
- **Coûts prévus :** 0 $ (PC existant, logiciels libres; espace libéré sur le disque existant). FSD : environ 99 $/mois au Canada (documentation seulement).
- **Données utilisables :** données générées par le simulateur et route de démo publique fournie par comma. Aucune donnée personnelle.

Un schéma (PC → openpilot ↔ pont → MetaDrive) sera ajouté dans le rapport.

### Démarche

1. Libérer l'espace et installer Ubuntu 24.04 en dual-boot sur JOSH-PC (sauvegarde avant le partitionnement), puis vérifier le pilote NVIDIA avec `nvidia-smi`.
2. Installer openpilot avec le script officiel (`bash <(curl -fsSL openpilot.comma.ai)`, puis `scons`) et vérifier que la compilation fonctionne.
3. Lancer openpilot (`./openpilot/tools/sim/launch_openpilot.sh`) et le pont MetaDrive (`./run_bridge.py`), puis engager le système en simulation.
4. Lire une route de démo avec `tools/replay` pour voir ce que le modèle détecte (voies, véhicule devant).
5. Exécuter les tests ci-dessous en notant les conditions, le résultat attendu, le résultat obtenu et une preuve (capture, vidéo, logs).
6. Comparer avec Tesla FSD selon : coût, compatibilité des véhicules, ouverture du code, données collectées, fonctions disponibles, encadrement légal.
7. Formuler la recommandation.

## Les grandes étapes du Projet

Projet fait seul : Joshua Leclerc est responsable de toutes les étapes.

| Cours | Étape |
|-------|-------|
| 11 | Proposition, création du dépôt GitHub, invitation de l'enseignant, mise en place de la veille |
| 12 | Environnement d'essai prêt, openpilot fonctionnel dans MetaDrive, premier résultat, trace de veille |
| 13 | Trois tests faits, comparaison avec FSD, limites, recommandation à discuter |
| 14 | Démonstration (scénario normal + cas limite en direct, vidéos de secours) |
| 15 | Remise finale : `rapport.md`, `README.md`, `journal.md`, preuves, tag `projet3-final` |

## Tests prévus

| # | Test | Conditions | Critère de réussite observable |
|---|------|------------|-------------------------------|
| 1 | **Usage normal** : maintien de voie | MetaDrive, route avec courbes douces, openpilot engagé, 5 min | Aucune sortie de voie, aucun désengagement non demandé; vidéo + logs |
| 2 | **Cas limite / échec** : courbe serrée à haute vitesse | Même route, vitesse de croisière augmentée jusqu'à la limite | openpilot avertit le conducteur (alerte « reprendre le contrôle ») **avant** de sortir de la voie. Échec si sortie de voie sans alerte |
| 3 | **Sécurité** : reprise de contrôle | openpilot engagé, freinage simulé par le conducteur | Désengagement immédiat (< 1 s) avec message visible; aucune commande d'openpilot après le freinage |
| 4 | **Ressources** | Simulation en cours pendant 5 min sur JOSH-PC | Utilisation CPU, GPU et RAM relevée avec `htop` et `nvidia-smi`; le système reste fluide (pas de messages de retard du modèle) |
| 5 | **Qualité de la perception** (route de démo) | Relecture d'une route réelle publique | Les lignes de voie et le véhicule devant sont détectés sur la majorité de la route; captures des cas ratés |

Ce que ces tests ne permettront **pas** d'affirmer : la performance sur une vraie route, en hiver ou sur un vrai véhicule. La simulation ne remplace pas un essai réel.
