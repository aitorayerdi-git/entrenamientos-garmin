import csv,json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

root=Path(__file__).parent
source=max((root/'datos garmin').rglob('*.csv'),key=lambda p:p.stat().st_mtime)
outer=list(csv.reader(open(source,encoding='utf-8-sig',newline='')))
rows=[next(csv.reader([r[0]])) if len(r)==1 else r for r in outer[1:] if r]
def num(v):
 try:return float(v.replace('.','').replace(',','.')) if v not in ('','--') else None
 except:return None
data=[]
for r in rows:
 try:d=datetime.fromisoformat(r[1]); avg=num(r[7])
 except:continue
 if avg:data.append([d.year,d.month,r[0].replace('\xad',''),avg])
hrmax=206 # percentil 99 de las FC máximas registradas; evita un valor extremo de 219
groups={'Carrera total':lambda t:any(x in t.lower() for x in ('trail','carrera','cinta')),'Ciclismo':lambda t:'cicl' in t.lower(),'Natación':lambda t:'nataci' in t.lower(),'Todos':lambda t:True}
agg={}
for group,test in groups.items():
 a=defaultdict(lambda:[[0]*5 for _ in range(12)])
 for y,m,t,hr in data:
  if test(t):a[y][m-1][min(4,max(0,sum(hr/hrmax>=x for x in (.6,.7,.8,.9))))]+=1
 agg[group]={str(y):v for y,v in a.items()}
payload=json.dumps(agg,ensure_ascii=False,separators=(',',':'))
html='''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Zonas de FC media</title><style>body{margin:0;background:#f3f7f5;color:#17212b;font:15px/1.5 system-ui}main{width:min(1100px,calc(100% - 28px));margin:30px auto}section{background:white;border:1px solid #dce5e1;border-radius:16px;padding:22px}h1{font-size:clamp(2rem,5vw,3.5rem);line-height:1;margin-bottom:.5rem}select{padding:9px;border:1px solid #ccd8d3;border-radius:8px;margin:0 10px 18px 0}svg{width:100%;height:440px}.grid{stroke:#e7eeeb}.txt{fill:#6c7973;font-size:11px}.legend{display:flex;flex-wrap:wrap;gap:12px;margin-top:10px}.legend span{display:flex;align-items:center;gap:5px}.dot{width:9px;height:9px;border-radius:50%}.note{color:#65727e}a{color:#087f5b}</style></head><body><main><a href="muestra-graficos.html">← Panel principal</a><h1>Zonas de frecuencia cardiaca media</h1><p class="note">Porcentaje mensual de sesiones cuya <b>frecuencia cardiaca media</b> cae en la zona elegida. Una línea por año.</p><section><select id="sport"><option>Carrera total</option><option>Ciclismo</option><option>Natación</option><option>Todos</option></select><select id="zone"><option value="0">Z1 · &lt;60% (&lt;124 ppm)</option><option value="1">Z2 · 60–70% (124–143 ppm)</option><option value="2" selected>Z3 · 70–80% (144–164 ppm)</option><option value="3">Z4 · 80–90% (165–184 ppm)</option><option value="4">Z5 · ≥90% (≥185 ppm)</option></select><svg id="chart"></svg><div class="legend" id="legend"></div><p class="note"><b>Estimación:</b> zonas calculadas sobre una FC máxima estimada de 206 ppm, correspondiente al percentil 99 de las máximas registradas. No representa minutos reales en zona; para ello necesitaremos los archivos FIT.</p></section></main><script>const D=__DATA__,M=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],C=['#087f5b','#d9485f','#3468c0','#e28413','#744fc6','#008da8','#8c6d31','#444'];function render(){let d=D[document.querySelector('#sport').value],z=+document.querySelector('#zone').value,ys=Object.keys(d).sort(),svg=document.querySelector('#chart'),W=900,H=410,p={l:45,r:12,t:15,b:35},x=i=>p.l+i*(W-p.l-p.r)/11,y=v=>H-p.b-v/100*(H-p.t-p.b),s='';for(let i=0;i<5;i++){let v=100-i*25,yy=y(v);s+=`<line class="grid" x1="${p.l}" y1="${yy}" x2="${W-p.r}" y2="${yy}"/><text class="txt" x="${p.l-7}" y="${yy+4}" text-anchor="end">${v}%</text>`}M.forEach((m,i)=>s+=`<text class="txt" x="${x(i)}" y="${H-10}" text-anchor="middle">${m}</text>`);ys.forEach((yr,j)=>{let pts=[];d[yr].forEach((counts,i)=>{let n=counts.reduce((a,b)=>a+b,0);if(n)pts.push([x(i),y(100*counts[z]/n)])});s+=`<polyline fill="none" stroke="${C[j%C.length]}" stroke-width="2.5" points="${pts.map(q=>q.join(',')).join(' ')}"/>`;pts.forEach(q=>s+=`<circle cx="${q[0]}" cy="${q[1]}" r="3" fill="${C[j%C.length]}"/>`)});svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.innerHTML=s;document.querySelector('#legend').innerHTML=ys.map((yr,j)=>`<span><i class="dot" style="background:${C[j%C.length]}"></i>${yr}</span>`).join('')}document.querySelectorAll('select').forEach(x=>x.onchange=render);render()</script></body></html>'''.replace('__DATA__',payload)
(root/'muestra-zonas-fc.html').write_text(html,encoding='utf-8')
print('Generado: muestra-zonas-fc.html')
