import requests

r = 'a839d12a-b123-404c-a1bd-868ecd628975'
c = 0
while True:
    c += 1
    r = requests.get(f"https://crumbs.web.actf.co/{r}")
    if r.text.startswith('actf{'):
        print(r.text)
        break
    r = r.text.split('Go to ')[-1].strip()
    print(c)