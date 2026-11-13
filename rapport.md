# Rapport — Projet 3 : openpilot, une aide à la conduite IA open source

**Auteur :** Joshua Leclerc
**Cours :** Nouvelles technologies, Cégep de Sherbrooke
**Dépôt :** https://github.com/AncientArrow292/projet3-openpilot (tag `projet3-final`)

---

## 1. Besoin et résultat attendu

Un gestionnaire de flotte (ex. : petite entreprise de livraison) demande au service TI s'il est possible d'ajouter une aide à la conduite (maintien de voie, régulateur adaptatif) à des véhicules déjà en service, plutôt que de remplacer la flotte par des Tesla avec FSD. Avant tout essai sur route, le technicien TI doit valider la technologie dans un environnement contrôlé.

- **Utilisateur cible :** technicien TI qui évalue la solution.
- **Résultat attendu :** une mise en œuvre fonctionnelle d'openpilot sur PC, des tests mesurables et une recommandation (adoption, adoption sous conditions ou rejet).

## 2. Veille technologique

### Outil et information suivie

- **Outil :** suivi des versions du dépôt `commaai/openpilot` (GitHub, onglet *Releases*, et flux RSS `releases.atom`).
- **Information suivie :** la version 0.11.2 apporte un nouveau modèle de conduite ; la 0.11.3 est en préparation, avec une vitesse choisie automatiquement selon la scène.
- **Conséquence pour le projet :** le dépôt change vite. Nous avons fixé la version testée (commit `d2200f1`) et l'avons notée dans le journal et le README pour que les résultats restent comparables et reproductibles.
- **Autre information trouvée en suivant le dépôt :** MetaDrive est désactivé (ligne commentée) dans `pyproject.toml`. Conséquence : installation manuelle du simulateur (voir section 4).

### Sources

