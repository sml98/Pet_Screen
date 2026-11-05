from pathlib import Path
import subprocess,time,xml.etree.ElementTree as ET,re,json,os
r=Path(__file__).resolve().parents[1];adb=os.environ.get('ADB','adb');out=r/'verification'
def run(*args,timeout=45,check=True):
 p=subprocess.run([adb,*args],capture_output=True,timeout=timeout)
 if check and p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')+p.stdout.decode(errors='replace'))
 return p.stdout.decode(errors='replace')
def nodes():
 run('shell','uiautomator','dump','/sdcard/window.xml',timeout=70)
 return ET.fromstring(run('shell','cat','/sdcard/window.xml')).iter('node')
def tap_text(text):
 for n in nodes():
  if text in n.attrib.get('text',''):
   pts=list(map(int,re.findall(r'\d+',n.attrib['bounds'])));run('shell','input','tap',str((pts[0]+pts[2])//2),str((pts[1]+pts[3])//2));return True
 return False
print('Waiting for Android 15 boot',flush=True)
end=time.time()+480
while time.time()<end:
 try:
  if run('shell','getprop','sys.boot_completed',timeout=4,check=False).strip()=='1':break
 except subprocess.TimeoutExpired:pass
 time.sleep(3)
else:raise RuntimeError('Emulator boot timed out')
print('Booted; installing release',flush=True)
run('shell','wm','size','450x900');run('shell','wm','density','160');run('shell','settings','put','global','window_animation_scale','0');run('shell','settings','put','global','transition_animation_scale','0');run('shell','settings','put','global','animator_duration_scale','0')
run('shell','input','keyevent','82');run('install','-r',os.environ.get('APK_PATH',str(r/'app/build/outputs/apk/release/app-release.apk')),timeout=120)
run('shell','appops','set','com.catpack.pet','SYSTEM_ALERT_WINDOW','allow');run('shell','pm','grant','com.catpack.pet','android.permission.POST_NOTIFICATIONS');run('logcat','-c');run('shell','am','start','-W','-n','com.catpack.pet/.MainActivity',timeout=90);time.sleep(4)
# Scroll to the save/start button, exercising the user-facing entry point.
for i in range(8):
 if tap_text('Salvar e iniciar'):break
 run('shell','input','swipe','225','750','225','260','350')
else:raise RuntimeError('Start button was not found')
time.sleep(3);services=run('shell','dumpsys','activity','services','com.catpack.pet');assert 'isForeground=true' in services,services
print('Foreground overlay started from app button',flush=True)
run('shell','input','keyevent','3');time.sleep(2)
# The pet is near the bottom edge; inspect window frame to locate its rectangle.
windows=run('shell','dumpsys','window','windows');(out/'android-windows.txt').write_text(windows)
# Capture the actual home-screen overlay for visual review.
assert "APPLICATION_OVERLAY" in windows or "ty=2038" in windows
with open(out/'android-overlay.png','wb') as f:subprocess.run([adb,'exec-out','screencap','-p'],stdout=f,check=True,timeout=45)
run('shell','input','keyevent','26');time.sleep(2);run('shell','input','keyevent','26');run('shell','input','keyevent','82');time.sleep(2)
logs=run('logcat','-d','-s','AndroidRuntime:E');assert 'FATAL EXCEPTION' not in logs,logs
(out/'android-runtime.log').write_text(logs)
(out/'android-services.txt').write_text(services)
(out/'android-smoke.json').write_text(json.dumps({'result':'PASS','api':35,'checks':['release installation','launcher activity','start button','foreground service','overlay permission','home screen overlay screenshot','screen off/on without crash'],'physicalDeviceTested':False},indent=2))
print('PASS Android 15 release install, launch, foreground overlay and screen cycle',flush=True)
