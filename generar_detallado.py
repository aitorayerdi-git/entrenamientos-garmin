from pathlib import Path
import zipfile,json,io,re
from collections import defaultdict
from datetime import datetime
import fitdecode
R=Path(__file__).parent; ZP=max((R/'datos garmin'/'completo').glob('*.zip'),key=lambda p:p.stat().st_mtime)
def mon(v):
 return datetime.fromtimestamp(v/1000).strftime('%Y-%m') if isinstance(v,(int,float)) else str(v)[:7]
def av(v):
 import statistics
 return statistics.median(v) if v else None
with zipfile.ZipFile(ZP) as z:
 ns=z.namelist(); vv=defaultdict(list);ll=defaultdict(list);rr=defaultdict(list);ss=defaultdict(list);daily={}
 for n in ns:
  try:
   o=json.loads(z.read(n))
   if 'ActivityVo2Max_' in n:
    for x in o:
     if x.get('vo2MaxValue') and x.get('sport')=='RUNNING' and 20<=x['vo2MaxValue']<=85:vv[mon(x['calendarDate'])].append(x['vo2MaxValue'])
   elif 'MetricsAcuteTrainingLoad_' in n:
    for x in o:
     if x.get('dailyTrainingLoadChronic') is not None:daily[str(x['calendarDate'])]=x
   elif 'UDSFile_' in n:
    for x in o:
     if x.get('restingHeartRate') and 30<=x['restingHeartRate']<=100:rr[mon(x['calendarDate'])].append(x['restingHeartRate'])
   elif n.endswith('_sleepData.json'):
    for x in o:
     sec=sum(x.get(k,0) or 0 for k in ('deepSleepSeconds','lightSleepSeconds','remSleepSeconds'))
     if not sec:
      try:sec=(datetime.fromisoformat(x['sleepEndTimestampGMT'])-datetime.fromisoformat(x['sleepStartTimestampGMT'])).total_seconds()
      except:sec=0
     if 7200<=sec<=57600:ss[mon(x['calendarDate'])].append(sec/3600)
  except:pass
 for x in daily.values():ll[mon(x['calendarDate'])].append(x['dailyTrainingLoadChronic'])
 cfg=json.loads(z.read(next(n for n in ns if n.endswith('_heartRateZones.json'))))[0]; floors=[cfg[k] for k in ('zone1Floor','zone2Floor','zone3Floor','zone4Floor','zone5Floor')]
 zones=defaultdict(lambda:[0]*5);fits=0
 for on in []:
  if 'UploadedFiles_' not in on or not on.endswith('.zip'):continue
  with zipfile.ZipFile(io.BytesIO(z.read(on))) as iz:
   for fn in iz.namelist():
    try:
     typ=None;last=None
     with fitdecode.FitReader(io.BytesIO(iz.read(fn)),error_handling=fitdecode.ErrorHandling.IGNORE) as f:
      for q in f:
       if not isinstance(q,fitdecode.FitDataMessage):continue
       if q.name=='file_id':
        typ=str(q.get_value('type',fallback='')).lower()
        if typ!='activity':break
        fits+=1
       elif typ=='activity' and q.name=='record':
        ts=q.get_value('timestamp',fallback=None);hr=q.get_value('heart_rate',fallback=None)
        if ts and hr and last:
         dt=min(max((ts-last).total_seconds(),0),10);zi=max(0,min(4,sum(hr>=v for v in floors)-1));zones[ts.year][zi]+=dt
        if ts:last=ts
    except:pass
 months=sorted(set(vv)|set(ll)|set(rr)|set(ss)); years=sorted({int(x[:4]) for x in months});D={}
 for y in years:
  D[y]=[]
  for m in range(1,13):
   k=f'{y}-{m:02d}';D[y].append({'vo2':av(vv[k]),'load':av(ll[k]),'sleep':av(ss[k]),'rhr':av(rr[k])})
