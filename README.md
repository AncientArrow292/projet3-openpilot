# Projet 3 — openpilot en simulation (comparé à Tesla FSD)

Projet 3 du cours Nouvelles technologies, Cégep de Sherbrooke.
Auteur : Joshua Leclerc

Évaluation d'openpilot (comma.ai), un système d'aide à la conduite basé sur l'IA, dans le simulateur MetaDrive. Aucun essai sur un véhicule réel.

## Contenu

- `proposition.md` : proposition approuvée
- `journal.md` : tâches, veille, décisions, utilisation d'agents IA
- `rapport.md` : rapport final (à venir)
- `preuves/` : captures, vidéos, logs des tests

## Prérequis

- Ubuntu 24.04 LTS (machine physique avec GPU NVIDIA recommandée)
- Au moins 50 Go libres
- Git, accès Internet pour l'installation

## Installation

```bash
bash <(curl -fsSL openpilot.comma.ai)
cd openpilot
source .venv/bin/activate
scons
git rev-parse HEAD   # noter la version testée dans journal.md
```

## Lancer la simulation

```bash
# Terminal 1 (racine du dépôt openpilot, .venv activé)
./openpilot/tools/sim/launch_openpilot.sh

# Terminal 2
cd openpilot/tools/sim
./run_bridge.py
```

Contrôles : `2` pour engager, `1`/`2` pour la vitesse, `S` pour simuler un freinage (désengagement), `r` pour réinitialiser, `q` pour quitter.

## Tests

Voir `proposition.md` (section Tests prévus) et `rapport.md`.

## Version finale

Tag : `projet3-final` (à créer à la remise)
