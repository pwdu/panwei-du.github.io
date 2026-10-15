"""Build static publication markup and the public CV using only Python's standard library.

Run from any directory: python scripts/build_academic_site.py
The public source of truth is docs/assets/publications.json. The private source CV
is deliberately not required or copied into this repository.
"""
from pathlib import Path
import html
import json
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
SOURCE = ROOT / 'site-content'
papers = json.loads((DOCS / 'assets/publications.json').read_text(encoding='utf-8'))
papers.sort(key=lambda p: (-p['year'], p['id']))
e = html.escape

def paper_markup(p):
    link = p['doi'] or 'https://scholar.google.com/scholar?q=' + quote(p['title'])
    label = 'Paper ↗' if p['doi'] else 'Find paper ↗'
    authors = e(p['authors']).replace('Panwei Du', '<strong>Panwei Du</strong>')
    return f'''<article class="paper" data-category="{e(p['category'])}" data-selected="{str(p['selected']).lower()}"><span class="paper-year">{p['year']}</span><div><h3><a href="{e(link)}">{e(p['title'])}</a></h3><p>{authors}</p><p class="venue">{e(p['detail'])}</p></div><a class="paper-link" href="{e(link)}" aria-label="{e(label)}: {e(p['title'])}">{label}</a></article>'''

markup = '\n'.join(paper_markup(p) for p in papers)
def read_content(name):
    return (SOURCE / (name + '.html')).read_text(encoding='utf-8')

page_info = {
    'home': ('Home', 'Panwei Du | AI, Structures & Resilient Infrastructure', 'Panwei Du is a Senior Research Fellow at NTU Singapore. Explore his research overview, current focus and recent highlights.'),
    'research': ('Research', 'Research | Panwei Du', 'Physics-aware AI, structural fire and protective engineering, and sustainable concrete research by Panwei Du.'),
    'publications': ('Publications', 'Publications | Panwei Du', 'Journal papers and ongoing manuscripts by Panwei Du, with publication search, topic filters and BibTeX downloads.'),
    'experience': ('Experience', 'Experience & Teaching | Panwei Du', 'Academic appointments, education, teaching, invited talks and academic service of Panwei Du at NTU Singapore.'),
    'contact': ('Contact', 'Contact | Panwei Du', 'Contact Panwei Du at Nanyang Technological University for research collaboration and academic enquiries.'),
}
layout = read_content('layout')
profiles = read_content('profile-links')
base_url = 'https://pwdu.github.io/panwei-du.github.io/'
for page, (label, title, description) in page_info.items():
    content = read_content(page)
    if page == 'home': content += read_content('highlights')
    content = content.replace('{{PUBLICATIONS}}', markup).replace('{{PROFILE_LINKS}}', profiles)
    if page != 'home':
        # Give each destination a single top-level heading.
        content = re.sub(r'<h2>(.*?)</h2>', r'<h1 class="page-title">\1</h1>', content, count=1, flags=re.S)
        content = re.sub(r'\d{2} / (RESEARCH|PUBLICATIONS|EXPERIENCE|GET IN TOUCH)', r'\1', content)
    if page == 'publications': content = content.replace('id="publication-list"', 'id="publication-list" data-default-filter="all"')
    prefix = './' if page == 'home' else '../'
    def local_link(match):
        url = match.group(2)
        if url.startswith(('#', '/', 'http:', 'https:', 'mailto:', 'data:')): return match.group(0)
        return match.group(1) + prefix + url + '"'
    content = re.sub(r'((?:href|src)=")([^"]+)"', local_link, content)
    navigation = ''.join(f'<a href="{prefix if key == "home" else prefix + key + "/"}"' + (' aria-current="page"' if key == page else '') + f'>{item[0]}</a>' for key, item in page_info.items())
    canonical = base_url + ('' if page == 'home' else page + '/')
    replacements = {'TITLE': e(title), 'DESCRIPTION': e(description), 'CANONICAL': canonical, 'PREFIX': prefix, 'PAGE': page, 'NAV': navigation, 'CONTENT': content}
    output = layout
    for key, value in replacements.items(): output = output.replace('{{' + key + '}}', value)
    folder = DOCS if page == 'home' else DOCS / page
    folder.mkdir(exist_ok=True)
    (folder / 'index.html').write_text(output, encoding='utf-8')

# Build the printable CV from the same editable details as the destination pages.
index = read_content('experience') + read_content('publications')

bib = []
for p in papers:
    # Preserve full author spellings supplied in the CV, in BibTeX author syntax.
    names = [name.strip() for name in p['authors'].replace('§', '').replace(', and ', ', ').replace(' and ', ', ').split(',') if name.strip()]
    authors = ' and '.join(names)
    fields = {'title': p['title'], 'author': authors, 'journal': p['journal'], 'year': str(p['year'])}
    volume = re.search(r' (\d+)(?:,|\s*\()', p['detail'])
    pages = re.search(r':\s*([0-9-]+)', p['detail'])
    if volume: fields['volume'] = volume.group(1)
    if pages: fields['pages'] = pages.group(1).replace('-', '--')
    if p['doi']: fields['doi'] = p['doi'].removeprefix('https://doi.org/')
    bib.append('@article{Du' + str(p['year']) + '_' + str(p['id']) + ',\n' + ',\n'.join('  ' + key + ' = {' + value + '}' for key, value in fields.items()) + '\n}')
