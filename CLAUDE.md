# CLAUDE.md — Projet 3 (openpilot vs Tesla FSD)

## Contexte

- Projet 3 du cours **Nouvelles technologies**, Cégep de Sherbrooke. Auteur : Joshua Leclerc (Josh).
- Énoncé : « Explorer et évaluer une technologie IA ». Technologie choisie : **openpilot** (comma.ai), comparé à **Tesla FSD**.
- Évaluation uniquement **sur PC** : simulateur MetaDrive + rejeu d'une route réelle. Aucun essai sur un vrai véhicule.
- Version finale à corriger : tag git **`projet3-final`**. Prochaine étape : démonstration au cours 14 + entrevue avec le prof.

## Langue et style

- Tout le contenu du dépôt est **en français** (rapport, journal, README). Garder ce registre : clair, niveau cégep, pas trop soutenu.
- Josh parle français et anglais ; répondre dans la langue de sa question.

## Structure du dépôt

| Fichier / dossier | Rôle |
|---|---|
| `rapport.md` | Rapport final (veille, choix technique, environnement, tests, comparaison, recommandation, contributions) |
| `proposition.md` | Proposition remise au cours 11 (ne plus modifier) |
| `journal.md` | Tâches et décisions, veille, **utilisation d'agents IA** |
| `preuves/` | Captures, mesures, vidéos des tests (index dans `preuves/README.md`) |
| `scripts/` | `watch_hz.py` (fréquence/validité des messages), `watch_calib.py` (vitesse, calibration) |
| `README.md` | Prérequis, installation, mise en service, tests, retour en arrière |

## Règles de travail

- **Chaque tâche ou décision** → une ligne dans le tableau « Tâches et décisions » de `journal.md` (date, responsable, tâche, résultat/décision, prochaine étape).
- **Chaque utilisation de Claude** → une ligne dans « Utilisation d'agents IA » de `journal.md` (objectif, apport retenu, vérification). C'est exigé par le cours.
- Toute nouvelle preuve ajoutée dans `preuves/` doit être décrite dans `preuves/README.md`, y compris ce qu'elle **ne montre pas**.
- Ne jamais présenter un résultat non mesuré comme un fait. Les limites connues doivent rester écrites dans le rapport.
- Ne pas déplacer le tag `projet3-final` sans que Josh le demande.

## Environnement d'essai (hors dépôt)

- Machine : **JOSH-PC**, Ubuntu 24.04.4 en dual-boot (Ryzen 5 5600G, 32 Go, RTX 3070, pilote NVIDIA 595). Pas de VM (pas d'accès GPU).
- openpilot est installé dans **`~/openpilot`** (pas dans ce dépôt), commit testé `d2200f170e30cd9a888e6d77ca95e5c05cfce4e4` (branche master = développement, pas une version publiée).
- Toujours activer le venv : `cd ~/openpilot && source .venv/bin/activate`.
- MetaDrive (fork comma, branche `minimal`, v0.4.2.3) installé à la main. **Ne pas lancer `uv sync`** : ça retire MetaDrive.
- L'UI plante sans `BIG=1 SCALE=0.5` (segfault dans `init_window`).
- Le modèle tourne sur le **CPU** seulement : l'essai GPU (`DEV=CL`) donne des sorties fausses. Retour : `git checkout openpilot/selfdrive/modeld/SConscript && scons -j$(nproc)`.
- Commandes de simulation et de rejeu : voir `README.md` (section « Mise en service »).

## Résultats clés (à ne pas contredire sans nouvelle mesure)

- Simulation : `modelV2` à 3-4 Hz au lieu de 20 Hz, `modeld` ≈ 100 % d'un cœur → alerte « Communication Issue Between Processes » → openpilot refuse de s'engager (échec sécuritaire).
- Rejeu à 0,2× avec `modeld` sur le PC : le modèle suit ~100 % des images, lignes, trajectoire et véhicule devant détectés. Une seule route, de jour, temps clair : on ne peut pas généraliser.
- La vidéo `demo_simulation_conduite_manuelle.mp4` ne montre **pas** l'alerte ; la preuve de l'alerte est `sim_alerte_communication_issue.png`.
