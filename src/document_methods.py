"""Publish methodological explanations without changing research code or outcomes.

Run after the ordinary notebook/site build. All documentation is a later
clarification; the registered hypotheses and original data remain unchanged.
"""
from __future__ import annotations

import html
import json
from pathlib import Path
import re
import shutil

import mistune
import nbformat
from build_exhibit import notebook_html

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
SITE = 'https://elonaelon000.github.io/could-jack-have-survived/docs/'
MARKER = 'later_methods_clarification'

AGE_NOTE = '''### Why these age windows? A later methodological clarification

This explanation was added on 19 October 2026, after analysis. The cutoffs themselves are already present in the original hypothesis commit; this note is not new preregistration or a claim of statistically optimized cutoffs.

| Window | Purpose |
|---|---|
| 18-25 | Closest Jack-like baseline: male, third class, known age. |
| 18-30 | H2: compare first- and third-class young men; show second class too. |
| 18-50 | H1: compare women and men within each class. H3: compare recorded relatives among third-class men. |

These are overlapping analysis windows, not disjoint age categories. Endpoints are inclusive. Unknown ages are excluded only from age-dependent subsets, not deleted from the source dataset. The narrower window favors similarity to Jack; wider windows add passengers but are less specific to him. More observations do not automatically make a comparison better, and sharing an age window does not fully adjust for age.

The website selector changes only the age filter, not the entire hypothesis test. First-class men 18-25 number 10; at 18-30 they number 22. These observed counts illustrate the trade-off, not an outcome-based justification for the original choice.

[Full methodological explanation](https://elonaelon000.github.io/could-jack-have-survived/docs/methods.html) | [Notebook guide in Albanian](https://elonaelon000.github.io/could-jack-have-survived/docs/notebook-guide-sq.html)
'''

BIN_NOTE = '''**Reading the exploratory age-band plot accurately.** The existing `pd.cut` edges are `[-0.01, 12, 17, 25, 35, 50, 65, 110]`, with right-closed intervals. For example, the shortened label "18-25" represents `(17, 25]` in that plot and should not be treated as the exact Jack filter for fractional ages. A displayed `nan` group means age not recorded, not an age interval. Registered comparisons use `Age.between(18, ...)` directly; neither the plot labels nor this clarification change those populations. The original exploratory code is retained.
'''


def code_snapshot(nb):
    return json.dumps([
        {'source': c.source, 'outputs': c.get('outputs', []),
         'execution_count': c.get('execution_count')}
        for c in nb.cells if c.cell_type == 'code'
    ], sort_keys=True, ensure_ascii=False)


def annotate_notebook():
    path = ROOT / 'notebooks/titanic_jack_analysis.ipynb'
    nb = nbformat.read(path, as_version=4)
    before = code_snapshot(nb)
    nb.cells = [c for c in nb.cells if not c.metadata.get(MARKER)]
    position = next(i for i, c in enumerate(nb.cells)
                    if c.cell_type == 'markdown' and c.source.startswith('## 3.'))
    note = nbformat.v4.new_markdown_cell(AGE_NOTE)
    note.id = 'age-window-clarification'
    note.metadata[MARKER] = True
    nb.cells.insert(position, note)
    position = next(i for i, c in enumerate(nb.cells)
                    if c.cell_type == 'code' and "clean['AgeBand']=pd.cut" in c.source)
    note = nbformat.v4.new_markdown_cell(BIN_NOTE)
    note.id = 'age-bin-reading-note'
    note.metadata[MARKER] = True
    nb.cells.insert(position, note)
    if code_snapshot(nb) != before:
        raise RuntimeError('A documentation update changed research code or outputs.')
    nbformat.write(nb, path)
    shutil.copyfile(path, DOCS / 'titanic_jack_analysis.ipynb')
    page = notebook_html(nb)
    nav = '<a href="methods.html">Age windows</a><a href="notebook-guide-sq.html">Guide in Albanian</a>'
    page = page.replace('</nav>', nav + '</nav>', 1)
    (DOCS / 'notebook.html').write_text(page, encoding='utf-8')


