"""Reproducibility, rubric and measurement integrity checks."""
from pathlib import Path
import sys

import pandas as pd
import nbformat

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from analysis import load_data, observed, jack_like, young_men, family_group, wilson


def test_source_and_jack_profile():
    d=load_data()
    assert d.shape==(891,12) and d.PassengerId.is_unique
    assert d.Age.isna().sum()==177
    assert d.Cabin.isna().sum()==687
    assert d.Embarked.isna().sum()==2
    j=jack_like(d)
    assert (len(j),int(j.Survived.sum()))==(86,10)
    assert all((d.Survived>=0)&(d.Survived<=1))


def test_original_hypotheses_and_denominators():
    d=load_data()
    h2=observed(young_men(d),'Pclass')
    assert [(int(h2.loc[c,'survived']),int(h2.loc[c,'passengers'])) for c in [1,2,3]]==[(9,22),(1,41),(19,130)]
    assert h2.loc[1,'rate']>h2.loc[3,'rate']>h2.loc[2,'rate']
    h3=observed(family_group(d),'RecordedRelatives')
    assert [(int(h3.loc[c,'survived']),int(h3.loc[c,'passengers'])) for c in (False,True)]==[(25,168),(3,33)]
    assert h3.loc[True,'rate']<h3.loc[False,'rate']
    assert sum(int(h2.loc[c,'passengers']) for c in (1,2,3))==len(young_men(d))
    assert wilson(1,41)[0]<=1/41<=wilson(1,41)[1]


def test_rubric_and_original_hypotheses_preserved():
    nb=nbformat.read(ROOT/'notebooks/titanic_jack_analysis.ipynb',as_version=4)
    md='\n'.join(c.source for c in nb.cells if c.cell_type=='markdown')
    headings=['## 1. Load and profile','## 2. Three hypotheses','## 3. Cleaning','## 4. Explore',
              '## 5. Test','## 6. Three','## 7. Conclusion']
    positions=[md.index(x) for x in headings]
    assert positions==sorted(positions)
    for s in ('18–50 inclusive','18–30 inclusive','SibSp + Parch > 0','before outcome exploration'):
        assert s in md
    assert all(not any(output.output_type=='error' for output in c.get('outputs',[]))
               for c in nb.cells if c.cell_type=='code')
    assert any(c.get('outputs') for c in nb.cells if c.cell_type=='code')


def test_poster_one_landscape_page():
    from pypdf import PdfReader
    pages=PdfReader(str(ROOT/'poster'/'titanic_jack_poster.pdf')).pages
    assert len(pages)==1
    assert float(pages[0].mediabox.width)>float(pages[0].mediabox.height)
    txt=pages[0].extract_text()
    for phrase in ('COULD JACK HAVE BEEN SAVED?', '01', '02', '03', '10 of 86', 'WHAT DATA CANNOT TELL US'):
        assert phrase in txt
