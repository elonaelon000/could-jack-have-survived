"""Finish the story-first exhibit, derived feature guide, and both Pages entry points.

Run after build_exhibit.main(). No registered hypothesis or raw value is changed.
"""
from __future__ import annotations
import hashlib
import io
import json
from pathlib import Path
import re
import urllib.request
from PIL import Image
from analysis import load_data

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
ART_URL = 'https://upload.wikimedia.org/wikipedia/commons/6/6e/St%C3%B6wer_Titanic.jpg'
ART_CREDIT = 'https://commons.wikimedia.org/wiki/File:St%C3%B6wer_Titanic.jpg'


def group(sub, label):
    return {'label': label, 'n': len(sub), 'k': int(sub.Survived.sum())}


def feature_guide():
    d = load_data()
    family = d[(d.Sex == 'male') & (d.Pclass == 3) & d.Age.between(18, 50)]
    ages = d[d.Age.notna()]
    bands = [
        ('0-12', ages.Age <= 12),
        ('>12-<18', (ages.Age > 12) & (ages.Age < 18)),
        ('18-25', ages.Age.between(18, 25)),
        ('>25-40', (ages.Age > 25) & (ages.Age <= 40)),
        ('>40', ages.Age > 40),
    ]
    names = {1: 'First class', 2: 'Second class', 3: 'Third class'}
    ports = [('S', 'Southampton'), ('C', 'Cherbourg'), ('Q', 'Queenstown')]
    return {
        'schema': 'story-first-v2',
        'source': 'Unchanged repository data/train.csv; new descriptive feature guide, not new preregistration.',
        'sha256': hashlib.sha256((ROOT / 'data/train.csv').read_bytes()).hexdigest(),
        'classes': [group(d[d.Pclass == c], names[c]) for c in (1, 2, 3)],
        'young_men': [group(d[(d.Pclass == c) & (d.Sex == 'male') & d.Age.between(18, 30)], names[c]) for c in (1, 2, 3)],
        'sexes': [group(d[d.Sex == s], s.title()) for s in ('female', 'male')],
        'age_bands': [group(ages[mask], label) for label, mask in bands],
        'age_known': len(ages), 'age_missing': int(d.Age.isna().sum()),
        'age_mean': float(ages.Age.mean()), 'age_median': float(ages.Age.median()),
        'family_h3': [group(family[(family.SibSp + family.Parch) == 0], 'None recorded'), group(family[(family.SibSp + family.Parch) > 0], 'Relatives recorded')],
        'ports': [dict(group(d[d.Embarked == code], label), code=code) for code, label in ports],
        'ports_missing': int(d.Embarked.isna().sum()),
        'cabins': [{'label': names[c], 'n': int((d.Pclass == c).sum()), 'missing': int(d.loc[d.Pclass == c, 'Cabin'].isna().sum())} for c in (1, 2, 3)],
        'fare': {'median': float(d.Fare.median()), 'max': float(d.Fare.max())},
        'columns': list(d.columns),
    }


def ensure_art():
    folder = DOCS / 'assets'
    folder.mkdir(exist_ok=True)
    target = folder / 'titanic-1912.jpg'
    if not target.is_file():
        request = urllib.request.Request(ART_URL, headers={'User-Agent': 'TitanicDataExhibit/2.0 (educational; github.com/elonaelon000/could-jack-have-survived)'})
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read(10 * 1024 * 1024)
        with Image.open(io.BytesIO(raw)) as original:
            image = original.convert('RGB')
            image.thumbnail((1600, 1600))
            image.save(target, 'JPEG', quality=88, optimize=True)
    with Image.open(target) as image:
        assert image.width >= 900 and image.height > 500, 'Hero artwork is unexpectedly small.'
    (folder / 'ATTRIBUTION.md').write_text(
        '# Hero artwork\n\nWilly Stower, 1912: Titanic sinking.\n'
        'Public-domain reproduction, Wikimedia Commons.\n'
        f'Source: {ART_CREDIT}\nOriginal: {ART_URL}\n\n'
        'Resized as JPEG for web delivery. Color treatment and crop are applied in CSS.\n'
        'This is a historical artistic interpretation, not a photograph, film still, or reconstruction of rescue geography.\n', encoding='utf-8')


def main():
    guide = feature_guide()
    assert sum(r['n'] for r in guide['age_bands']) == guide['age_known'] == 714
    assert sum(r['n'] for r in guide['ports']) + guide['ports_missing'] == 891
    assert len(guide['columns']) == 12
    ensure_art()
    (DOCS / 'feature-guide.json').write_text(json.dumps(guide, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    path = DOCS / 'index.html'
    page = path.read_text(encoding='utf-8')
    extra = '<script>window.JACK_GUIDE=' + json.dumps(guide, separators=(',', ':'), allow_nan=False) + ';</script>\n<script>' + (ROOT / 'web/lenses.js').read_text(encoding='utf-8') + '</script>\n'
    page = page.replace('</body>', extra + '</body>')
    path.write_text(page, encoding='utf-8')
    # GitHub Pages can serve the branch root or /docs. Neither may fall back to README.
    resources = {'notebook.html', 'titanic_jack_analysis.ipynb', 'titanic_jack_poster.pdf', 'poster-preview.png', 'feature-guide.json'}
    def root_url(match):
        attr, url = match.group(1), match.group(2)
        if url.split('#')[0] in resources or url.startswith('assets/'):
            url = 'docs/' + url
        return f'{attr}="{url}"'
    root_page = re.sub(r'(href|src)="([^"]+)"', root_url, page)
    (ROOT / 'index.html').write_text(root_page, encoding='utf-8')
    (ROOT / '.nojekyll').write_text('')
    (DOCS / '.nojekyll').write_text('')
    print('STORY RELEASE: story-first-v2; both root index.html and docs/index.html are complete exhibit pages.')
    print('FEATURE GUIDE: 12 columns; 714 known ages; 889 known ports; all summaries derived from unchanged CSV.')


if __name__ == '__main__':
    main()
