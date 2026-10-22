#!/usr/bin/env python3
import argparse, json, re
from collections import Counter
from pathlib import Path
import yaml

KEYWORDS={
 'fitness':['fitness','workout','exercise','strength','muscle','hypertrophy','mobility','flexibility','running','cycling','endurance','athlete','sports','rehab','pain','injury','posture','anatomy','physiology','coach','trainer','gym'],
 'nutrition':['nutrition','diet','food','protein','carb','fat','calorie','supplement','meal','eating','obesity','metabolic','vitamin','mineral','hydration','gut','microbiome'],
 'health':['health','wellness','sleep','stress','mental','depression','anxiety','medical','clinical','disease','chronic','aging','recovery','readiness','hrv','biomarker','wearable'],
 'research':['research','paper','review','meta-analysis','journal','academic','evidence','citation','literature'],
 'skill':['skill','agent','prompt','workflow','template','evaluation']
}

def main():
 ap=argparse.ArgumentParser(description='Inventory and classify local GitHub skill repositories.')
 ap.add_argument('--root',required=True)
 ap.add_argument('--output',required=True)
 a=ap.parse_args();root=Path(a.root);rows=[]
 for p in root.rglob('SKILL.md'):
  text=p.read_text(encoding='utf-8',errors='replace');name='';desc=''
  m=re.match(r'^---\s*\n(.*?)\n---',text,re.S)
  if m:
   try:
    fm=yaml.safe_load(m.group(1)) or {};name=str(fm.get('name',''));desc=str(fm.get('description',''))
   except Exception: pass
  blob=(str(p)+' '+name+' '+desc).lower()
  cats={k:[w for w in ws if w in blob] for k,ws in KEYWORDS.items()}
  rows.append({'repo':p.relative_to(root).parts[0] if p.relative_to(root).parts else '', 'path':str(p.relative_to(root)), 'name':name,'description':desc,'categories':{k:v for k,v in cats.items() if v},'score':sum(len(v) for v in cats.values())})
 Path(a.output).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'skills':len(rows),'repos':dict(Counter(r['repo'] for r in rows)),'domain_relevant':sum(1 for r in rows if set(r['categories'])&{'fitness','nutrition'})},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