| Source | Type | Consultée | Fiabilité |
|--------|------|-----------|-----------|
| [Dépôt openpilot](https://github.com/commaai/openpilot) (README, SAFETY, RELEASES, `pyproject.toml`) | Officielle | 2026-11-11 au 13 | Élevée : source primaire, mais rédigée par l'éditeur |
| [Guide du simulateur](https://github.com/commaai/openpilot/blob/master/openpilot/tools/sim/README.md) | Officielle | 2026-11-12 | Élevée ; la copie sur docs.comma.ai semble moins à jour |
| [Liste des véhicules compatibles](https://docs.comma.ai/CARS/) | Officielle | 2026-11-13 | Élevée pour la compatibilité annoncée |
| [Boutique comma (comma four)](https://comma.ai/shop) | Officielle, commerciale | 2026-11-13 | Élevée pour le prix ; source commerciale |
| [Drive Tesla Canada — guide FSD](https://driveteslacanada.ca/news/tesla-fsd-autopilot-canada-guide/) | Média spécialisé | 2026-11-13 | Moyenne : non officiel, recoupé avec d'autres médias |
| [tslna — FSD au Canada](https://tslna.com/?p=3690) | Média spécialisé | 2026-11-11 | Moyenne : non officiel |

## 3. Choix technique

**openpilot** est un système d'aide à la conduite open source (licence MIT) développé par comma.ai. L'IA est au cœur du système : un réseau de neurones (`modeld`) reçoit les images de la caméra et prédit la trajectoire, les lignes de voie et les véhicules devant. Le reste du système (planification, contrôle) utilise ces prédictions. C'est un système de **niveau 2** : le conducteur reste responsable en tout temps. Le dépôt le décrit lui-même comme un logiciel de qualité alpha, destiné à la recherche.

**Pourquoi ce choix :** c'est l'un des rares systèmes de conduite assistée par IA dont le code est ouvert et qu'on peut installer et tester soi-même sur un PC.

**Alternative :** Tesla FSD (Supervised), système fermé de niveau 2, comparé à partir de la documentation (section 6).

**Ce que le projet n'inclut pas :** essai sur route, achat d'un appareil comma, modification ou ré-entraînement du modèle. Ma Civic 2012 n'est pas compatible (pas de régulateur adaptatif ni de maintien de voie d'origine), et tester un système non supporté sur la voie publique serait dangereux.

## 4. Environnement d'essai

### Matériel et logiciels

| Élément | Détail |
|---------|--------|
| Machine | JOSH-PC, machine physique (pas de VM : une VM n'a pas accès au GPU) |
| CPU / RAM | AMD Ryzen 5 5600G (6 cœurs / 12 fils), 32 Go |
| GPU | NVIDIA RTX 3070, pilote 595 |
| Stockage | Partition Ubuntu de 80 Go en dual-boot avec Windows (NVMe) |
| OS | Ubuntu 24.04.4 LTS (cible officielle d'openpilot) |
| openpilot | commit `d2200f170e30cd9a888e6d77ca95e5c05cfce4e4` |
| Simulateur | MetaDrive 0.4.2.3 (fork comma) |
| Réseau | Internet seulement pour l'installation et la route de démo ; essais en local |
| Comptes | Aucun (pas de compte comma, aucune clé) |
| Coût | 0 $ |

### Schéma

```
                       JOSH-PC (Ubuntu 24.04)
 ┌──────────────────────────────────────────────────────────────┐
 │                                                              │
 │  Source d'images                    openpilot                │
 │  ┌────────────────────┐   caméra   ┌──────────────────────┐  │
 │  │ A. MetaDrive (GPU) │──────────▶│ modeld (IA, CPU)     │  │
 │  │    via run_bridge  │            │   │ modelV2          │  │
 │  │ ou                 │            │   ▼                  │  │
 │  │ B. replay (route   │  état du   │ locationd, planner,  │  │
 │  │    réelle de démo) │──véhicule─▶│ controlsd, selfdrived│  │
 │  └────────────────────┘            └──────────┬───────────┘  │
 │                                               │ messages     │
 │                                               ▼              │
 │                                    ┌──────────────────────┐  │
 │                                    │ UI (raylib, CPU)     │  │
 │                                    └──────────────────────┘  │
 │  Mesures : watch_hz.py, htop, nvidia-smi                     │
 └──────────────────────────────────────────────────────────────┘
```

Dans un vrai déploiement, la source d'images serait la caméra de l'appareil comma, et `controlsd` enverrait les commandes au véhicule par le port OBD-II. Sur PC, MetaDrive ou le rejeu remplacent la caméra et le véhicule.

### Installation, difficultés et corrections

La procédure complète est dans le `README.md`. Les difficultés rencontrées :

| Difficulté | Diagnostic | Correction | Vérification |
|------------|------------|------------|--------------|
| Pas assez d'espace sur JOSH-PC | Windows refusait de réduire C: (0 Mo disponible) | `pagefile.sys` toujours actif : désactivé par PowerShell, redémarrage, réduction de 80 Go, puis réactivé | Partition de 80 Go non allouée, puis Ubuntu installé |
| Affichage corrompu à l'installation | Pilote libre `nouveau` avec la RTX 3070 | Démarrage en *safe graphics*, pilotes tiers cochés | `nvidia-smi` affiche la RTX 3070 |
| Script d'installation officiel en échec | Variables `OPENPILOT_ROOT` et `SKIP_GIT_CLONE` non définies | Clone manuel + `tools/op.sh setup` | `scons` : `done building targets` |
| `No module named 'metadrive'` | MetaDrive commenté dans `pyproject.toml` | `uv pip install` depuis le fork comma | `import metadrive` réussit |
| `soundd` plante | Bibliothèque audio manquante | `apt install libportaudio2` | `soundd` passe au vert |
| `ui` plante (code 139) | Segmentation fault dans `init_window` (raylib, rendu logiciel) ; le calcul automatique de l'échelle échoue | Forcer `BIG=1 SCALE=0.5` | La fenêtre s'ouvre, `ui` au vert ([capture](preuves/sim_ui_fonctionnelle.png)) |
| Essai du modèle sur GPU | `DEV=CPU:LLVM` codé en dur ; essai avec `DEV=CL` (OpenCL) | La vérification de tinygrad échoue : 553 sorties sur 553 fausses. Retour au CPU (`git checkout`) | Recompilation réussie sur CPU |

## 5. Tests

Les résultats attendus ont été définis dans la proposition, avant les essais. Les tests 1 et 3 de la proposition (maintien de voie et reprise de contrôle en simulation) n'ont pas pu être exécutés : openpilot refuse de s'engager sur ce PC (voir test 2). Le rejeu d'une route réelle a servi de test d'usage normal.

### Test 1 — Usage normal : perception de l'IA sur une route réelle

- **Conditions :** route de démo de comma (vidéo et données réelles), rejeu à 0,2×, sorties IA enregistrées bloquées (`-b modelV2,cameraOdometry`), modèle `modeld` exécuté sur le PC.
- **Résultat attendu :** les lignes de voie et le véhicule devant sont détectés sur la majorité de la route ; tous les messages en aval sont valides.
- **Résultat obtenu :** trajectoire qui suit les courbes en ville et sur l'autoroute, lignes de voie détectées, véhicule devant signalé (chevron jaune). Aucune erreur visible sur toute la route. Mesures : caméra 4 Hz, `modelV2` 3,9 Hz en moyenne (environ 97 % des images traitées), `cameraOdometry` et `deviceMotion` valides tout au long.
- **Preuves :** [courbe en ville](preuves/test5_replay_ia_en_direct_courbe.png), [autoroute + fréquences](preuves/test5_replay_ia_en_direct_autoroute_hz.png), [mesures](preuves/test5_frequences_replay.txt), [IA enregistrée dans le véhicule, pour comparaison](preuves/test5_replay_ia_enregistree.png).
- **Interprétation :** quand il a le temps de traiter chaque image, le modèle donne une perception correcte. **Réussi.**

### Test 2 — Cas limite / échec : openpilot en temps réel sur un PC

- **Conditions :** simulation MetaDrive en temps réel, véhicule en mouvement, tentative d'engagement (touche `2`).
- **Résultat attendu (proposition) :** openpilot avertit le conducteur avant de sortir de la voie plutôt que d'échouer en silence.
- **Résultat obtenu :** openpilot **refuse de s'engager**. L'UI affiche « Communication Issue Between Processes ». Mesures : caméra simulée 15-16 Hz, mais `modelV2` seulement 3-4 Hz (20 Hz attendus). Comme les prédictions arrivent trop lentement, `cameraOdometry` et `deviceMotion` sont marqués invalides, et le système bloque l'engagement. La calibration, elle, était à 100 %.
- **Preuves :** [alerte](preuves/sim_alerte_communication_issue.png), [mesures](preuves/test4_frequences_simulation.txt), [calibration et vitesse](preuves/calibration_vitesse_simulation.txt).
- **Interprétation :** l'échec est **sécuritaire**. openpilot détecte que ses données sont dégradées et refuse de conduire, au lieu de conduire mal. C'est le comportement attendu d'un système d'aide à la conduite. **Réussi** (comme cas d'échec), mais le scénario prévu (courbe serrée) n'a pas pu être joué.

### Test 3 — Ressources : CPU et GPU

- **Conditions :** simulation en cours, mesures avec `htop` et `nvidia-smi`.
- **Résultat attendu :** le système reste fluide ; le GPU est utilisé.
- **Résultat obtenu :**

| Processus | Charge mesurée |
|-----------|----------------|
| `modeld` (IA) | ~100 % d'un cœur (limité à un seul cœur) |
| `run_bridge.py` (simulateur) | ~45 % + 33 % + 7 % |
| `ui` | ~29 % (moins quand sa fenêtre est cachée) |
| GPU (RTX 3070) | 16 %, 1,2 Go de mémoire, utilisés par MetaDrive seulement |
| CPU global | ~25 % en moyenne sur 12 fils |

  Essai GPU pour le modèle (OpenCL) : sorties fausses à 100 %, refusées par la vérification automatique.
- **Preuves :** [htop](preuves/test4_htop_simulation.png), journal du 2026-11-12.
- **Interprétation :** le goulot est le modèle, exécuté sur un seul cœur du CPU. Le PC n'est pas saturé dans l'ensemble, mais le modèle ne peut pas aller plus vite. Le GPU ne peut pas le remplacer avec cette version. **Échoué** par rapport au critère « fluide ».

### Tests prévus non réalisés

| Test prévu | Raison |
|------------|--------|
| Maintien de voie en simulation, 5 min | openpilot ne s'engage pas sur ce PC (test 2) |
| Reprise de contrôle par freinage (touche `S`) | Même raison : impossible de désengager un système qui ne s'engage pas |

### Ce que les tests permettent et ne permettent pas d'affirmer

- **Ils permettent d'affirmer :** la perception du modèle est correcte sur la route de démo ; openpilot détecte des données trop lentes et refuse de s'engager ; sur un CPU de bureau, le modèle tourne à environ 4 Hz au lieu de 20 Hz.
- **Ils ne permettent pas d'affirmer :** que le contrôle (direction, freinage) fonctionne, puisqu'il n'a pas été testé ; que la perception est fiable la nuit, sous la pluie, dans la neige ou avec des lignes effacées (une seule route, de jour) ; que les performances seraient les mêmes sur l'appareil comma, qui a une puce dédiée ; que les résultats valent pour une version publiée, puisque l'UI indique « This branch is not tested (master) » : nous avons testé la branche de développement.

## 6. Comparaison avec Tesla FSD (Supervised)

FSD n'a pas été installé ni testé. La colonne Tesla repose sur la documentation ; la colonne openpilot distingue le documenté (D) de l'observé (O).

| Critère | openpilot | Tesla FSD (Supervised) |
|---------|-----------|------------------------|
| Niveau d'autonomie | Niveau 2, conducteur responsable (D) | Niveau 2, conducteur responsable (D) |
| Véhicules | 350+ modèles de 27 marques, s'ils ont déjà le régulateur adaptatif et le maintien de voie d'origine (D) | Tesla seulement, avec au moins l'ordinateur HW3 (D) |
| Coût | Appareil comma four : 999 $ US, harnais inclus, sans abonnement obligatoire (D) | Abonnement de 99 $/mois au Canada ; achat unique abandonné en février 2026 (D) |
| Code et transparence | Open source (MIT), installable et vérifiable sur PC (O) | Fermé, impossible à évaluer hors d'une Tesla (D) |
| Matériel requis | Appareil comma dédié ; sur PC, le modèle tourne à ~4 Hz sur 20 (O) | Ordinateur Tesla intégré ; HW3 moins performant que HW4/AI4 (D) |
| Perception | Correcte sur la route de démo (O) | Non évaluée |
| Échec sécuritaire | Refuse de s'engager si ses données sont dégradées (O) | Non évalué |
| Encadrement | Logiciel « alpha » pour la recherche selon l'éditeur ; responsabilité de l'utilisateur (D) | Produit commercial ; Transport Canada indique que les véhicules autonomes ne sont pas offerts commercialement au Canada (D) |

**Pour notre besoin (véhicules existants) :** FSD oblige à remplacer la flotte par des Tesla, ce qui va à l'encontre de la demande. openpilot peut s'ajouter à des véhicules existants, mais seulement s'ils sont compatibles.

## 7. Recommandation

**Adoption sous conditions**, sous forme de projet pilote. **Rejet** de l'idée de valider la technologie uniquement sur PC.

**Avantages :**
- Perception de l'IA correcte sur une vraie route (test 1).
- Comportement sécuritaire : refuse de conduire avec des données dégradées (test 2).
- Coût bien plus faible que le remplacement de véhicules : environ 999 $ US par véhicule, sans abonnement, contre l'achat d'une Tesla plus 99 $/mois.
- Code ouvert, ce qui permet au service TI de comprendre et vérifier le système.

**Limites :**
- Le contrôle du véhicule n'a pas été validé : nos tests couvrent la perception, pas la conduite.
- Sur PC, le système ne fonctionne pas en temps réel (~4 Hz sur 20) : un PC de bureau ne remplace pas l'appareil comma pour valider la technologie.
- Installation fragile hors des conditions prévues par l'éditeur (script en échec, simulateur désactivé, UI qui plante sans correctif).
- Logiciel présenté comme alpha ; niveau 2 seulement.

**Conditions de déploiement :**
1. Vérifier que les véhicules de la flotte sont dans la liste officielle (régulateur adaptatif et maintien de voie d'origine). Les véhicules non compatibles sont exclus.
2. Tester sur 1 ou 2 véhicules avec un appareil comma, sur un terrain fermé d'abord, avec un conducteur formé.
3. Vérifier les questions d'assurance et de responsabilité avant tout usage sur la voie publique.
4. Former les conducteurs : niveau 2, mains au volant et attention en tout temps.
5. Fixer une version d'openpilot et suivre les notes de version avant chaque mise à jour.

**Ressources nécessaires :** appareil comma par véhicule, temps de formation, un technicien pour l'installation et le suivi des versions.

## 8. Contributions

Projet réalisé seul : **Joshua Leclerc** a fait toutes les étapes (proposition, installation, essais, mesures, rapport).

### Utilisation d'agents IA

Les agents IA ont servi à m'aider. Ce ne sont pas la technologie étudiée (openpilot).

| Agent | Objectif | Apport retenu | Vérification |
|-------|----------|---------------|--------------|
| Claude | Proposition, installation, diagnostic des pannes, scripts de mesure, rédaction | Correctifs (`SCALE`, MetaDrive, `libportaudio2`, fichier d'échange), scripts `watch_hz.py` et `watch_calib.py`, structure du rapport | Chaque commande exécutée et vérifiée sur JOSH-PC ; une hypothèse de l'agent (calibration bloquée sous 15 mph) s'est révélée fausse après mesure et a été corrigée |
| ChatGPT | Proposition alternative | Non retenue : tests qui vérifiaient un script plutôt que l'IA, pas d'alternative crédible | Comparée à l'énoncé |
