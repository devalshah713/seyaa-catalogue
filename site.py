#!/usr/bin/env python3
"""Seyaa Jewels Inc. — trade catalogue website (single self-contained HTML)."""
import base64, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
b64 = lambda p: base64.b64encode(open(os.path.join(ROOT, p), 'rb').read()).decode()

DATA = json.load(open(os.path.join(ROOT, 'site_data.json')))
EMBLEM = b64('assets/mark_web.png')
WORD = b64('assets/word_web.png')
QR = b64('assets/wa_qr.png')

ORDER = ['Round Tennis Bracelet', 'All Mix Fancy Bracelet',
         'Straight Line Tennis Necklace', 'Graduated Tennis Necklace',
         'Round Studs \u2014 Basket Setting', 'Round Studs \u2014 Martini Setting',
         'Eternity Bands']

BLURB = {
 'Round Tennis Bracelet': 'The classic four-prong line bracelet. Uniform round brilliants set edge to edge on a flexible link that sits flat on the wrist.',
 'All Mix Fancy Bracelet': 'Alternating fancy shapes set in a continuous line, for more movement and light return than a round line.',
 'Straight Line Tennis Necklace': 'A single uniform line of round brilliants carried around the neck, finished with a concealed box clasp.',
 'Graduated Tennis Necklace': 'Stones graduate from the clasp to the largest centres at the front, giving the line a tapered drape.',
 'Round Studs \u2014 Basket Setting': 'Round brilliants in an open four-prong basket. The lifted gallery lets light through the pavilion.',
 'Round Studs \u2014 Martini Setting': 'A low three-prong mount that sets the stone close to the ear, lighter in gold than the basket.',
 'Eternity Bands': 'Round brilliants in a continuous shared-prong circuit. Supplied in US size 7 as standard.',
}
FIXED = {
 'Round Tennis Bracelet': '7 inch \u00b7 Box clasp with safety catch',
 'All Mix Fancy Bracelet': '7 inch \u00b7 Box clasp with safety catch',
 'Straight Line Tennis Necklace': '16.5 inch \u00b7 Box clasp with safety catch',
 'Graduated Tennis Necklace': '16.5 inch \u00b7 Box clasp with safety catch',
 'Round Studs \u2014 Basket Setting': 'Four-prong basket \u00b7 Push back',
 'Round Studs \u2014 Martini Setting': 'Three-prong martini \u00b7 Push back',
 'Eternity Bands': 'US size 7 \u00b7 Shared prong',
}


def ct(t):
    m = re.match(r'([\d.]+)', t)
    return m.group(1) if m else ''


def size_of(it):
    s = str(it.get('size') or '').strip()
    return '\u2014' if s in ('', 'None', 'NA') else s.replace('INCH', 'in')


payload = []
for sec in ORDER:
    items = []
    for it in DATA[sec]:
        items.append({
            'ct': ct(it['title']),
            'tcw': str(it.get('tcw') or '\u2014'),
            'stones': str(int(float(it['stones']))) if it.get('stones') else '\u2014',
            'shape': (it.get('shape') or '').strip().title() or '\u2014',
            'gold': str(it.get('gold') or '\u2014'),
            'size': size_of(it),
            'color': str(it.get('color') or '\u2014'),
            'clarity': str(it.get('clarity') or '\u2014'),
            'skuW': it.get('skuW', '\u2014'),
            'skuY': it.get('skuY', '\u2014'),
            'imgW': it.get('imgW', []),
            'imgY': it.get('imgY', []),
        })
    payload.append({'name': sec, 'slug': re.sub(r'[^a-z0-9]+', '-', sec.lower()).strip('-'),
                    'blurb': BLURB[sec], 'fixed': FIXED[sec], 'items': items})

