import sys,urllib.request,re,html
u=sys.argv[1]; kw=[k.lower() for k in sys.argv[2:]]
req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36'})
t=urllib.request.urlopen(req,timeout=30).read().decode('utf8','ignore')
t=re.sub(r'(?is)<(script|style|nav|header|footer)[^>]*>.*?</\1>','',t)
paras=re.findall(r'(?is)<(?:p|li|h[1-4]|td)[^>]*>(.*?)</(?:p|li|h[1-4]|td)>',t)
out=[]
for p in paras:
    s=re.sub(r'\s+',' ',html.unescape(re.sub('<.*?>','',p))).strip()
    if len(s)>60 and (not kw or any(k in s.lower() for k in kw)): out.append(s)
print('\n'.join(dict.fromkeys(out))[:int(9000)])