(DOCS / 'assets/publications.bib').write_text('\n\n'.join(bib) + '\n', encoding='utf-8')

def extract(pattern):
    match = re.search(pattern, index, flags=re.S)
    if not match: raise ValueError('Missing section: ' + pattern)
    return match.group(1)

appointments = extract(r'<div class="timeline">(.*?)<div class="education">')
education = extract(r'<div class="education">(.*?)</div></div></div></section>')
teaching = extract(r'<div class="teaching-grid">(.*?)</div></section>')
manuscripts = extract(r'<details class="manuscripts">.*?</summary>(.*?)</details>')
cv = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Academic CV | Panwei Du</title><meta name="description" content="Public academic CV of Panwei Du, Senior Research Fellow at Nanyang Technological University, Singapore."><link rel="icon" href="assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css"><script src="assets/site.js" defer></script></head><body><main class="wrap cv"><div class="cv-toolbar"><a class="text-link" href="./">← Back to website</a><button class="print-button">Print / Save as PDF</button></div><p class="eyebrow">PUBLIC ACADEMIC CV · BASED ON AUGUST 2026 CV</p><h1>Panwei Du, PhD</h1><p>Senior Research Fellow · School of Civil and Environmental Engineering<br>Nanyang Technological University, Singapore</p><p class="cv-contact"><a href="mailto:pwdu@ntu.edu.sg">pwdu@ntu.edu.sg</a> · <a href="https://scholar.google.com/citations?user=tJcaQK4AAAAJ&amp;hl=en">Google Scholar</a> · <a href="https://orcid.org/0000-0003-3838-2705">ORCID: 0000-0003-3838-2705</a></p><h2>Research profile</h2><p>I am a civil and structural engineering researcher working at the intersection of computational mechanics, artificial intelligence and resilient infrastructure. My research develops physics-informed and data-driven AI methods, including neural operators, surrogate modelling and transfer learning, for rapid assessment of structural and infrastructure response under fire and blast hazards.</p><p>Research interests: scientific machine learning for civil engineering; structural fire and protective engineering; concrete materials and structures at elevated temperatures; sustainable concrete and composite structural systems.</p><h2>Academic and research appointments</h2>'''
cv += appointments + '<h2>Education</h2>' + education
cv += '<h2>Peer-reviewed journal papers</h2><p>16 journal papers listed in the source CV. § Corresponding author.</p>' + markup
cv += '<h2>Manuscripts in progress</h2>' + manuscripts
cv += '<h2>Teaching, mentoring and academic service</h2>' + teaching
cv += '''<h2>Awards and recognition</h2><ul><li>Dean’s List with Academic Excellence Award, AY2012–13, AY2013–14 and AY2015–16.</li><li>IStructE Gold Medal cum Book Prize, AY2015–16.</li><li>Continental Steel Book Prize, AY2015–16.</li><li>Singapore Concrete Institute Book Prize, AY2015–16.</li></ul><h2>Computational and AI skills</h2><p>PyTorch, TensorFlow, Scikit-learn; physics-informed neural networks, neural operators and graph neural networks; Python, NumPy, SciPy, Pandas, HDF5 and Matplotlib; Abaqus and MATLAB.</p><p class="small muted">This public CV is adapted from the August 2026 source CV. Personal telephone numbers and referee contact details are omitted.</p></main></body></html>'''
(DOCS / 'cv.html').write_text(cv, encoding='utf-8')

# Retain common links from the former Academic Pages site.
redirects = {'about': '../', 'cv': '../cv.html', 'teaching': '../experience/#teaching', 'talks': '../experience/#teaching', 'portfolio': '../research/'}
for path, destination in redirects.items():
    folder = DOCS / path
    folder.mkdir(exist_ok=True)
    (folder / 'index.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={destination}"><title>Panwei Du</title></head><body><a href="{destination}">Continue to Panwei Du’s website</a></body></html>', encoding='utf-8')

for legacy in (ROOT / '_publications').glob('*.md'):
    match = re.search(r'^permalink:\s*(/publication/[^\s]+)', legacy.read_text(encoding='utf-8'), flags=re.M)
    if match:
        folder = DOCS / match.group(1).strip('/')
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=../../publications/"><title>Publications | Panwei Du</title></head><body><a href="../../publications/">View publications</a></body></html>', encoding='utf-8')

(DOCS / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://pwdu.github.io/panwei-du.github.io/sitemap.xml\n', encoding='utf-8')
urls = [base_url + ('' if page == 'home' else page + '/') for page in page_info] + [base_url + 'cv.html']
(DOCS / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>' + url + '</loc></url>' for url in urls) + '</urlset>', encoding='utf-8')
print(f'Built {len(page_info)} pages, {len(papers)} papers, BibTeX, public CV and legacy redirects in {DOCS}')