JSON = json.dumps(payload, separators=(',', ':'))

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Seyaa Jewels Inc. &mdash; Trade Catalogue 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Allura&family=Montserrat:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#1C1C1C; --panel:#232323; --panel2:#2A2A2A; --line:#333;
  --paper:#fff; --muted:#9A9A9A; --dim:#CFCFCF; --accent:#DD611C;
  --script:'Allura', cursive; --sans:'Montserrat', system-ui, -apple-system, 'Segoe UI', sans-serif;
  box-sizing:border-box; padding-top:env(safe-area-inset-top,0px); padding-bottom:env(safe-area-inset-bottom,0px);
}
*,*::before,*::after{box-sizing:inherit}
html{background:var(--ink);scroll-behavior:smooth; scroll-padding-top:calc(64px + env(safe-area-inset-top,0px))}
body{margin:0;background:var(--ink);color:var(--paper);font-family:var(--sans);font-weight:300;
  -webkit-font-smoothing:antialiased;line-height:1.6}
img{max-width:100%;display:block}
a{color:inherit}

.bar{position:fixed;inset:0 0 auto 0;z-index:60;background:rgba(28,28,28,.94);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--line);
  padding-top:env(safe-area-inset-top,0px)}
.bar-in{max-width:1240px;margin:0 auto;padding:10px 20px;display:flex;align-items:center;gap:18px}
.bar .mark{display:flex;align-items:center;gap:9px;text-decoration:none;flex:none}
.bar .mark .m{height:30px;width:auto}
.bar .mark .w{height:17px;width:auto}
.navscroll{overflow-x:auto;scrollbar-width:none;-ms-overflow-style:none;flex:1}
.navscroll::-webkit-scrollbar{display:none}
nav{display:flex;gap:16px;white-space:nowrap}
nav a{font-size:11px;letter-spacing:.11em;text-transform:uppercase;color:var(--dim);
  text-decoration:none;padding:6px 0;border-bottom:1px solid transparent;transition:.2s}
nav a:hover{color:var(--accent);border-color:var(--accent)}

.hero{min-height:88vh;display:flex;flex-direction:column;align-items:center;justify-content:center;
  text-align:center;padding:140px 20px 70px;border-bottom:1px solid var(--line)}
.hero .mk{width:118px;margin-bottom:26px}
.hero .wd{width:min(430px,78vw);margin:0 auto}
.hero .sub{letter-spacing:.3em;font-size:11px;text-transform:uppercase;color:var(--dim);margin:14px 0 0}
.hero hr{width:80px;border:0;border-top:1px solid var(--accent);margin:30px auto}
.hero h2{font-weight:400;letter-spacing:.3em;font-size:13px;text-transform:uppercase;margin:0}
.hero .yr{font-family:var(--script);font-size:46px;color:var(--accent);margin-top:2px}
.hero .std{margin-top:40px;font-size:11px;letter-spacing:.17em;text-transform:uppercase;color:var(--muted)}

.intro{max-width:760px;margin:0 auto;padding:76px 24px 10px;text-align:center}
.intro p{color:var(--dim);font-size:15px;margin:0 0 20px}
.standards{display:grid;grid-template-columns:repeat(auto-fit,minmax(118px,1fr));gap:22px;
  margin:44px 0 0;padding:28px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.standards div{text-align:center}
.standards dt{font-size:9.5px;letter-spacing:.17em;text-transform:uppercase;color:var(--accent);font-weight:600}
.standards dd{margin:7px 0 0;font-size:14px}

.collection{max-width:1240px;margin:0 auto;padding:78px 20px 0}
.col-head{text-align:center;max-width:720px;margin:0 auto 42px}
.eyebrow{font-size:10px;letter-spacing:.3em;text-transform:uppercase;color:var(--muted);margin:0}
.col-head h2{font-family:var(--script);font-size:clamp(34px,5.4vw,52px);font-weight:400;margin:8px 0 0;line-height:1.1}
.col-head .rule{width:60px;border-top:1px solid var(--accent);margin:18px auto 22px}
.blurb{color:var(--dim);font-size:14.5px;margin:0}
.fixed{font-size:10.5px;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);margin:16px 0 0}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(236px,1fr));gap:20px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:4px;overflow:hidden;
  cursor:pointer;transition:border-color .2s, transform .2s}
