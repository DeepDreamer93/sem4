import sys,urllib.parse,urllib.request,re,html
q=' '.join(sys.argv[1:])
req=urllib.request.Request('https://html.duckduckgo.com/html/?q='+urllib.parse.quote(q),headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'})
t=urllib.request.urlopen(req,timeout=20).read().decode('utf8','ignore')
for m in re.finditer(r'class="result__a" href="([^"]+)".*?>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>',t,re.S)[:0] if False else list(re.finditer(r'class="result__a" href="([^"]+)"[^>]*>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>',t,re.S))[:8]:
    u=m.group(1)
    if 'uddg=' in u: u=urllib.parse.unquote(u.split('uddg=')[1].split('&')[0])
    print('*',re.sub('<.*?>','',html.unescape(m.group(2))),'|',u); print('  ',re.sub('<.*?>','',html.unescape(m.group(3)))[:300])
