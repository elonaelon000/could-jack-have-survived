"""Build a self-contained research notebook and a no-dependency static exhibit.

The original hypothesis generator is retained. This build changes delivery,
not the registered analysis populations or the unmodified source data.
"""
from __future__ import annotations
import ast
import base64
import gzip
import hashlib
import html
import json
from pathlib import Path
import shutil
import subprocess
import sys
import textwrap
import nbformat
from nbclient import NotebookClient
import mistune
from analysis import load_data, summaries, observed, wilson

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
TEAM='Kleant Laboti | Elona Tarja | Sarita Koci'
EXPECTED_SHA='7d118fef8b6ccf7f81111877bc388536f7b1e498a655e3d649d19aaa010e9f6f'


def make_portable_notebook():
    path=ROOT/'notebooks/titanic_jack_analysis.ipynb'
    nb=nbformat.read(path,as_version=4)
    raw=(ROOT/'data/train.csv').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_SHA:
        raise ValueError('Raw CSV checksum differs from the original uploaded data.')
    payload=base64.b64encode(gzip.compress(raw,mtime=0)).decode()
    payload_lines='\n'.join('    '+repr(payload[i:i+100]) for i in range(0,len(payload),100))
    src=(ROOT/'src/analysis.py').read_text()
    tree=ast.parse(src)
    names={'observed','jack_like','young_men','adults','family_group','wilson'}
    helpers='\n\n'.join(ast.get_source_segment(src,node) for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in names)
    bootstrap='''# Self-contained bootstrap: exact original CSV + transparent helper functions.
# No network, repository checkout, external src imports, or data upload required.
from pathlib import Path
from math import sqrt
import base64, gzip, hashlib, io, math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
from matplotlib.ticker import PercentFormatter

CSV_GZIP_BASE64 = (
'''+payload_lines+'''
)
raw_csv = gzip.decompress(base64.b64decode(CSV_GZIP_BASE64))
assert hashlib.sha256(raw_csv).hexdigest() == '''+repr(EXPECTED_SHA)+'''

def load_data(path=None):
    """Use original embedded bytes by default; do not mutate source values."""
    data = pd.read_csv(io.BytesIO(raw_csv) if path is None else path)
    assert data.shape == (891, 12)
    assert data.PassengerId.is_unique
    assert data.Survived.isin([0, 1]).all()
    assert data.Pclass.isin([1, 2, 3]).all()
    return data

'''+helpers+'''

df = load_data()
print('Dataset shape:', df.shape)
print('Verified SHA-256:', hashlib.sha256(raw_csv).hexdigest())
df.info()
print('Missing values per column:')
display(df.isna().sum().rename('missing').to_frame())
display(df.head())
'''
    initial=next(c for c in nb.cells if c.cell_type=='code')
    initial.source=bootstrap
    initial.metadata['jupyter']={'source_hidden':True}
    nb.cells[0].source+='\n\n**Group members:** '+TEAM+'\n\n**Portable edition:** the first code cell embeds the exact original CSV (gzip/base64) and validates its SHA-256. The encoding is a delivery convenience, not generated or simulated data. Expand it to inspect every helper. Run all cells in a clean Python kernel or Google Colab.'
    # Add qualifications outside the registered hypothesis section.
    idx=next(i for i,c in enumerate(nb.cells) if c.cell_type=='markdown' and c.source.startswith('## 5.'))
    nb.cells.insert(idx+1,nbformat.v4.new_markdown_cell('''**How to read the decisions.** These are registered descriptive directional comparisons, not null-hypothesis significance tests. *SURVIVED* means the observed direction agrees; *NOT SUPPORTED* means it does not. Approximate 95% Wilson intervals illustrate uncertainty under a binomial model. They do not account for this training sample's selection, missingness, confounding, or dependence between relatives. Overlap between separate intervals is not itself a valid test of a difference. No interval estimates the effect of changing Jack's ticket.'''))
    for c in nb.cells:
        if c.cell_type=='code':
            c.outputs=[];c.execution_count=None
        elif c.cell_type=='markdown':
            c.source=c.source.replace('These hypotheses are preserved exactly from the earlier preregistered GitHub version.','The original operational definitions and directional claims are preserved; consult the first commit for the original wording.')
    # Deterministic cell IDs avoid unrelated churn on a rebuild.
    for i,c in enumerate(nb.cells):c.id=hashlib.sha256((str(i)+c.source).encode()).hexdigest()[:12]
    nbformat.write(nb,path)
    NotebookClient(nb,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
    nbformat.write(nb,path)
    return nb


def record(sub):
    n=len(sub);k=int(sub.Survived.sum())
    lo,hi=wilson(k,n)
    return {'k':k,'n':n,'lo':lo if n else None,'hi':hi if n else None}


def evidence():
    d=load_data();s=summaries(d)
    out={'source':'Kaggle Titanic train.csv','sha256':EXPECTED_SHA,'rows':len(d),'jack':record(d[(d.Sex=='male')&(d.Pclass==3)&d.Age.between(18,25)]),'profiles':{},'h1':[]}
    for sex in ('male','female'):
        for cl in (1,2,3):
            for high in (25,30,50):
                sub=d[(d.Sex==sex)&(d.Pclass==cl)&d.Age.between(18,high)]
                for family in ('all','yes','no'):
                    group=sub if family=='all' else sub[((sub.SibSp+sub.Parch)>0)==(family=='yes')]
                    out['profiles'][f'{sex}:{cl}:{high}:{family}']=record(group)
    for cl in (1,2,3):
        f=s['h1'].loc[(cl,'female')];m=s['h1'].loc[(cl,'male')]
        out['h1'].append({'class':cl,'fk':int(f.survived),'fn':int(f.passengers),'mk':int(m.survived),'mn':int(m.passengers)})
    def row(label,sex,cl,age,family='all',style=''):
        return dict(label=label,style=style,**out['profiles'][f'{sex}:{cl}:{age}:{family}'])
    out['charts']=[
        {'topic':'SEX','title':'Young women fared better.','cohort':'Third class / known ages 18-25','rows':[row('Men','male',3,25,style='coral'),row('Women','female',3,25)],'caption':'Same class and age range; women had higher observed survival.'},
        {'topic':'CLASS','title':'Class was not a ladder.','cohort':'Men / known ages 18-30','rows':[row('First class','male',1,30),row('Second class','male',2,30,style='coral'),row('Third class','male',3,30,style='slate')],'caption':'First class was higher than third, but second was lower. Small groups limit interpretation.'},
        {'topic':'RELATIVES','title':'No clear family advantage.','cohort':'Third-class men / known ages 18-50','rows':[row('None recorded','male',3,50,'no','slate'),row('Relatives recorded','male',3,50,'yes','coral')],'caption':'Recorded close relatives were not associated with higher survival in the registered H3 group.'}
    ]
    return out


def notebook_html(nb):
    md=mistune.create_markdown(plugins=['table'])
    blocks=[]
    for i,c in enumerate(nb.cells):
        if c.cell_type=='markdown':blocks.append('<section class="prose">'+md(c.source)+'</section>');continue
        source=html.escape(c.source)
        summary='Self-contained data bootstrap (exact original CSV and helpers)' if i==2 else f'Code cell {c.execution_count}'
        blocks.append('<details class="code"'+('' if i==2 else ' open')+'><summary>'+summary+'</summary><pre><code>'+source+'</code></pre></details>')
        for out in c.get('outputs',[]):
            if out.output_type=='error':raise RuntimeError('Notebook execution contains an error.')
            if out.output_type=='stream':blocks.append('<pre class="output">'+html.escape(out.text)+'</pre>')
            else:
                data=out.get('data',{})
                if 'image/png' in data:blocks.append('<img class="plot" alt="Code-generated analysis chart; surrounding text and tables provide context and values." src="data:image/png;base64,'+data['image/png']+'">')
                elif 'text/html' in data:blocks.append('<div class="table-wrap">'+data['text/html']+'</div>')
                elif 'text/plain' in data:blocks.append('<pre class="output">'+html.escape(data['text/plain'])+'</pre>')
    style='''body{margin:0;background:#f5f1e9;color:#152733;font:15px/1.7 Arial,sans-serif}main{max-width:1050px;margin:auto;padding:35px 24px 80px}nav{background:#0b1c29;color:#e8d6b5;padding:18px 24px}nav a{color:inherit;margin-right:25px}h1,h2,h3{font-family:Georgia,serif;line-height:1.25}h1{font-size:36px}h2{font-size:29px;margin-top:58px;border-top:1px solid #bac3bb;padding-top:23px}h3{font-size:23px}table{border-collapse:collapse;width:100%;font-size:12px;margin:18px 0}th,td{border-bottom:1px solid #c6cec7;padding:9px;text-align:left}th{background:#e4e7df}pre{font-size:12px;line-height:1.6;overflow:auto;background:#e9ebe4;padding:18px;max-height:650px}summary{cursor:pointer;padding:14px 0;color:#795932}img.plot{max-width:100%;height:auto;display:block;margin:22px auto}.table-wrap{overflow:auto}a{color:#675332}code{font-size:.9em}strong{font-weight:600}.prose{margin:18px 0}.note{padding:17px;background:#e4e7df;font-size:13px}'''
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Jack File | Executed notebook</title><style>'+style+'</style><body><nav><a href="index.html">Back to the exhibit</a><a href="titanic_jack_analysis.ipynb" download>Download notebook</a></nav><main><p class="note">Executed research notebook. Every result below comes from running the original dataset through the shown code. The compressed data cell can be expanded. Original registered groups are unchanged.</p>'+''.join(blocks)+'</main></body></html>'


def main():
    DOCS.mkdir(exist_ok=True)
    subprocess.run([sys.executable,str(ROOT/'src/build_notebook.py')],check=True,cwd=ROOT)
    nb=make_portable_notebook()
    subprocess.run([sys.executable,str(ROOT/'src/make_poster.py')],check=True,cwd=ROOT)
    info=evidence()
    template=(ROOT/'web/index.html').read_text()
    page=template.replace('/*__CSS__*/',(ROOT/'web/style.css').read_text()).replace('/*__DATA__*/','window.JACK_DATA='+json.dumps(info,separators=(',',':'),allow_nan=False)+';').replace('/*__JS__*/',(ROOT/'web/app.js').read_text())
    (DOCS/'index.html').write_text(page)
    (DOCS/'evidence.json').write_text(json.dumps(info,indent=2,allow_nan=False)+'\n')
    (DOCS/'notebook.html').write_text(notebook_html(nb))
    (DOCS/'.nojekyll').write_text('')
    for source,target in [('poster/titanic_jack_poster.pdf','titanic_jack_poster.pdf'),('poster/preview.png','poster-preview.png'),('notebooks/titanic_jack_analysis.ipynb','titanic_jack_analysis.ipynb')]:shutil.copyfile(ROOT/source,DOCS/target)
    print('Built portable executed notebook, PDF, poster preview and complete static exhibit.')

if __name__=='__main__':main()
