#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def clamp(x,a,b): return max(a,min(b,x))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);a=ap.parse_args()
    d=json.loads(Path(a.input).read_text(encoding='utf-8'))
    if d.get('red_flags'):
        print(json.dumps({'score':0,'band':'urgent_review','advice':'Stop self-directed training and seek medical assessment.'},ensure_ascii=False,indent=2));return
    sleep=clamp(float(d.get('sleep_hours',7)),0,10)
    quality=clamp(float(d.get('sleep_quality',3)),1,5)
    soreness=clamp(float(d.get('soreness',2)),1,5)
    stress=clamp(float(d.get('stress',2)),1,5)
    energy=clamp(float(d.get('energy',3)),1,5)
    pain=clamp(float(d.get('pain',0)),0,10)
    score=25*(sleep/8)+15*((quality-1)/4)+20*((5-soreness)/4)+15*((5-stress)/4)+15*((energy-1)/4)+10*((10-pain)/10)
    if 'hrv_deviation_pct' in d:
        score+=clamp(float(d['hrv_deviation_pct'])/10,-1,1)*5
    score=round(clamp(score,0,100),1)
    if score>=80: band='full_training';advice='Proceed with planned training; keep normal progression.'
    elif score>=60: band='monitor';advice='Train as planned but reduce one set if warm-up feels poor.'
    elif score>=40: band='reduce';advice='Reduce volume/intensity by about 20-40% and prioritize technique.'
    else: band='rest_or_refer';advice='Rest or use light activity; reassess and seek professional input if symptoms persist.'
    print(json.dumps({'score':score,'band':band,'advice':advice,'note':'Heuristic only; not a medical or diagnostic score.'},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
