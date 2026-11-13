# Projet 3 — openpilot sur PC (simulation et rejeu), comparé à Tesla FSD

Projet 3 du cours Nouvelles technologies, Cégep de Sherbrooke.
Auteur : Joshua Leclerc

Évaluation d'openpilot (comma.ai), un système d'aide à la conduite basé sur l'IA, sur un PC Linux : simulateur MetaDrive et rejeu d'une route réelle. Aucun essai sur un véhicule réel.

**Version finale à corriger : tag `projet3-final`.**

## Contenu

| Fichier / dossier | Rôle |
|-------------------|------|
| `rapport.md` | Rapport final : veille, choix technique, environnement, tests, comparaison, recommandation, contributions |
| `proposition.md` | Proposition remise au cours 11 |
| `journal.md` | Tâches, décisions, trace de veille, utilisation d'agents IA |
| `preuves/` | Captures et mesures des tests (voir `preuves/README.md`) |
| `scripts/` | Scripts de mesure (`watch_hz.py`, `watch_calib.py`) |

## Prérequis

| Élément | Version testée |
|---------|----------------|
| OS | Ubuntu 24.04.4 LTS (machine physique, pas de VM : une VM n'a pas accès au GPU) |
| Matériel | Ryzen 5 5600G, 32 Go RAM, RTX 3070 (pilote NVIDIA 595) |
| Espace disque | 80 Go pour la partition Ubuntu (50 Go libres minimum recommandés) |
| openpilot | commit `d2200f170e30cd9a888e6d77ca95e5c05cfce4e4` |
| MetaDrive | 0.4.2.3 (fork comma, branche `minimal`) |
| Réseau | Internet pour l'installation et le téléchargement de la route de démo |

Aucun compte, mot de passe ni clé n'est nécessaire.

## Installation

Le script officiel `bash <(curl -fsSL openpilot.comma.ai)` a échoué sur notre machine (variables `OPENPILOT_ROOT` et `SKIP_GIT_CLONE` non définies). Installation manuelle :

```bash
sudo apt update && sudo apt install -y git curl git-lfs libportaudio2
git lfs install
cd ~
git clone --recurse-submodules https://github.com/commaai/openpilot.git
cd openpilot
git checkout d2200f170e30cd9a888e6d77ca95e5c05cfce4e4   # version testée
git submodule update --init --recursive
git lfs pull
./tools/op.sh setup          # dépendances (crée .venv)
source .venv/bin/activate
scons -j$(nproc)             # compilation (plusieurs minutes)
```

`libportaudio2` est nécessaire au processus `soundd` (sinon il plante en boucle).

### MetaDrive (simulateur)

MetaDrive est commenté dans `pyproject.toml` d'openpilot, donc `uv sync` ne l'installe pas. Installation manuelle :

```bash
cd ~/openpilot && source .venv/bin/activate
~/.local/bin/uv pip install "metadrive-simulator @ git+https://github.com/commaai/metadrive.git@minimal"
python -c "import metadrive; print('metadrive OK')"
```

Ne pas relancer `uv sync` ensuite (il retire MetaDrive).

## Mise en service

### A. Simulation (MetaDrive)

```bash
# Terminal 1
cd ~/openpilot && source .venv/bin/activate
BIG=1 SCALE=0.5 ./openpilot/tools/sim/launch_openpilot.sh

# Terminal 2
cd ~/openpilot/openpilot/tools/sim && source ~/openpilot/.venv/bin/activate
./run_bridge.py
```

`BIG=1 SCALE=0.5` est obligatoire sur notre machine : sans `SCALE`, l'UI plante (segmentation fault dans `init_window`). Ajuster `SCALE` (0,5 à 0,8) selon l'écran.

Contrôles (dans le terminal 2, pas dans la fenêtre de l'UI) : `2` engager, `1`/`2` vitesse, `3` annuler, `w a s d` conduite manuelle, `i` contact, `r` réinitialiser, `q` quitter.

### B. Rejeu d'une route réelle avec l'IA calculée sur le PC

```bash
# Terminal 1 : rejeu de la route de démo, sorties IA enregistrées bloquées, vitesse 0,2×
cd ~/openpilot && source .venv/bin/activate
./openpilot/tools/replay/replay --demo -b modelV2,cameraOdometry,drivingModelData -x 0.2

# Terminal 2 : interface (une seule instance)
cd ~/openpilot && source .venv/bin/activate
BIG=1 SCALE=0.5 python -c "from openpilot.selfdrive.ui.ui import main; main()"

# Terminal 3 : le modèle d'IA, exécuté sur le PC
cd ~/openpilot && source .venv/bin/activate
python -c "from openpilot.selfdrive.modeld.modeld import main; main()"
```

Sans `-b ...`, l'UI affiche les sorties IA enregistrées dans le véhicule (utile pour comparer). Pendant le rejeu : `s` +10 s, `space` pause, `+/-` vitesse, `q` quitter.

## Tests

Copier les scripts dans `~` ou les lancer depuis `scripts/`, avec le `.venv` d'openpilot activé :

```bash
python scripts/watch_hz.py      # fréquence et validité des messages clés
python scripts/watch_calib.py   # vitesse et état de la calibration
htop                             # CPU (trier avec P)
nvidia-smi                       # utilisation du GPU
```

Résultats attendus et obtenus : voir `rapport.md`, section Tests.

## Retour en arrière

- Essai GPU : `git checkout openpilot/selfdrive/modeld/SConscript && scons -j$(nproc)` remet le modèle sur le CPU.
- Désinstallation : supprimer `~/openpilot` et `~/.comma`.
