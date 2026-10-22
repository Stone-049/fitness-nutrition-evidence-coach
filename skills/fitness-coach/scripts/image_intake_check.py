#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True)
    a=ap.parse_args()
    d=json.loads(Path(a.input).read_text(encoding='utf-8'))
    reasons=[]
    warnings=[]
    if not d.get('adult_verified'): reasons.append('adult_verified must be true')
    if not d.get('consent'): reasons.append('explicit consent is required')
    if d.get('purpose')!='fitness_analysis': reasons.append('purpose must be fitness_analysis')
    if d.get('sexually_explicit'): reasons.append('explicit or sexualized images are not accepted')
    if d.get('intimate_focus'): reasons.append('intimate/genital focus is not accepted')
    if d.get('minor_present'): reasons.append('no minors may be present')
    views=d.get('views',[])
    if len(views)<1: reasons.append('at least one body view is required')
    elif len(views)<3: warnings.append('front, side, and back views improve confidence')
    if not d.get('identity_minimized'): warnings.append('prefer cropping or covering identifying features')
    if not d.get('attire') or 'nude' in str(d.get('attire','')).lower():
        warnings.append('prefer opaque form-fitting athletic clothing; nudity is unnecessary')
    out={'allowed':not reasons,'reasons':reasons,'warnings':warnings,'recommended_views':['front','side','back']}
    print(json.dumps(out,ensure_ascii=False,indent=2))
    sys.exit(0 if not reasons else 2)
if __name__=='__main__': main()