.card:hover,.card:focus-visible{border-color:var(--accent);transform:translateY(-3px);outline:none}
.shot{aspect-ratio:1;background:var(--panel2);position:relative;overflow:hidden}
.shot img{width:100%;height:100%;object-fit:contain}
.ph{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  color:#4A4A4A;font-size:10px;letter-spacing:.17em;text-transform:uppercase;text-align:center;padding:12px}
.meta{padding:15px 16px 17px}
.meta h3{margin:0;font-size:19px;font-weight:600;letter-spacing:.01em}
.skus{margin:3px 0 12px;font-size:10.5px;letter-spacing:.07em;color:var(--accent)}
.meta dl{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0;
  border-top:1px solid var(--line);padding-top:11px}
.meta dt{font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.meta dd{margin:3px 0 0;font-size:12.5px}

.speclist{margin:28px 0 0;border-top:1px solid var(--line)}
.speclist summary{cursor:pointer;padding:16px 0;font-size:10.5px;letter-spacing:.17em;
  text-transform:uppercase;color:var(--muted);list-style:none}
.speclist summary::-webkit-details-marker{display:none}
.speclist summary::before{content:'+ ';color:var(--accent)}
.speclist[open] summary::before{content:'\\2212  '}
.tablewrap{overflow-x:auto;padding-bottom:22px}
table{width:100%;border-collapse:collapse;font-size:13px;min-width:580px}
th{background:var(--panel2);color:var(--accent);font-size:9.5px;letter-spacing:.14em;
  text-transform:uppercase;font-weight:600;padding:11px 10px;text-align:left}
td{padding:10px;border-bottom:1px solid #2A2A2A}
td.sku{color:var(--dim);font-size:12px}

.contact{max-width:760px;margin:0 auto;padding:96px 24px 60px;text-align:center}
.contact img.logo{width:88px;margin:0 auto 20px}
.contact .wordc{width:min(330px,70vw);margin:0 auto}
.contact .sub{letter-spacing:.26em;font-size:10px;text-transform:uppercase;color:var(--muted);margin:18px 0 0}
.contact hr{width:70px;border:0;border-top:1px solid var(--accent);margin:28px auto 34px}
.blk{margin:0 0 30px}
.blk .lbl{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);font-weight:600;margin:0 0 9px}
.blk p{margin:0;font-size:15px;line-height:1.75}
.blk a{text-decoration:none;border-bottom:1px solid var(--line)}
.blk a:hover{border-color:var(--accent)}
.qr{display:inline-block;background:#fff;padding:9px;border-radius:5px;margin-top:6px}
.qr img{width:124px}
.qrc{font-size:9.5px;letter-spacing:.17em;text-transform:uppercase;color:var(--muted);margin:11px 0 0}
footer{border-top:1px solid var(--line);margin-top:48px;padding:26px 0 10px;
  font-size:10px;letter-spacing:.17em;text-transform:uppercase;color:#6E6E6E}

/* lightbox */
.lb{position:fixed;inset:0;z-index:100;background:rgba(14,14,14,.97);display:none;
  overflow-y:auto;padding:calc(26px + env(safe-area-inset-top,0px)) 18px 40px}
.lb.on{display:block}
.lb-in{max-width:1080px;margin:0 auto}
.lb-head{display:flex;align-items:flex-start;justify-content:space-between;gap:18px;margin-bottom:22px}
.lb-head .eyebrow{text-align:left}
.lb-head h3{font-family:var(--script);font-size:42px;font-weight:400;margin:4px 0 0;line-height:1}
.x{background:none;border:1px solid var(--line);color:var(--paper);width:40px;height:40px;
  border-radius:50%;font-size:19px;cursor:pointer;flex:none;line-height:1}
.x:hover{border-color:var(--accent);color:var(--accent)}
.metals{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:22px}
.metal h4{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);
  font-weight:600;margin:0 0 10px}
.big{aspect-ratio:1;background:var(--panel);border:1px solid var(--line);border-radius:4px;
  overflow:hidden;position:relative}
.big img{width:100%;height:100%;object-fit:contain}
.thumbs{display:flex;gap:8px;margin-top:9px;flex-wrap:wrap}
.thumbs button{width:56px;height:56px;padding:0;background:var(--panel);border:1px solid var(--line);
  border-radius:3px;overflow:hidden;cursor:pointer}
.thumbs button.sel{border-color:var(--accent)}
.thumbs img{width:100%;height:100%;object-fit:contain}
.lb-specs{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:20px;
  margin-top:32px;padding:26px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.lb-specs dt{font-size:9.5px;letter-spacing:.15em;text-transform:uppercase;color:var(--accent);font-weight:600}
.lb-specs dd{margin:7px 0 0;font-size:15px}
.lb-foot{margin-top:22px;font-size:11.5px;color:var(--muted);text-align:center}
.cta{display:inline-block;margin-top:20px;padding:12px 26px;border:1px solid var(--accent);
  color:var(--accent);text-decoration:none;font-size:10.5px;letter-spacing:.18em;text-transform:uppercase}
.cta:hover{background:var(--accent);color:var(--ink)}
@media(max-width:620px){
  .bar .mark .w{display:none}
  .hero{min-height:76vh;padding-top:120px}
  .lb-head h3{font-size:34px}
}
</style>
</head>
<body>

<div class="bar"><div class="bar-in">
  <a class="mark" href="#top"><img class="m" src="data:image/png;base64,__EMBLEM__" alt=""><img class="w" src="data:image/png;base64,__WORD__" alt="Seyaa Jewels"></a>
  <div class="navscroll"><nav id="nav"></nav></div>
</div></div>

<header class="hero" id="top">
  <img class="mk" src="data:image/png;base64,__EMBLEM__" alt="">
  <img class="wd" src="data:image/png;base64,__WORD__" alt="Seyaa Jewels">
  <p class="sub">Lab Grown Diamond Jewellery</p>
  <hr>
  <h2>Trade Catalogue</h2>
  <div class="yr">2026</div>
  <p class="std">14K Gold &middot; E-F &middot; VS-SI &middot; IGI Certified &middot; Prices on request</p>
</header>

<section class="intro">
  <p>Seyaa Jewels Inc. manufactures fine jewellery set exclusively with IGI-certified lab grown diamonds. Every piece in this catalogue is produced in-house, from stone selection and setting through to final polish, giving us direct control over quality, consistency and delivery timelines.</p>
  <p>Our range is built for the trade: classic silhouettes in tennis bracelets, necklaces, studs and eternity bands, offered across a full spread of carat weights in 14K yellow and white gold. Specifications are standardised so repeat orders match the first.</p>
  <p>All diamonds are E-F colour, VS-SI clarity. Prices are available on request.</p>
  <dl class="standards">
    <div><dt>Metal</dt><dd>14K Gold</dd></div>
    <div><dt>Colours</dt><dd>Yellow &middot; White</dd></div>
    <div><dt>Diamonds</dt><dd>Lab Grown</dd></div>
    <div><dt>Colour</dt><dd>E-F</dd></div>
    <div><dt>Clarity</dt><dd>VS-SI</dd></div>
    <div><dt>Certification</dt><dd>IGI</dd></div>
  </dl>
</section>

<main id="main"></main>

<section class="contact" id="contact">
  <img class="logo" src="data:image/png;base64,__EMBLEM__" alt="">
  <img class="wordc" src="data:image/png;base64,__WORD__" alt="Seyaa Jewels">
  <p class="sub">Lab Grown Diamond Jewellery</p>
  <hr>
  <div class="blk">
    <p class="lbl">Seyaa Jewels Inc.</p>
    <p>42 West 48th Street, Suite #600<br>New York, NY 10036<br>United States</p>
  </div>
  <div class="blk">
    <p class="lbl">Contact</p>
    <p>Rahul Shah<br>
      <a href="tel:+19178016060">+1 917 801 6060</a><br>
      <a href="mailto:seyaajewels@gmail.com">seyaajewels@gmail.com</a></p>
  </div>
  <a class="qr" href="__WA__" target="_blank" rel="noopener"><img src="data:image/png;base64,__QR__" alt="WhatsApp"></a>
  <p class="qrc">Scan to chat on WhatsApp</p>
  <footer>Prices on request &nbsp;&middot;&nbsp; &copy; 2026 Seyaa Jewels Inc.</footer>
</section>

<div class="lb" id="lb" role="dialog" aria-modal="true"><div class="lb-in" id="lbin"></div></div>

<script>
const DATA = __JSON__;
const WA = "__WA__";
const src = (id,w) => "https://drive.google.com/thumbnail?id=" + id + "&sz=w" + w;

function shot(ids, label, w){
  if(!ids || !ids.length) return '<div class="ph">Image<br>'+label+'</div>';
  return '<img loading="lazy" alt="'+label+'" src="'+src(ids[0],w)+'" '+
         'onerror="this.style.display=\\'none\\';this.insertAdjacentHTML(\\'afterend\\',\\'<div class=&quot;ph&quot;>Image unavailable</div>\\')">';
}

const nav = document.getElementById('nav');
const main = document.getElementById('main');

DATA.forEach(sec => {
  nav.insertAdjacentHTML('beforeend','<a href="#'+sec.slug+'">'+sec.name+'</a>');

  const cards = sec.items.map((it,idx) => {
    const ids = (it.imgW && it.imgW.length) ? it.imgW : it.imgY;
    return '<article class="card" data-sec="'+sec.slug+'" data-i="'+idx+'" tabindex="0">'+
      '<div class="shot">'+shot(ids, it.ct+' ct', 500)+'</div>'+
      '<div class="meta"><h3>'+it.ct+' ct</h3>'+
      '<p class="skus">'+it.skuW+' &nbsp;/&nbsp; '+it.skuY+'</p>'+
      '<dl><div><dt>Stones</dt><dd>'+it.stones+'</dd></div>'+
      '<div><dt>Gold</dt><dd>'+it.gold+' g</dd></div>'+
      '<div><dt>Size</dt><dd>'+it.size+'</dd></div></dl></div></article>';
  }).join('');

  const rows = sec.items.map(it =>
    '<tr><td>'+it.ct+' ct</td><td>'+it.stones+'</td><td>'+it.gold+' g</td><td>'+it.size+'</td>'+
    '<td class="sku">'+it.skuW+'</td><td class="sku">'+it.skuY+'</td></tr>').join('');

  main.insertAdjacentHTML('beforeend',
    '<section class="collection" id="'+sec.slug+'">'+
      '<div class="col-head"><p class="eyebrow">Collection</p><h2>'+sec.name+'</h2>'+
      '<hr class="rule"><p class="blurb">'+sec.blurb+'</p><p class="fixed">'+sec.fixed+'</p></div>'+
      '<div class="grid">'+cards+'</div>'+
      '<details class="speclist"><summary>Full specification table</summary><div class="tablewrap"><table>'+
      '<thead><tr><th>Ct wt</th><th>Stones</th><th>Gold wt</th><th>Size</th><th>SKU &middot; White</th><th>SKU &middot; Yellow</th></tr></thead>'+
      '<tbody>'+rows+'</tbody></table></div></details>'+
    '</section>');
});

/* ---- lightbox ---- */
const lb = document.getElementById('lb'), lbin = document.getElementById('lbin');

function metalBlock(label, ids, sku, key){
  if(!ids || !ids.length)
    return '<div class="metal"><h4>'+label+' &middot; '+sku+'</h4><div class="big"><div class="ph">No image</div></div></div>';
  const thumbs = ids.length > 1 ? '<div class="thumbs">'+ ids.map((id,i) =>
      '<button class="'+(i?'':'sel')+'" data-k="'+key+'" data-id="'+id+'"><img src="'+src(id,120)+'" alt="" onerror="this.style.opacity=0"></button>'
    ).join('') +'</div>' : '';
  return '<div class="metal"><h4>'+label+' &middot; '+sku+'</h4>'+
         '<div class="big"><img id="big-'+key+'" alt="" src="'+src(ids[0],1400)+'" '+
           'onerror="this.style.display=\\'none\\';this.parentElement.insertAdjacentHTML(\\'beforeend\\',\\'<div class=&quot;ph&quot;>Image unavailable</div>\\')"></div>'+
         thumbs+'</div>';
}

function open(sec, idx){
  const s = DATA.find(x => x.slug === sec), it = s.items[idx];
  lbin.innerHTML =
    '<div class="lb-head"><div><p class="eyebrow">'+s.name+'</p><h3>'+it.ct+' Carat</h3></div>'+
    '<button class="x" id="x" aria-label="Close">&times;</button></div>'+
    '<div class="metals">'+ metalBlock('14K White', it.imgW, it.skuW, 'w') +
                             metalBlock('14K Yellow', it.imgY, it.skuY, 'y') +'</div>'+
    '<dl class="lb-specs">'+
      '<div><dt>Total carat weight</dt><dd>'+it.tcw+' ct</dd></div>'+
      '<div><dt>Diamonds</dt><dd>'+it.stones+'</dd></div>'+
      '<div><dt>Shape</dt><dd>'+it.shape+'</dd></div>'+
      '<div><dt>Gold weight</dt><dd>'+it.gold+' g</dd></div>'+
      '<div><dt>Length / size</dt><dd>'+it.size+'</dd></div>'+
      '<div><dt>Colour &middot; clarity</dt><dd>'+it.color+' &middot; '+it.clarity+'</dd></div>'+
    '</dl>'+
    '<p class="lb-foot">14K Gold, yellow or white &middot; Lab grown diamonds &middot; IGI certified &middot; '+s.fixed+
    '<br><a class="cta" href="'+WA+'" target="_blank" rel="noopener">Enquire on WhatsApp</a></p>';
  lb.classList.add('on');
  document.body.style.overflow = 'hidden';
  document.getElementById('x').focus();
}

function close(){ lb.classList.remove('on'); document.body.style.overflow = ''; }

document.addEventListener('click', e => {
  const card = e.target.closest('.card');
  if(card){ open(card.dataset.sec, +card.dataset.i); return; }
  if(e.target.id === 'x' || e.target === lb){ close(); return; }
  const t = e.target.closest('.thumbs button');
  if(t){
    const bigEl = document.getElementById('big-' + t.dataset.k);
    const ph = bigEl.parentElement.querySelector('.ph'); if(ph) ph.remove();
    bigEl.style.display = ''; bigEl.src = src(t.dataset.id, 1400);
    t.parentElement.querySelectorAll('button').forEach(b => b.classList.remove('sel'));
    t.classList.add('sel');
  }
});
document.addEventListener('keydown', e => {
  if(e.key === 'Escape') close();
  if(e.key === 'Enter' && document.activeElement.classList.contains('card')){
    open(document.activeElement.dataset.sec, +document.activeElement.dataset.i);
  }
});
</script>
</body>
</html>
"""

WA = ('https://wa.me/19178016060?text=Hi%2C%20I%27d%20like%20a%20quote%20on%20'
      'your%20lab%20grown%20diamond%20jewellery.')

out = (HTML.replace('__EMBLEM__', EMBLEM)
           .replace('__WORD__', WORD)
           .replace('__QR__', QR)
           .replace('__JSON__', JSON)
           .replace('__WA__', WA))

# Written to both public/ and the repo root so Cloudflare Pages serves the site
# whether its build output directory is set to `public` or left empty.
os.makedirs(os.path.join(ROOT, 'public'), exist_ok=True)
for path in (os.path.join(ROOT, 'public', 'index.html'), os.path.join(ROOT, 'index.html')):
    open(path, 'w', encoding='utf-8').write(out)
    print('written', path, len(out), 'bytes')
