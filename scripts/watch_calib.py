# Affiche la vitesse (mph) et l'état de la calibration openpilot.
# Usage : cd ~/openpilot && source .venv/bin/activate && python watch_calib.py
try:
    import cereal.messaging as m
except ImportError:
    import openpilot.cereal.messaging as m

sm = m.SubMaster(['carState', 'extrinsicsCalibration'])
while True:
    sm.update(500)
    mph = round(sm['carState'].vEgo * 2.237, 1)
    cal = sm['extrinsicsCalibration'].to_dict()
    info = {k: v for k, v in cal.items() if 'status' in k.lower() or 'perc' in k.lower() or 'valid' in k.lower()}
    print(f"{mph} mph | {info if info else list(cal.keys())}")
