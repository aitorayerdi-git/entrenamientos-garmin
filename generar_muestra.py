from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = max((ROOT / "datos garmin").rglob("*.csv"), key=lambda p: p.stat().st_mtime)
OUTPUT = ROOT / "muestra-graficos.html"


def clean(text: str) -> str:
    return (text or "").replace("\xad", "")


def number(text: str) -> float | None:
    text = clean(text).strip()
    if not text or text == "--":
        return None
    try:
        return float(text.replace(".", "").replace(",", "."))
    except ValueError:
        return None


def seconds(text: str) -> float | None:
    text = clean(text).strip().replace(",", ".")
    if not text or text == "--":
        return None
    try:
        parts = [float(x) for x in text.split(":")]
        return sum(value * 60**index for index, value in enumerate(reversed(parts)))
    except ValueError:
        return None


def family(activity_type: str) -> str:
    value = clean(activity_type).lower()
    if any(x in value for x in ("trail", "carrera", "cinta")):
        return "Carrera total"
    if "cicl" in value:
        return "Ciclismo"
    if "nataci" in value:
        return "Natación"
    if "fuerza" in value:
        return "Fuerza"
    return "Otros"


with SOURCE.open(encoding="utf-8-sig", newline="") as source:
    outer = list(csv.reader(source))

header = next(csv.reader([outer[0][0]])) if len(outer[0]) == 1 else outer[0]
rows = [next(csv.reader([row[0]])) if len(row) == 1 else row for row in outer[1:] if row]

# Garmin repite dos nombres de cabecera. Para esta muestra usamos la primera
# aparición, que corresponde a carrera; se conservan las posiciones originales.
indices = {}
for index, name in enumerate(header):
    indices.setdefault(clean(name), index)


def get(row, name):
    index = indices.get(name)
    return clean(row[index]) if index is not None and index < len(row) else ""


activities = []
for row in rows:
    try:
        date = datetime.fromisoformat(get(row, "Fecha"))
    except ValueError:
        continue
    duration = seconds(get(row, "Tiempo en movimiento")) or seconds(get(row, "Tiempo"))
    distance = number(get(row, "Distancia"))
    heart_rate = number(get(row, "Frecuencia cardiaca media"))
    speed = distance / (duration / 3600) if distance and duration else None
    activities.append({
        "y": date.year,
        "m": date.month,
        "type": get(row, "Tipo de actividad"),
        "family": family(get(row, "Tipo de actividad")),
        "hours": duration / 3600 if duration else 0,
        "distance": distance or 0,
        "ascent": number(get(row, "Ascenso total")) or 0,
        "hr": heart_rate,
        "speed": speed,
        "te": number(get(row, "TE aeróbico")),
    })

payload = json.dumps(activities, ensure_ascii=False, separators=(",", ":"))
updated = datetime.now().strftime("%d/%m/%Y %H:%M")
data_updated = datetime.fromtimestamp(SOURCE.stat().st_mtime).strftime("%d/%m/%Y %H:%M")

