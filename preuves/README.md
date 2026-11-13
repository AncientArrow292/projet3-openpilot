# Preuves

| Fichier | Contenu |
|---------|---------|
| `sim_ui_plantee_engaged_false.png` | Avant le correctif : `ui` en rouge (plante) dans la liste des processus, `Engaged: False` malgré la touche 2 |
| `sim_ui_fonctionnelle.png` | UI openpilot fonctionnelle dans MetaDrive après le contournement `BIG=1 SCALE=0.5` |
| `sim_alerte_communication_issue.png` | Alerte « Communication Issue Between Processes » : openpilot refuse de s'engager (échec sécuritaire) |
| `test4_htop_simulation.png` | Ressources pendant la simulation : `modeld` ~100 % d'un cœur, `run_bridge.py` ~45+33 %, UI ~29 % |
| `test4_frequences_simulation.txt` | Fréquences en simulation : caméra 15-16 Hz, `modelV2` 3-4 Hz (attendu 20 Hz), `cameraOdometry`/`deviceMotion` invalides |
| `calibration_vitesse_simulation.txt` | Calibration déjà à 100 % ; vitesse max au clavier ~13,7 mph |
| `test5_replay_ia_enregistree.png` | Rejeu de la route de démo avec les sorties IA enregistrées dans le véhicule |
| `test5_replay_ia_en_direct_courbe.png` | Rejeu à 0,2× avec `modeld` exécuté sur le PC : trajectoire qui suit une courbe en ville |
| `test5_replay_ia_en_direct_autoroute_hz.png` | Rejeu à 0,2× sur autoroute : lignes, trajectoire et véhicule devant (chevron jaune) + mesures de fréquence |
| `test5_frequences_replay.txt` | Fréquences en rejeu à 0,2× : caméra 4 Hz, `modelV2` ~3,9 Hz en moyenne (~97 % des images), tout valide |
