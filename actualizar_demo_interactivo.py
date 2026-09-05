from pathlib import Path
import re

p=Path(__file__).parent/'informe-detallado-demo.html'
s=p.read_text(encoding='utf-8')
s=s.replace('.controls{padding:14px 18px;margin-bottom:18px}', '.controls{padding:14px 18px;margin-bottom:18px}.yearbar{display:flex;flex-wrap:wrap;gap:7px;padding:13px 18px;margin-bottom:18px;background:white;border:1px solid var(--line);border-radius:14px}.year{border:1px solid var(--line);background:white;border-radius:99px;padding:5px 10px;cursor:pointer;font-weight:750}.year.off{opacity:.28;text-decoration:line-through}.zone-row{display:grid;grid-template-columns:55px 1fr;gap:10px;align-items:center;margin:12px 0}.zone-row .zones{margin:0}')
s=re.sub(r'<section class="controls">.*?</section>','<section class="yearbar"><strong>Años visibles:</strong><span id="yearButtons"></span></section>',s,count=1)
s=re.sub(r'<div class="zones"><div style="width:18%;.*?</div></div><p class="note">Ejemplo ficticio:.*?</p>','<div id="zoneRows"></div><p class="note">Distribución ficticia por año. Pulsar un año arriba oculta también su barra.</p>',s,count=1)
s=s.replace('ALL=[2019,2020,2021,2022,2023,2024,2025,2026];function wave','ALL=[2019,2020,2021,2022,2023,2024,2025,2026];let hidden=new Set();function wave')
s=re.sub(r'function years\(\)\{.*?\}function fmt','function years(){return ALL.filter(y=>!hidden.has(y))}function fmt',s,count=1)
old="function render(){line('#vo2','vo2','#l1');line('#load','load','#l2');line('#hrv','hrv','#l3');line('#rhr','rhr','#l4');scatter()}document.querySelector('#years').onchange=render;render();"
new="""function renderZones(ys){document.querySelector('#zoneRows').innerHTML=ys.map(y=>{let z1=17+(y-2019)%5,z2=49-(y-2019)%4,z3=20,z4=10,z5=100-z1-z2-z3-z4;return `<div class="zone-row"><b>${y}</b><div class="zones"><div style="width:${z1}%;background:#8799a5">Z1 ${z1}%</div><div style="width:${z2}%;background:#2a9d70">Z2 ${z2}%</div><div style="width:${z3}%;background:#e0a326">Z3 ${z3}%</div><div style="width:${z4}%;background:#e66c3c">Z4 ${z4}%</div><div style="width:${z5}%;background:#bf3b53">Z5 ${z5}%</div></div></div>`}).join('')}
function render(){document.querySelector('#yearButtons').innerHTML=ALL.map((y,j)=>`<button class="year ${hidden.has(y)?'off':''}" data-year="${y}"><i class="dot" style="display:inline-block;background:${COLORS[j%COLORS.length]}"></i>${y}</button>`).join(' ');line('#vo2','vo2','#l1');line('#load','load','#l2');line('#hrv','hrv','#l3');line('#rhr','rhr','#l4');scatter();renderZones(years())}document.addEventListener('click',e=>{let b=e.target.closest('[data-year]');if(b){let y=+b.dataset.year;hidden.has(y)?hidden.delete(y):hidden.add(y);render()}});render();"""
if old not in s:
    raise SystemExit('No se encontró el bloque interactivo esperado')
s=s.replace(old,new)
p.write_text(s,encoding='utf-8')
print('Informe detallado actualizado')
