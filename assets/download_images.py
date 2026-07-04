import urllib.request, os
os.makedirs('assets', exist_ok=True)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
images = {
 'hero':'https://source.unsplash.com/1600x900/?hospital,safety',
 'school':'https://source.unsplash.com/1200x800/?school,safety',
 'construction':'https://source.unsplash.com/1200x800/?construction,safety',
 'oilgas':'https://source.unsplash.com/1200x800/?oil,gas,safety'
}
fallback = 'https://picsum.photos/{w}/{h}?random={r}'
for name,url in images.items():
    out = os.path.join('assets', f'{name}.jpg')
    tried = []
    success = False
    for attempt, u in enumerate([url, fallback.format(w=1600 if name=='hero' else 1200, h=900 if name=='hero' else 800, r=attempt+1)],1):
        tried.append(u)
        req = urllib.request.Request(u, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
                with open(out,'wb') as f:
                    f.write(data)
            print('saved', out)
            success = True
            break
        except Exception as e:
            print('failed', u, str(e))
    if not success:
        print('all attempts failed for', name, 'tried:', tried)
