"""Regression tests for the real homepage and the new feature explanations."""
import json
from pathlib import Path
from html.parser import HTMLParser
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids
            self.ids.add(a['id'])
        if tag in ('a','link') and 'href' in a: self.refs.append(a['href'])
        if tag in ('img','script') and 'src' in a: self.refs.append(a['src'])

def test_root_is_story_not_readme():
    for parent in (ROOT, ROOT/'docs'):
        page=(parent/'index.html').read_text()
        assert 'story-first-v2' in page
        assert 'His name was<br><em>Jack Dawson.</em>' in page
        assert page.index('id="story"') < page.index('id="dataset"') < page.index('id="understand"') < page.index('id="evidence"')
        assert 'window.JACK_GUIDE=' in page and 'window.JACK_DATA=' in page
        assert '/*__' not in page
        links=Links(); links.feed(page)
        for ref in links.refs:
            if ref.startswith('#'): assert ref[1:] in links.ids, ref
            elif not ref.startswith(('https:','http:','data:','mailto:')): assert (parent/ref.split('#')[0]).is_file(),ref
        assert (parent/'.nojekyll').is_file()

def test_guide_preserves_denominators():
    d=pd.read_csv(ROOT/'data/train.csv')
    g=json.loads((ROOT/'docs/feature-guide.json').read_text())
    assert g['columns']==list(d.columns)
    assert len(g['columns'])==12
    assert sum(r['n'] for r in g['age_bands'])==714
    assert sum(r['k'] for r in g['age_bands'])==int(d.loc[d.Age.notna(),'Survived'].sum())
    assert sum(r['n'] for r in g['ports'])+g['ports_missing']==891
    for r in g['ports']:
        sub=d[d.Embarked==r['code']]
        assert (r['n'],r['k'])==(len(sub),int(sub.Survived.sum()))
    assert [(r['k'],r['n']) for r in g['classes']]==[(136,216),(87,184),(119,491)]
    assert [(r['k'],r['n']) for r in g['young_men']]==[(9,22),(1,41),(19,130)]
    assert [(r['k'],r['n']) for r in g['family_h3']]==[(25,168),(3,33)]

def test_art_and_research_boundaries():
    from PIL import Image
    with Image.open(ROOT/'docs/assets/titanic-1912.jpg') as im: assert im.width>=900
    p=(ROOT/'docs/index.html').read_text()
    for phrase in ('not an authentic ticket','a nationality.','not movie footage or an AI-generated film','not an individual','not a controlled experiment'):
        assert phrase in p, phrase
