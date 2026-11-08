from __future__ import annotations

import hashlib
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://apps.yokoichi.jp'
DETAILS = ['yorishiro/index.html', 'yorishiro/en/index.html',
         'tozankinen/index.html', 'ichikeshi/index.html', 'ichikeshi/en/index.html',
         'realtime-search-shortcut/index.html', 'x-bookmark-exporter/index.html']
PAGES = ['index.html', 'en/index.html'] + DETAILS


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.elements = []
        self.anchor_depth = 0
        self.nested_controls = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.elements.append((tag, a))
        if tag in ('a', 'button') and self.anchor_depth:
            self.nested_controls.append((tag, a))
        if tag == 'a':
            self.anchor_depth += 1

    def handle_endtag(self, tag):
        if tag == 'a':
            self.anchor_depth -= 1

    def by_tag(self, tag):
        return [a for t, a in self.elements if t == tag]


class PortalJourneyTests(unittest.TestCase):
    def test_root_offers_five_named_single_detail_links(self):
        d = Document(ROOT / 'index.html')
        rows = [a for a in d.by_tag('a') if 'portal-row' in a.get('class', '').split()]
        self.assertEqual([urlsplit(urljoin(ORIGIN + '/', a['href'])).path for a in rows],
                         ['/yorishiro/', '/tozankinen/', '/ichikeshi/', '/realtime-search-shortcut/', '/x-bookmark-exporter/'])
        for a, name in zip(rows, ['Yorishiro', '登山記念', '位置消し', 'リアルタイム検索', 'Xブックマークエクスポーター']):
            self.assertIn(name, a.get('aria-label', ''))
        self.assertEqual(d.nested_controls, [])

    def test_shared_support_is_a_product_specific_directory(self):
        d = Document(ROOT / 'index.html')
        self.assertTrue(any(a.get('id') == 'support' for _, a in d.elements))
        hrefs = [urlsplit(urljoin(ORIGIN + '/', a.get('href', ''))).path for a in d.by_tag('a')]
        for p in ['/yorishiro/support/', '/yorishiro/privacy/', '/yorishiro/terms/',
                  '/yorishiro/legal-notice/', '/tozankinen/support/', '/tozankinen/privacy/',
                  '/tozankinen/terms/', '/ichikeshi/support/', '/ichikeshi/privacy/',
                  '/realtime-search-shortcut/privacy/', '/x-bookmark-exporter/privacy/']:
            self.assertIn(p, hrefs)
        self.assertGreaterEqual(sum(a.get('href') == '#support' for a in d.by_tag('a')), 1)
        self.assertNotIn('/ichikeshi/terms/', hrefs)

    def test_existing_extension_fragment_still_identifies_its_product(self):
        d = Document(ROOT / 'index.html')
        self.assertTrue(any(a.get('id') == 'extensions' for _, a in d.elements))

    def test_ichikeshi_switches_language_at_the_same_page_depth(self):
        for page, target in [('ichikeshi/index.html', '/ichikeshi/en/'),
                             ('ichikeshi/en/index.html', '/ichikeshi/')]:
            d = Document(ROOT / page)
            switches = [a for a in d.by_tag('a') if 'locale-switch' in a.get('class', '').split()]
            self.assertEqual(len(switches), 1)
            self.assertEqual(urlsplit(urljoin(ORIGIN + '/' + page, switches[0]['href'])).path, target)
            self.assertTrue(switches[0].get('aria-label'))
            if '/en/' in page:
                back = [a for a in d.by_tag('a') if a.get('href') == '../../en/']
                self.assertEqual(len(back), 1)
                self.assertIn('All apps', (ROOT / page).read_text())

    def test_each_product_has_a_text_store_link(self):
        ids = {'yorishiro': '6764608171', 'tozankinen': '6797188526',
               'ichikeshi': '6816470389', 'realtime-search-shortcut': 'cbaakfanbmegjclflbbdgiegibfaoflo'}
        for page in [page for page in DETAILS if not page.startswith('x-bookmark-exporter/')]:
            with self.subTest(page=page):
                d = Document(ROOT / page)
                links = [a for a in d.by_tag('a') if 'portal-store' in a.get('class', '').split()]
                self.assertEqual(len(links), 1)
                self.assertIn(ids[page.split('/')[0]], links[0]['href'])
                self.assertIn('App Store' if 'realtime' not in page else 'Chrome Web Store', (ROOT / page).read_text())
                self.assertNotIn('近日公開', (ROOT / page).read_text())

    def test_every_local_navigation_media_and_fragment_resolves(self):
        for page in PAGES + ['x-bookmark-exporter/privacy/index.html']:
            d = Document(ROOT / page)
            base = ORIGIN + '/' + page.removesuffix('index.html')
            for tag, a in d.elements:
                attr = 'src' if tag in ('img', 'script') else 'href' if tag in ('a', 'link') else None
                if not attr or attr not in a:
                    continue
                u = urlsplit(urljoin(base, a[attr]))
                if u.netloc != 'apps.yokoichi.jp':
                    continue
                target = ROOT / unquote(u.path).lstrip('/')
                if target.is_dir():
                    target /= 'index.html'
                with self.subTest(page=page, url=a[attr]):
                    self.assertTrue(target.is_file(), str(target))
                    if u.fragment:
                        ids = [x.get('id') for _, x in Document(target).elements]
                        self.assertIn(u.fragment, ids)

    def test_product_screens_have_verified_sources_and_dimensions(self):
        ledger = json.loads((ROOT / 'assets/portal-media.json').read_text())
        screens = {a['path']: a for a in ledger if a.get('kind') == 'screenshot'}
        for page in DETAILS:
            images = [a for a in Document(ROOT / page).by_tag('img') if 'portal-screen' in a.get('class', '').split()]
            self.assertGreaterEqual(len(images), 1, page)
            self.assertLessEqual(len(images), 2 if 'realtime' in page else 3)
            for i, a in enumerate(images):
                path = urlsplit(urljoin(ORIGIN + '/' + page, a['src'])).path.lstrip('/')
                source = screens[path]
                self.assertTrue(source['owner_verified'])
                self.assertEqual(int(a['width']), source['width'])
                self.assertEqual(int(a['height']), source['height'])
                self.assertTrue(a.get('alt'))
                self.assertNotIn('generated', source['source'])
                if i == 0:
                    self.assertNotEqual(a.get('loading'), 'lazy')

    def test_marketing_styles_are_isolated_and_no_new_executable_dependencies(self):
        for page in PAGES:
            d = Document(ROOT / page)
            self.assertIn('portal-marketing', d.by_tag('body')[0].get('class', '').split())
            scripts = d.by_tag('script')
            if page in ('index.html', 'en/index.html'):
                self.assertEqual(len(scripts), 1)
                self.assertTrue(scripts[0].get('src', '').endswith('assets/portal-locale.js'))
            else:
                self.assertEqual(scripts, [])
            sheets = [a['href'] for a in d.by_tag('link') if a.get('rel') == 'stylesheet']
            self.assertEqual(len(sheets), 1)
            self.assertTrue(sheets[0].endswith('/assets/portal.css') or sheets[0] == 'assets/portal.css')
            self.assertFalse(any('fonts.googleapis' in str(a) for _, a in d.elements))

    def test_exporter_unpublished_store_status_price_and_local_archive_features(self):
        page = ROOT / 'x-bookmark-exporter/index.html'
        text, document = page.read_text(), Document(page)
        self.assertFalse(any('chromewebstore.google.com' in a.get('href', '') for a in document.by_tag('a')))
        for phrase in ['Chromeウェブストアでの公開準備中', 'USD3.99', '1,000', '1〜50GB', '5GB',
                       'CSV', 'JSON', 'Excel', 'GIF', 'MP4', 'index.html', '全件', '差分',
                       'データ同期', '非公式', '保存画面の例（サンプルデータ）']:
            self.assertIn(phrase, text)
        for filename in ['index.html', 'en/index.html']:
            d = Document(ROOT / filename)
            rows = [a for a in d.by_tag('a') if 'portal-row' in a.get('class', '').split()]
            self.assertEqual(len(rows), 5)
            self.assertTrue(rows[-1]['href'].endswith('x-bookmark-exporter/'))
            if filename.startswith('en/'):
                self.assertEqual(rows[-1]['hreflang'], 'ja')
            self.assertIn('mailto:main@yokoichi.jp', [a.get('href') for a in d.by_tag('a')])

    def test_exporter_privacy_discloses_local_and_billing_data_separately(self):
        path = ROOT / 'x-bookmark-exporter/privacy/index.html'
        text, document = path.read_text(), Document(path)
        for phrase in ['2026年11月8日', '横田裕市', '数値アカウントID', '診断', '一時メモリ',
                       'pbs.twimg.com', 'video.twimg.com', 'HEAD', 'Range', 'Cookie', 'オフライン',
                       'Cloudflare', 'D1', 'HMAC', 'SHA-256', '30日', '20分', '5回', 'Resend',
                       'Stripe', 'CVC', '権利確認', '物理削除', 'アンインストール', 'GitHub Pages']:
            self.assertIn(phrase, text)
        self.assertIn('mailto:main@yokoichi.jp', [a.get('href') for a in document.by_tag('a')])
        self.assertEqual(document.by_tag('script'), [])
        self.assertIn('../../assets/styles.css', [a.get('href') for a in document.by_tag('link')])
        self.assertNotIn('workers.dev', text)
        self.assertNotIn('情報を一切収集しません', text)

    def test_exporter_screenshot_bytes_and_ledger_match_actual_jpeg_dimensions(self):
        import struct
        ledger = json.loads((ROOT / 'assets/portal-media.json').read_text())
        entry = next(item for item in ledger if item['path'] == 'assets/portal-screens/x-bookmark-exporter.jpg')
        data = (ROOT / entry['path']).read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), entry['sha256'])
        self.assertEqual(data[:2], b'\xff\xd8')
        offset = 2
        while offset < len(data):
            self.assertEqual(data[offset], 255)
            marker = data[offset + 1]
            length = struct.unpack('>H', data[offset + 2:offset + 4])[0]
            if marker in (0xc0, 0xc1, 0xc2):
                height, width = struct.unpack('>HH', data[offset + 5:offset + 9])
                break
            offset += 2 + length
        else:
            self.fail('JPEG dimensions not found')
        self.assertEqual((width, height), (1265, 889))
        self.assertEqual((entry['width'], entry['height']), (width, height))
        self.assertIn('synthetic data', entry['source'])
        self.assertIn('implemented extension UI', entry['source'])

    def test_protected_legal_support_original_assets_and_routing_bytes_unchanged(self):
        baseline = json.loads((ROOT / 'tests/protected-baseline.json').read_text())
        for path, sha in baseline['files'].items():
            with self.subTest(path=path):
                self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), sha)

    def test_ichikeshi_copy_explains_processing_and_advertising_separately(self):
        ja = (ROOT / 'ichikeshi/index.html').read_text()
        en = (ROOT / 'ichikeshi/en/index.html').read_text()
        for text, copy, ads in [(ja, 'コピー', 'AdMob'), (en, 'copy', 'AdMob')]:
            self.assertIn(copy, text)
            self.assertIn(ads, text)
        self.assertNotIn('通信しない', ja)


if __name__ == '__main__':
    unittest.main()
