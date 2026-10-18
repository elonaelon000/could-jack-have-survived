"""Checks linking the website, source data, portable notebook and poster."""
import hashlib
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
import nbformat
from nbclient import NotebookClient

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from analysis import load_data


def test_original_csv_checksum():
    assert hashlib.sha256((ROOT/'data/train.csv').read_bytes()).hexdigest()=='7d118fef8b6ccf7f81111877bc388536f7b1e498a655e3d649d19aaa010e9f6f'


def test_every_explorer_profile_matches_raw_data():
    d=load_data();info=json.loads((ROOT/'docs/evidence.json').read_text())
    assert len(info['profiles'])==54
    for key,r in info['profiles'].items():
        sex,cl,high,family=key.split(':')
        sub=d[(d.Sex==sex)&(d.Pclass==int(cl))&d.Age.between(18,int(high))]
        if family!='all':sub=sub[((sub.SibSp+sub.Parch)>0)==(family=='yes')]
        assert r['n']==len(sub) and r['k']==int(sub.Survived.sum()),key
        if r['n']:assert 0<=r['lo']<=r['k']/r['n']<=r['hi']<=1
        else:assert r['lo'] is None and r['hi'] is None


def test_family_profiles_partition_each_group():
    p=json.loads((ROOT/'docs/evidence.json').read_text())['profiles']
    for key,r in p.items():
        if key.endswith(':all'):
            base=key[:-3]
            for field in ('k','n'):assert r[field]==p[base+'yes'][field]+p[base+'no'][field]


def test_poster_charts_and_fixed_cohorts():
    e=json.loads((ROOT/'docs/evidence.json').read_text())
    assert len(e['charts'])==3
    assert [(r['k'],r['n']) for r in e['charts'][0]['rows']]==[(10,86),(14,30)]
    assert [(r['k'],r['n']) for r in e['charts'][1]['rows']]==[(9,22),(1,41),(19,130)]
    assert [(r['k'],r['n']) for r in e['charts'][2]['rows']]==[(25,168),(3,33)]


def test_site_resources_are_identical_to_canonical_files():
    for src,dest in [('poster/titanic_jack_poster.pdf','docs/titanic_jack_poster.pdf'),('poster/preview.png','docs/poster-preview.png'),('notebooks/titanic_jack_analysis.ipynb','docs/titanic_jack_analysis.ipynb')]:
        assert (ROOT/src).read_bytes()==(ROOT/dest).read_bytes()


class References(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids,'Duplicate HTML id';self.ids.add(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag in ('img','script','link') and ('src' in a or 'href' in a):self.links.append(a.get('src',a.get('href')))


def test_all_local_site_resources_and_anchors_resolve():
    doc=(ROOT/'docs/index.html').read_text();p=References();p.feed(doc)
    assert '/*__' not in doc
    for link in p.links:
        if link.startswith('#'):assert link[1:] in p.ids,link
        elif not link.startswith(('http:','https:','data:','mailto:')):assert (ROOT/'docs'/link.split('#')[0]).is_file(),link
    assert 'FICTIONAL ALTERNATE ENDING' in doc
    assert 'not movie footage or an AI-generated film' in doc


def test_one_canonical_notebook_and_team_identity():
    assert len(list((ROOT/'notebooks').glob('*.ipynb')))==1
    nb=nbformat.read(ROOT/'notebooks/titanic_jack_analysis.ipynb',as_version=4)
    md='\n'.join(c.source for c in nb.cells if c.cell_type=='markdown')
    for name in ('Kleant Laboti','Elona Tarja','Sarita Koci'):assert name in md
    for c in nb.cells:
        if c.cell_type=='code':assert 'from analysis import' not in c.source


def test_notebook_runs_outside_repository(tmp_path):
    nb=nbformat.read(ROOT/'notebooks/titanic_jack_analysis.ipynb',as_version=4)
    NotebookClient(nb,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(tmp_path)}}).execute()
    assert all(c.execution_count is not None for c in nb.cells if c.cell_type=='code')
    assert not any(o.output_type=='error' for c in nb.cells for o in c.get('outputs',[]))


def test_wilson_endpoints_do_not_show_negative_zero():
    from analysis import wilson
    for n in (1,10,11,30,86):
        assert wilson(0,n)[0]==0.0
        assert wilson(n,n)[1]==1.0
