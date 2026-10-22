#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
import requests

API='https://www.ebi.ac.uk/europepmc/webservices/rest/search'

def main():
    ap=argparse.ArgumentParser(description='Search Europe PMC for fitness/nutrition evidence.')
    ap.add_argument('--query',required=True)
    ap.add_argument('--limit',type=int,default=10)
    ap.add_argument('--sort',default='CITED desc')
    ap.add_argument('--output')
    a=ap.parse_args()
    try:
        r=requests.get(API,params={'query':a.query,'format':'json','pageSize':min(max(a.limit,1),100),'resultType':'core','sort':a.sort},timeout=60)
        r.raise_for_status(); data=r.json()
    except Exception as e:
        print(json.dumps({'error':str(e)},ensure_ascii=False)); sys.exit(1)
    rows=[]
    for x in data.get('resultList',{}).get('result',[]):
        pubs=x.get('pubTypeList',{}).get('pubType',[])
        rows.append({
            'title':x.get('title'),'authors':x.get('authorString',''),
            'journal':x.get('journalTitle',''),'year':x.get('pubYear',''),
            'pmid':x.get('pmid',''),'doi':x.get('doi',''),
            'pub_types':pubs if isinstance(pubs,list) else [str(pubs)],
            'abstract':x.get('abstractText','')
        })
    report={'query':a.query,'count':len(rows),'results':rows}
    text=json.dumps(report,ensure_ascii=False,indent=2)
    if a.output: Path(a.output).write_text(text,encoding='utf-8')
    else: print(text)

if __name__=='__main__': main()