def learning_page(markdown_text, title, language):
    body = mistune.create_markdown(plugins=['table'])(markdown_text)
    headings = []
    def heading(match):
        anchor = 'section-' + str(len(headings) + 1)
        label = re.sub('<[^>]+>', '', match.group(1))
        headings.append((anchor, label))
        return '<h2 id="' + anchor + '">' + match.group(1) + '</h2>'
    body = re.sub(r'<h2>(.*?)</h2>', heading, body, flags=re.S)
    body = body.replace('<table>', '<div class="table-scroll"><table>').replace('</table>', '</table></div>')
    toc = '<details class="contents"><summary>' + ('Permbajtja' if language == 'sq' else 'Contents') + '</summary>'
    toc += ''.join('<a href="#' + a + '">' + t + '</a>' for a, t in headings) + '</details>'
    css = '''*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:20px}body{margin:0;background:#f5f1e9;color:#172a35;font:17px/1.8 system-ui,sans-serif}nav{background:#071b28;color:#ecd7b6;padding:20px max(20px,calc((100vw - 1080px)/2));display:flex;flex-wrap:wrap;gap:14px 25px}nav a{color:inherit;font-size:14px}main{max-width:1080px;padding:44px 28px 90px;margin:auto}h1,h2,h3{font-family:Georgia,serif;line-height:1.25}h1{font-size:clamp(31px,5vw,52px)}h2{font-size:29px;margin-top:50px;padding-top:26px;border-top:1px solid #c6c8bd}h3{font-size:23px}p{max-width:82ch}a{color:#695024;text-underline-offset:3px}a:focus-visible,summary:focus-visible{outline:3px solid #a87438;outline-offset:4px}pre{overflow:auto;max-width:100%;padding:22px;background:#0b2330;color:#f4e7d1;font:14px/1.7 ui-monospace,monospace;border-radius:5px}code{font-family:ui-monospace,monospace;font-size:.88em;overflow-wrap:anywhere}pre code{font-size:inherit;overflow-wrap:normal}table{border-collapse:collapse;width:100%;min-width:480px;font-size:14px}th,td{padding:12px 14px;text-align:left;vertical-align:top;border-bottom:1px solid #c6c8bd}th{background:#e3e5db}.table-scroll{overflow-x:auto;margin:25px 0}.contents{border:1px solid #c6c8bd;padding:18px 22px;margin:28px 0}.contents a{display:block;font-size:15px;margin:6px 0}.contents summary{cursor:pointer;font-weight:650}.edition{font-size:13px;letter-spacing:.06em;color:#655942}blockquote{margin:24px 0;padding:2px 22px;border-left:3px solid #a98b5c;background:#e8e9df}@media(max-width:480px){body{font-size:16px}main{padding:28px 18px 60px}h2{font-size:25px}pre{padding:15px;font-size:12px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}'''
    return ('<!doctype html><html lang="' + language + '"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1"><title>'
            + html.escape(title) + '</title><style>' + css + '</style></head><body><nav>'
            '<a href="index.html">The Jack File</a><a href="notebook.html">Executed notebook</a>'
            '<a href="methods.html">Age windows</a><a href="notebook-guide-sq.html">Shpjegimi ne shqip</a>'
            '</nav><main><p class="edition">METHODS &amp; LEARNING / 19 OCTOBER 2026</p>'
            + toc + body + '</main></body></html>')


def inject_explanation(path, prefix):
    page = path.read_text(encoding='utf-8')
    # Idempotent for a standalone rerun; a normal build starts from the template.
    page = re.sub(r'<!-- AGE-METHODS START -->.*?<!-- AGE-METHODS END -->', '', page, flags=re.S)
    page = page.replace('<select id="age">', '<select id="age" aria-describedby="age-window-note">')
    content = '''<!-- AGE-METHODS START --><div id="age-methods" style="margin-top:20px;max-width:100%">
<p id="age-window-note" style="font-size:14px;line-height:1.6">Overlapping age windows, not separate categories. The selector changes only age; other filters still apply.</p>
<details class="dark-details"><summary>Why 18&#8211;25, 18&#8211;30 and 18&#8211;50?</summary>
<p><strong>18&#8211;25:</strong> the closest Jack-like baseline. <strong>18&#8211;30:</strong> H2, comparing first- and third-class young men. <strong>18&#8211;50:</strong> H1 compares women and men within each class; H3 compares recorded relatives among third-class men.</p>
<p>The narrower window prioritizes similarity to Jack. Wider windows include more passengers but are less specific. These are design choices, not statistically optimized boundaries. Endpoints are inclusive; unknown ages cannot establish membership. A 22-year-old belongs to all three windows.</p>
<p>The cutoffs were recorded before outcome analysis. This fuller explanation was added later; it is not new preregistration. A shared age window does not fully adjust for age.</p>
<p><a href="__PREFIX__methods.html">Read the full methodological explanation &#8599;</a><br><a href="__PREFIX__notebook-guide-sq.html">Notebook-u i shpjeguar ne shqip &#8599;</a></p>
</details></div><!-- AGE-METHODS END -->'''.replace('__PREFIX__', prefix)
    pattern = r'(<button\b[^>]*\bid="reset"[^>]*>.*?</button>)'
    page, count = re.subn(pattern, lambda m: m.group(1) + content, page, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError('Could not locate the explorer reset control in ' + str(path))
    path.write_text(page, encoding='utf-8')


def main():
    DOCS.mkdir(exist_ok=True)
    for source, target, title, language in [
        ('AGE_WINDOWS.md', 'methods.html', 'The Jack File | Why these age windows?', 'en'),
        ('NOTEBOOK_GUIDE_SQ.md', 'notebook-guide-sq.html', 'The Jack File | Notebook-u ne shqip', 'sq'),
    ]:
        text = (DOCS / source).read_text(encoding='utf-8')
        (DOCS / target).write_text(learning_page(text, title, language), encoding='utf-8')
    annotate_notebook()
    inject_explanation(DOCS / 'index.html', '')
    inject_explanation(ROOT / 'index.html', 'docs/')
    print('Published age-window explanations and Albanian notebook guide; research code and outputs unchanged.')


if __name__ == '__main__':
    main()