html = r'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Evolución anual · Entrenamientos Garmin</title>
<style>
:root{--bg:#f4f7f6;--card:#fff;--ink:#17212b;--muted:#65727e;--green:#087f5b;--line:#dce5e1}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,"Segoe UI",sans-serif}main{width:min(1260px,calc(100% - 28px));margin:28px auto 60px}header{display:flex;justify-content:space-between;gap:20px;align-items:end;margin-bottom:24px}h1{font-size:clamp(2rem,5vw,3.6rem);line-height:1;margin:.2rem 0}.eyebrow{color:var(--green);font-weight:800;text-transform:uppercase;letter-spacing:.08em}.muted{color:var(--muted)}.controls,.card{background:var(--card);border:1px solid var(--line);border-radius:16px;box-shadow:0 8px 30px #163b2c0b}.controls{display:flex;flex-wrap:wrap;gap:16px;padding:16px;margin-bottom:18px}.control{display:grid;gap:5px;min-width:180px}.control label{font-size:.78rem;font-weight:800;color:var(--muted);text-transform:uppercase}select{padding:9px 34px 9px 10px;border:1px solid #cdd9d4;border-radius:9px;background:white;color:var(--ink)}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.card{padding:20px;min-width:0}.wide{grid-column:1/-1}.card h2{margin:0;font-size:1.25rem}.chart-head{display:flex;justify-content:space-between;gap:15px;align-items:start}.value{color:var(--green);font-size:.82rem;font-weight:700}svg{width:100%;height:350px;display:block;overflow:visible}.axis{stroke:#afbeb7;stroke-width:1}.gridline{stroke:#e8eeeb;stroke-width:1}.axistext{fill:#738078;font-size:11px}.legend{display:flex;flex-wrap:wrap;gap:7px 14px;margin-top:5px}.legend span{display:inline-flex;align-items:center;gap:5px;font-size:.78rem}.dot{width:9px;height:9px;border-radius:50%}.tip{position:fixed;display:none;pointer-events:none;background:#17212b;color:#fff;padding:7px 9px;border-radius:7px;font-size:12px;z-index:3}table{width:100%;border-collapse:collapse;margin-top:12px}th,td{padding:9px 10px;border-bottom:1px solid var(--line);text-align:right}th:first-child,td:first-child{text-align:left}th{color:var(--muted);font-size:.76rem;text-transform:uppercase}.note{margin:12px 0 0;color:var(--muted);font-size:.82rem}@media(max-width:820px){header{display:block}.grid{grid-template-columns:1fr}.wide{grid-column:auto}svg{height:310px}}
</style></head><body><main>
<header><div><div class="eyebrow">Garmin · comparación anual</div><h1>Evolución de entrenamiento</h1><div class="muted">Datos actualizados: __DATA_UPDATED__ · Enero–diciembre · una línea por año</div></div><span><a href="actualizar-informes.html">Actualizar informes</a> · <a href="diario.html">Ver diario</a></span></header>
<section class="controls"><div class="control"><label for="sport">Actividad</label><select id="sport"><option>Carrera total</option><option>Trail running</option><option>Ciclismo</option><option>Natación</option><option>Fuerza</option><option>Todos</option></select></div><div class="control"><label for="load">Nivel de entrenamiento</label><select id="load"><option value="hours">Horas mensuales</option><option value="distance">Distancia mensual</option><option value="sessions">Sesiones mensuales</option><option value="ascent">Desnivel mensual</option></select></div><div class="control"><label for="performance">Rendimiento</label><select id="performance"><option value="efficiency">Velocidad / pulso</option><option value="speed">Velocidad media</option><option value="hr">Pulso medio</option><option value="te">Efecto aeróbico medio</option></select></div><div class="control"><label for="years">Años visibles</label><select id="years"><option value="all">Todos</option><option value="5">Últimos 5</option><option value="3">Últimos 3</option></select></div></section>
<div class="grid"><section class="card"><div class="chart-head"><div><h2>Nivel de entrenamiento</h2><div class="muted" id="loadSub"></div></div></div><svg id="loadChart"></svg><div class="legend" id="legend1"></div></section><section class="card"><div class="chart-head"><div><h2>Rendimiento</h2><div class="muted" id="perfSub"></div></div></div><svg id="perfChart"></svg><div class="legend" id="legend2"></div><p class="note">La eficiencia divide la velocidad por el pulso medio. Úsala para comparar sesiones del mismo deporte y terreno similar.</p></section><section class="card wide"><div class="chart-head"><div><h2>Resumen por año</h2><div class="muted">Carga acumulada y rendimiento medio del filtro seleccionado</div></div></div><div style="overflow:auto"><table><thead><tr><th>Año</th><th>Sesiones</th><th>Horas</th><th>Distancia</th><th>Desnivel</th><th>Velocidad</th><th>Pulso</th><th>Eficiencia</th></tr></thead><tbody id="summary"></tbody></table></div></section></div>
<p class="note">Generado __UPDATED__. Los meses sin actividad se dejan sin línea. Los datos futuros de 2026 se muestran hasta la fecha disponible.</p></main><div class="tip" id="tip"></div>
<script>const DATA=__DATA__;const MONTHS=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];const COLORS=['#087f5b','#d9485f','#3468c0','#e28413','#744fc6','#008da8','#8c6d31','#444'];
const $=s=>document.querySelector(s);function filtered(){let s=$('#sport').value,d=DATA;if(s==='Trail running')d=d.filter(x=>x.type==='Trail running');else if(s!=='Todos')d=d.filter(x=>x.family===s);let ys=[...new Set(d.map(x=>x.y))].sort((a,b)=>a-b),n=$('#years').value;if(n!=='all')ys=ys.slice(-+n);return {d:d.filter(x=>ys.includes(x.y)),ys}}
function aggregate(){const {d,ys}=filtered(),map={};ys.forEach(y=>map[y]=Array.from({length:12},()=>({sessions:0,hours:0,distance:0,ascent:0,sw:0,hw:0,te:0,tec:0})));d.forEach(x=>{let a=map[x.y][x.m-1];a.sessions++;a.hours+=x.hours;a.distance+=x.distance;a.ascent+=x.ascent;if(x.speed&&x.hr){a.sw+=x.speed*x.hours;a.hw+=x.hr*x.hours}if(x.te){a.te+=x.te;a.tec++}});Object.values(map).flat().forEach(a=>{a.speed=a.hours?a.sw/a.hours:null;a.hr=a.hours?a.hw/a.hours:null;a.efficiency=a.speed&&a.hr?a.speed/a.hr:null;a.te=a.tec?a.te/a.tec:null});return {map,ys,d}}
function fmt(v,key){if(v==null||!isFinite(v))return '—';if(key==='hours')return v.toFixed(1)+' h';if(key==='distance'||key==='speed')return v.toFixed(1)+' km'+(key==='speed'?'/h':'');if(key==='ascent')return Math.round(v).toLocaleString('es-ES')+' m';if(key==='hr')return Math.round(v)+' ppm';if(key==='efficiency')return v.toFixed(3);if(key==='te')return v.toFixed(1);return Math.round(v).toString()}
function chart(id,key,ys,map,legend){const svg=$(id),W=600,H=330,p={l:48,r:12,t:18,b:35},vals=ys.flatMap(y=>map[y].map(a=>a[key])).filter(v=>v!=null&&isFinite(v)),max=Math.max(...vals,1),min=key==='hr'?Math.min(...vals)*.92:0,x=i=>p.l+i*(W-p.l-p.r)/11,y=v=>H-p.b-(v-min)/(max-min||1)*(H-p.t-p.b);let s='';for(let i=0;i<5;i++){let yy=p.t+i*(H-p.t-p.b)/4,v=max-i*(max-min)/4;s+=`<line class="gridline" x1="${p.l}" y1="${yy}" x2="${W-p.r}" y2="${yy}"/><text class="axistext" x="${p.l-7}" y="${yy+4}" text-anchor="end">${fmt(v,key).replace(/ .*/,'')}</text>`}MONTHS.forEach((m,i)=>s+=`<text class="axistext" x="${x(i)}" y="${H-10}" text-anchor="middle">${m}</text>`);ys.forEach((yr,j)=>{let points=[],segments=[];map[yr].forEach((a,i)=>{let v=a[key];if(v==null){if(points.length)segments.push(points);points=[]}else points.push([x(i),y(v),i,v])});if(points.length)segments.push(points);segments.forEach(q=>s+=`<polyline fill="none" stroke="${COLORS[j%COLORS.length]}" stroke-width="2.4" points="${q.map(z=>z[0]+','+z[1]).join(' ')}"/>`);segments.flat().forEach(q=>s+=`<circle cx="${q[0]}" cy="${q[1]}" r="3.5" fill="${COLORS[j%COLORS.length]}" data-tip="${yr} · ${MONTHS[q[2]]}: ${fmt(q[3],key)}"/>`)});svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.innerHTML=s;$(legend).innerHTML=ys.map((yr,j)=>`<span><i class="dot" style="background:${COLORS[j%COLORS.length]}"></i>${yr}</span>`).join('')}
function render(){let {map,ys,d}=aggregate(),lk=$('#load').value,pk=$('#performance').value;$('#loadSub').textContent=$('#load').selectedOptions[0].text;$('#perfSub').textContent=$('#performance').selectedOptions[0].text;chart('#loadChart',lk,ys,map,'#legend1');chart('#perfChart',pk,ys,map,'#legend2');$('#summary').innerHTML=ys.slice().reverse().map(y=>{let a=d.filter(x=>x.y===y),h=a.reduce((s,x)=>s+x.hours,0),dist=a.reduce((s,x)=>s+x.distance,0),asc=a.reduce((s,x)=>s+x.ascent,0),valid=a.filter(x=>x.speed&&x.hr),speed=valid.length?valid.reduce((s,x)=>s+x.speed*x.hours,0)/valid.reduce((s,x)=>s+x.hours,0):null,hr=valid.length?valid.reduce((s,x)=>s+x.hr*x.hours,0)/valid.reduce((s,x)=>s+x.hours,0):null;return `<tr><td>${y}</td><td>${a.length}</td><td>${fmt(h,'hours')}</td><td>${fmt(dist,'distance')}</td><td>${fmt(asc,'ascent')}</td><td>${fmt(speed,'speed')}</td><td>${fmt(hr,'hr')}</td><td>${fmt(speed&&hr?speed/hr:null,'efficiency')}</td></tr>`}).join('')}
document.querySelectorAll('select').forEach(x=>x.addEventListener('change',render));document.addEventListener('mouseover',e=>{if(e.target.dataset.tip){let t=$('#tip');t.textContent=e.target.dataset.tip;t.style.display='block'}});document.addEventListener('mousemove',e=>{let t=$('#tip');t.style.left=e.clientX+12+'px';t.style.top=e.clientY+12+'px'});document.addEventListener('mouseout',e=>{if(e.target.dataset.tip)$('#tip').style.display='none'});render();</script></body></html>'''

OUTPUT.write_text(html.replace("__DATA__", payload).replace("__UPDATED__", updated).replace("__DATA_UPDATED__", data_updated), encoding="utf-8")
portal = ROOT / "informe-inmediato.html"
if portal.exists():
    content = portal.read_text(encoding="utf-8")
    content = re.sub(r"<!--DATA_DATE-->.*?<!--/DATA_DATE-->", f"<!--DATA_DATE-->Datos actualizados: {data_updated}<!--/DATA_DATE-->", content)
    portal.write_text(content, encoding="utf-8")
print(f"Generado: {OUTPUT.name} ({len(activities)} actividades)")
