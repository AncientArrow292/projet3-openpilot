# Journal — Projet 3

## Tâches et décisions

| Date | Responsable | Tâche | Résultat / décision | Prochaine étape |
|------|-------------|-------|---------------------|-----------------|
| 2026-11-11 | Joshua Leclerc | Proposition et choix du sujet | Sujet : openpilot en simulation (MetaDrive), comparé à Tesla FSD. Machine choisie : JOSH-PC (RTX 3070) plutôt qu'une VM, car une VM n'a pas accès au GPU. Plan B : HP ProBook 450 G5 (iGPU). | Faire approuver le sujet, libérer de l'espace et installer Ubuntu 24.04 |
| 2026-11-12 | Joshua Leclerc | Environnement d'essai | Ubuntu 24.04.4 LTS installé en dual-boot sur JOSH-PC (partition de 80 Go, NVMe), pilote NVIDIA 595 fonctionnel (RTX 3070). Script d'installation officiel (`openpilot.comma.ai`) en échec (variables non définies) : installation manuelle (clone + `tools/op.sh setup`). Compilation `scons` réussie. Version testée : commit `d2200f170e30cd9a888e6d77ca95e5c05cfce4e4`. | Lancer la simulation MetaDrive |
| 2026-11-12 | Joshua Leclerc | MetaDrive manquant | `run_bridge.py` : `No module named 'metadrive'`. MetaDrive est commenté dans `pyproject.toml` (groupe `tools`). Installé à la main : `uv pip install "metadrive-simulator @ git+https://github.com/commaai/metadrive.git@minimal"` (v0.4.2.3). | Lancer la simulation |
| 2026-11-12 | Joshua Leclerc | UI qui plante | `ui` : segmentation fault (code 139) dans `init_window` (raylib, rendu logiciel). Contourné avec `BIG=1 SCALE=0.5` (le calcul automatique de l'échelle plante sur ce PC). `soundd` réparé avec `libportaudio2`. | Engager openpilot |
| 2026-11-12 | Joshua Leclerc | Essai GPU (OpenCL) | `DEV=CL` au lieu de `DEV=CPU:LLVM` dans `modeld/SConscript` : la vérification de tinygrad échoue (553/553 sorties fausses). Retour au CPU (`git checkout`). Conclusion : sur PC, le modèle ne donne des résultats corrects que sur le CPU. | Mesurer les performances |
| 2026-11-13 | Joshua Leclerc | Mesure des fréquences (test ressources) | Caméra simulée 15-16 Hz, `carState` 100 Hz, mais `modelV2` (sortie de l'IA) 3-4 Hz au lieu de 20 Hz ; `modeld` à ~100 % d'un cœur. `cameraOdometry`/`deviceMotion` marqués invalides → alerte « Communication Issue Between Processes » → openpilot refuse de s'engager (échec sécuritaire). Calibration déjà à 100 %. Vitesse max au clavier ~13,7 mph. UI plus fluide quand sa fenêtre est cachée (rendu logiciel). | Rejeu (test 5) et rédaction |
| 2026-11-13 | Joshua Leclerc | Test 5 : rejeu avec IA en direct | `replay --demo -b modelV2,cameraOdometry -x 0.2` + `modeld` lancé seul + UI (`BIG=1 SCALE=0.5`). Mesure : caméra 4 Hz, `modelV2` 4 Hz, `cameraOdometry`/`deviceMotion` valides, `carState` 20 Hz (= 100 Hz × 0,2). Le modèle traite environ 100 % des images à 0,2×. Trajectoire qui suit les courbes, lignes de voie et véhicule devant (chevron jaune) détectés. Captures dans `preuves/`. | Bloquer aussi `drivingModelData`, captures des cas ratés, rédaction |

## Veille

| Date | Source | Information suivie | Conséquence pour le projet |
|------|--------|--------------------|----------------------------|
| 2026-11-11 | Releases GitHub commaai/openpilot (RSS) | Version 0.11.3 en préparation (vitesse choisie automatiquement selon la scène) | Noter le commit testé pour garder des résultats comparables |

## Utilisation d'agents IA

| Date | Agent | Objectif | Apport retenu | Vérification |
|------|-------|----------|---------------|--------------|
| 2026-11-11 | Claude | Rédiger la proposition, choisir l'environnement d'essai | Structure de la proposition, tests, commandes d'installation | Commandes et sources à vérifier dans la doc officielle |
