import sys,urllib.parse,urllib.request,re,html
q=' '.join(sys.argv[1:])
req=urllib.request.Request('https://www.bing.com/search?q='+urllib.parse.quote(q)+'&setlang=en-GB&cc=GB',headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept-Language':'en-GB,en;q=0.9'})
t=urllib.request.urlopen(req,timeout=20).read().decode('utf8','ignore')
for m in list(re.finditer(r'<li class="b_algo".*?<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a>(.*?)</li>',t,re.S))[:7]:
    snip=re.sub('<.*?>','',html.unescape(m.group(3)))
    print('*',re.sub('<.*?>','',html.unescape(m.group(2))),'|',m.group(1)); print('  ',snip[:280])
