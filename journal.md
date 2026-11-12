# Journal — Projet 3

## Tâches et décisions

| Date | Responsable | Tâche | Résultat / décision | Prochaine étape |
|------|-------------|-------|---------------------|-----------------|
| 2026-11-11 | Joshua Leclerc | Proposition et choix du sujet | Sujet : openpilot en simulation (MetaDrive), comparé à Tesla FSD. Machine choisie : JOSH-PC (RTX 3070) plutôt qu'une VM, car une VM n'a pas accès au GPU. Plan B : HP ProBook 450 G5 (iGPU). | Faire approuver le sujet, libérer de l'espace et installer Ubuntu 24.04 |
| 2026-11-12 | Joshua Leclerc | Environnement d'essai | Ubuntu 24.04.4 LTS installé en dual-boot sur JOSH-PC (partition de 80 Go, NVMe), pilote NVIDIA 595 fonctionnel (RTX 3070). Script d'installation officiel (`openpilot.comma.ai`) en échec (variables non définies) : installation manuelle (clone + `tools/op.sh setup`). Compilation `scons` réussie. Version testée : commit `d2200f170e30cd9a888e6d77ca95e5c05cfce4e4`. | Lancer la simulation MetaDrive |

## Veille

| Date | Source | Information suivie | Conséquence pour le projet |
|------|--------|--------------------|----------------------------|
| 2026-11-11 | Releases GitHub commaai/openpilot (RSS) | Version 0.11.3 en préparation (vitesse choisie automatiquement selon la scène) | Noter le commit testé pour garder des résultats comparables |

## Utilisation d'agents IA

| Date | Agent | Objectif | Apport retenu | Vérification |
|------|-------|----------|---------------|--------------|
| 2026-11-11 | Claude | Rédiger la proposition, choisir l'environnement d'essai | Structure de la proposition, tests, commandes d'installation | Commandes et sources à vérifier dans la doc officielle |
