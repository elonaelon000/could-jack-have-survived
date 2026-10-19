"""Check documentation without changing research populations or executed code."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import sys
import threading
import nbformat
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))


def test_explanations_at_both_entry_points():
    for relative, prefix in [('docs/index.html', ''), ('index.html', 'docs/')]:
        page = (ROOT / relative).read_text(encoding='utf-8')
        assert page.count('id="age-methods"') == 1
        assert page.count('id="age-window-note"') == 1
        assert 'aria-describedby="age-window-note"' in page
        assert 'Overlapping age windows' in page
        for name in ('methods.html', 'notebook-guide-sq.html'):
            assert 'href="' + prefix + name + '"' in page
            assert (ROOT / relative).parent.joinpath(prefix + name).is_file()


def test_learning_pages_and_notebook_annotation():
    guide = (ROOT / 'docs/notebook-guide-sq.html').read_text(encoding='utf-8')
    assert '<html lang="sq">' in guide
    for phrase in ('RecordedRelatives', 'NOT SUPPORTED', '10/86', 'pd.cut'):
        assert phrase in guide
    methods = (ROOT / 'docs/methods.html').read_text(encoding='utf-8')
    for phrase in ('after analysis', 'not three age categories', 'statistically optimized thresholds'):
        assert phrase in methods
    nb = nbformat.read(ROOT / 'notebooks/titanic_jack_analysis.ipynb', as_version=4)
    assert len([c for c in nb.cells if c.cell_type == 'code']) == 13
    notes = [c for c in nb.cells if c.metadata.get('later_methods_clarification')]
    assert len(notes) == 2
    assert 'after analysis' in notes[0].source
    assert (ROOT / 'docs/titanic_jack_analysis.ipynb').read_bytes() == (ROOT / 'notebooks/titanic_jack_analysis.ipynb').read_bytes()


def test_annotation_preserves_executed_code_and_is_idempotent(tmp_path, monkeypatch):
    import document_methods as methods
    (tmp_path / 'notebooks').mkdir()
    (tmp_path / 'docs').mkdir()
    target = tmp_path / 'notebooks/titanic_jack_analysis.ipynb'
    shutil.copyfile(ROOT / 'notebooks/titanic_jack_analysis.ipynb', target)
    before = methods.code_snapshot(nbformat.read(target, as_version=4))
    monkeypatch.setattr(methods, 'ROOT', tmp_path)
    monkeypatch.setattr(methods, 'DOCS', tmp_path / 'docs')
    methods.annotate_notebook()
    methods.annotate_notebook()
    after = nbformat.read(target, as_version=4)
    assert methods.code_snapshot(after) == before
    assert sum(bool(c.metadata.get(methods.MARKER)) for c in after.cells) == 2


def test_age_window_endpoints_and_overlap():
    import pandas as pd
    values = pd.Series([17.5, 18, 22, 25, 25.5, 28, 30, 42, 50, 50.5, None])
    assert values[values.between(18, 25)].tolist() == [18, 22, 25]
    assert values[values.between(18, 30)].tolist() == [18, 22, 25, 25.5, 28, 30]
    assert 42 in values[values.between(18, 50)].tolist()
    assert all(values[values.between(18, high)].notna().all() for high in (25, 30, 50))


def test_methods_browser_when_available():
    pw = pytest.importorskip('playwright.sync_api')
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/'
    try:
        with pw.sync_playwright() as p:
            try:
                browser = p.chromium.launch()
            except pw.Error as error:
                if "Executable doesn't exist" in str(error):
                    pytest.skip('Install Playwright Chromium for this optional local test.')
                raise
            page = browser.new_page(reduced_motion='reduce')
            for width in (320, 390, 1440):
                page.set_viewport_size({'width': width, 'height': 960})
                for route in ('docs/methods.html', 'docs/notebook-guide-sq.html'):
                    response = page.goto(base + route)
                    assert response.status == 200
                    assert page.locator('h1').count() == 1
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
                page.goto(base)
                page.locator('#age-methods summary').click()
                assert page.locator('#age-methods details').get_attribute('open') is not None
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
                link = page.locator('#age-methods a').first.evaluate('(a) => a.href')
                assert page.request.get(link).status == 200
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
