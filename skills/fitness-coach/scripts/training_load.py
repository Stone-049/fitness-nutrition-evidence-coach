#!/usr/bin/env python3
import argparse, json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);a=ap.parse_args()
    rows=json.loads(Path(a.input).read_text(encoding='utf-8'))
    byday=defaultdict(float);details=[]
    for r in rows:
        date=datetime.fromisoformat(r['date']).date()
        duration=float(r.get('duration_min',0));rpe=float(r.get('rpe',0))
        volume=0
        for ex in r.get('exercises',[]):
            volume+=float(ex.get('weight',0))*sum(float(x) for x in ex.get('reps',[]))
        session_load=duration*rpe
        byday[date]+=session_load
        details.append({'date':str(date),'session_load':session_load,'volume_load':volume,'type':r.get('type','unknown')})
    if not byday:
        print(json.dumps({'error':'no sessions'},indent=2));return
    end=max(byday);start=end-timedelta(days=27)
    acute=sum(v for d,v in byday.items() if d>end-timedelta(days=7))
    chronic=sum(v for d,v in byday.items() if d>=start)/4
    ratio=round(acute/chronic,2) if chronic else None
    weekly=round(sum(v for d,v in byday.items() if d>end-timedelta(days=7)),1)
    print(json.dumps({'window_end':str(end),'session_count':len(rows),'training_days':len(byday),'weekly_load':weekly,'acute_7d':round(acute,1),'chronic_28d_weekly_average':round(chronic,1),'acute_chronic_ratio':ratio,'warning':'ACWR is unreliable with sparse or irregular data; require a consistent 28-day log.' if len(byday)<8 else None,'interpretation':'ratio is a monitoring heuristic, not a diagnosis'},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