html=(R/'informe-detallado-demo.html').read_text(encoding='utf-8')
html=re.sub(r'<div class="demo">.*?</div>','',html,count=1).replace('Demostración','Datos reales').replace('prototipo','datos reales')
html=re.sub(r'<p class="muted">Datos ficticios actualizados:.*?</p>',f'<p class="muted">Exportación Garmin actualizada: {datetime.fromtimestamp(ZP.stat().st_mtime).strftime("%d/%m/%Y %H:%M")} · {fits} actividades FIT procesadas</p>',html,count=1)
html=html.replace('HRV nocturna','Duración del sueño').replace('Media mensual en milisegundos','Mediana mensual en horas').replace("hrv:wave(y,m,47,1.8,6)","sleep:null").replace("'#hrv','hrv'","'#hrv','sleep'")
html=re.sub(r'ALL=\[.*?\];let hidden',f'ALL={json.dumps(years)};const Z={json.dumps({y:[round(100*v/sum(a),1) if sum(a) else 0 for v in a] for y,a in zones.items()})};let hidden',html,count=1)
html=re.sub(r'const D=\{\};ALL\.forEach\(.*?\);',f'const D={json.dumps(D,separators=(",",":"))};',html,count=1)
html=html.replace("let z1=17+(y-2019)%5,z2=49-(y-2019)%4,z3=20,z4=10,z5=100-z1-z2-z3-z4;","let [z1,z2,z3,z4,z5]=Z[y]||[0,0,0,0,0];")
html=html.replace('Media móvil de 42 días · índice ficticio','Promedio mensual de la carga crónica calculada por Garmin').replace('Ejemplo del reparto anual que se calculará a partir de archivos FIT','Calculado desde los registros FIT y los límites personales de Garmin').replace('Distribución ficticia por año.','Distribución real por año.')
html=re.sub(r'<div class="kpis">.*?</div></div>',f'<div class="kpis"><div class="kpi"><span class="muted">Datos reales</span><b>{len(years)} años</b><small class="muted">Garmin Data Management</small></div><div class="kpi"><span class="muted">FIT de actividad</span><b>{fits}</b></div><div class="kpi"><span class="muted">Zonas personales</span><b>{floors[0]}–{floors[-1]}+</b><small class="muted">ppm</small></div><div class="kpi"><span class="muted">HRV</span><b>—</b><small class="muted">No incluida en la exportación</small></div></div>',html,count=1)
html=html.replace("vals=ys.flatMap(y=>D[y].map(x=>x[key]))","vals=ys.flatMap(y=>D[y].map(x=>x[key])).filter(v=>v!=null)")
html=html.replace("let pts=D[yr].map((a,i)=>[x(i),y(a[key])]);","let pts=D[yr].flatMap((a,i)=>a[key]==null?[]:[[x(i),y(a[key])]]);")
html=html.replace("xmin=15,xmax=110,ymin=42,ymax=58","xmin=Math.min(...pts.map(q=>q[0]))*.95,xmax=Math.max(...pts.map(q=>q[0]))*1.05,ymin=Math.min(...pts.map(q=>q[1]))*.98,ymax=Math.max(...pts.map(q=>q[1]))*1.02")
html=html.replace("ml/kg/min · enero a diciembre","Carrera · mediana mensual · ml/kg/min")
(R/'informe-detallado.html').write_text(html,encoding='utf-8')
idx=R/'index.html';s=idx.read_text(encoding='utf-8').replace('href="informe-detallado-demo.html"','href="informe-detallado.html"').replace('Datos ficticios','Datos reales').replace('Abrir demostración','Abrir informe');stamp=datetime.fromtimestamp(ZP.stat().st_mtime).strftime('%d/%m/%Y %H:%M');s=re.sub(r'<!--DETAILED_DATE-->.*?<!--/DETAILED_DATE-->',f'<!--DETAILED_DATE-->Última actualización: {stamp}<!--/DETAILED_DATE-->',s);idx.write_text(s,encoding='utf-8')
print('Generado',len(years),'años',fits,'FIT')
