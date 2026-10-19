"""Browser checks for the actual generated or deployed story, not the README."""
from __future__ import annotations
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import itertools
import json
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url')
    args = parser.parse_args()
    server = None
    if args.url:
        url = args.url
    else:
        server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        url = f'http://127.0.0.1:{server.server_port}/'
    out = ROOT / 'qa'
    out.mkdir(exist_ok=True)
    errors = []
    report = {'url': url, 'widths': [], 'profiles': 0, 'feature_tabs': 0}
    evidence = json.loads((ROOT / 'docs/evidence.json').read_text())
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 960})
        page.on('pageerror', lambda e: errors.append(str(e)))
        response = page.goto(url, wait_until='networkidle', timeout=60000)
        assert response and response.status == 200
        assert page.locator('meta[name="jack-release"]').get_attribute('content') == 'story-first-v2'
        assert page.locator('h1').inner_text().replace('\n', ' ') == 'His name was Jack Dawson.'
        assert page.locator('.hero-visual img').evaluate('(i)=>i.complete && i.naturalWidth>=900')
        for width in (320, 390, 768, 1024, 1440, 1920):
            page.set_viewport_size({'width': width, 'height': 960})
            page.evaluate('window.scrollTo(0,0)')
            page.wait_for_timeout(100)
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), f'Overflow at {width}'
            h = page.locator('h1').bounding_box()
            assert h and h['x'] >= 0 and h['x'] + h['width'] <= width + 1
            report['widths'].append(width)
            if width in (390, 1440):
                page.screenshot(path=str(out / f'hero-{width}.jpg'), type='jpeg', quality=78)
            for name in ('class', 'sex', 'age', 'family', 'geography', 'columns'):
                page.locator(f'[data-lens="{name}"]').click()
                assert len(page.locator('#lens-content').inner_text()) > 100
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), f'Feature overflow {name} at {width}'
                report['feature_tabs'] += 1
        page.set_viewport_size({'width': 1440, 'height': 960})
        page.locator('[data-lens="class"]').click()
        page.locator('[data-class-view="young"]').click()
        assert '40.9%' in page.locator('#lens-content').inner_text()
        page.locator('[data-class-view="all"]').click()
        assert '63.0%' in page.locator('#lens-content').inner_text()
        page.locator('#understand').screenshot(path=str(out / 'feature-guide.jpg'), type='jpeg', quality=75)
        for sex, cl, age, family in itertools.product(('male','female'), ('1','2','3'), ('25','30','50'), ('all','yes','no')):
            for selector, value in zip(('sex','class','age','family'), (sex,cl,age,family)):
                page.locator('#'+selector).select_option(value)
            row = evidence['profiles'][':'.join((sex,cl,age,family))]
            text = page.locator('#result-count').inner_text()
            assert text == f"{row['k']} survivor{'s' if row['k'] != 1 else ''} out of {row['n']} passenger{'s' if row['n'] != 1 else ''}"
            report['profiles'] += 1
        page.locator('#reset').click()
        assert page.locator('#result-count').inner_text() == '10 survivors out of 86 passengers'
        page.locator('[data-open-story]').click()
        assert page.locator('#story-dialog').is_visible()
        page.keyboard.press('Escape')
        assert not page.locator('#story-dialog').is_visible()
        assert page.locator('[data-open-story]').evaluate('(e)=>e===document.activeElement')
        # Resource URLs must be actual files on the requested site, not GitHub source views.
        for selector in ('.resource[href$="notebook.html"]', '.resource[href$="titanic_jack_poster.pdf"]', '.resource[download]'):
            resource = page.locator(selector).evaluate('(a)=>a.href')
            r = page.request.get(resource)
            assert r.status == 200, resource
            if resource.endswith('.pdf'): assert r.body().startswith(b'%PDF')
        page.emulate_media(reduced_motion='reduce')
        assert page.evaluate('getComputedStyle(document.documentElement).scrollBehavior') == 'auto'
        report['errors'] = errors
        assert not errors, errors
        report['heading'] = page.locator('h1').inner_text().replace('\n', ' ')
        report['title'] = page.title()
        browser.close()
    (out / ('live-report.json' if args.url else 'browser-report.json')).write_text(json.dumps(report, indent=2)+'\n')
    print('STORY_BROWSER_VERIFIED '+json.dumps(report))
    if server: server.shutdown()


if __name__ == '__main__':
    main()
