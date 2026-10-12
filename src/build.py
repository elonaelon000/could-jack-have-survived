"""Rebuild the project notebook (with fresh outputs) and the one-page poster."""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
for path in (ROOT/'src'/'build_notebook.py', ROOT/'src'/'make_poster.py'):
    subprocess.run([sys.executable,str(path)],cwd=ROOT,check=True)

from nbclient import NotebookClient
import nbformat
path=ROOT/'notebooks'/'titanic_jack_analysis.ipynb'
nb=nbformat.read(path,as_version=4)
NotebookClient(nb,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
nbformat.write(nb,path)
print('Executed notebook successfully:',path)
