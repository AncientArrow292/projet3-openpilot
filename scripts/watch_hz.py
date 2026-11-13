# Mesure la fréquence (Hz) et la validité des messages openpilot clés.
# Usage : cd ~/openpilot && source .venv/bin/activate && python watch_hz.py
import time
try:
    import cereal.messaging as m
except ImportError:
    import openpilot.cereal.messaging as m

svcs = ['narrowRoadCameraState', 'modelV2', 'cameraOdometry', 'deviceMotion', 'extrinsicsCalibration', 'carState']
sm = m.SubMaster(svcs)
cnt = {s: 0 for s in svcs}
t0 = time.monotonic()
while True:
    sm.update(100)
    for s in svcs:
        if sm.updated[s]:
            cnt[s] += 1
    dt = time.monotonic() - t0
    if dt >= 2:
        print(' | '.join(f"{s}: {cnt[s]/dt:.0f}Hz valid={sm.valid[s]}" for s in svcs))
        cnt = {s: 0 for s in svcs}
        t0 = time.monotonic()
