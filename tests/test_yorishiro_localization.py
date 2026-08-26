from __future__ import annotations

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
YORISHIRO_ROOT = REPOSITORY_ROOT / "yorishiro"
SITE_ORIGIN = "https://apps.yokoichi.jp"

PAGES = {
    "home": {
        "ja_file": YORISHIRO_ROOT / "index.html",
        "en_file": YORISHIRO_ROOT / "en" / "index.html",
        "ja_url": f"{SITE_ORIGIN}/yorishiro/",
        "en_url": f"{SITE_ORIGIN}/yorishiro/en/",
    },
    "privacy": {
        "ja_file": YORISHIRO_ROOT / "privacy" / "index.html",
        "en_file": YORISHIRO_ROOT / "en" / "privacy" / "index.html",
        "ja_url": f"{SITE_ORIGIN}/yorishiro/privacy/",
        "en_url": f"{SITE_ORIGIN}/yorishiro/en/privacy/",
    },
    "terms": {
        "ja_file": YORISHIRO_ROOT / "terms" / "index.html",
        "en_file": YORISHIRO_ROOT / "en" / "terms" / "index.html",
        "ja_url": f"{SITE_ORIGIN}/yorishiro/terms/",
        "en_url": f"{SITE_ORIGIN}/yorishiro/en/terms/",
    },
    "support": {
        "ja_file": YORISHIRO_ROOT / "support" / "index.html",
        "en_file": YORISHIRO_ROOT / "en" / "support" / "index.html",
        "ja_url": f"{SITE_ORIGIN}/yorishiro/support/",
        "en_url": f"{SITE_ORIGIN}/yorishiro/en/support/",
    },
    "legal-notice": {
        "ja_file": YORISHIRO_ROOT / "legal-notice" / "index.html",
        "en_file": YORISHIRO_ROOT / "en" / "legal-notice" / "index.html",
        "ja_url": f"{SITE_ORIGIN}/yorishiro/legal-notice/",
        "en_url": f"{SITE_ORIGIN}/yorishiro/en/legal-notice/",
    },
}


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_lang: str | None = None
        self.links: list[dict[str, str]] = []
        self.anchors: list[dict[str, str]] = []
        self.visible_text: list[str] = []
        self._hidden_depth = 0

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = {key: value or "" for key, value in attrs}
        if tag == "html":
            self.html_lang = attributes.get("lang")
        elif tag == "link":
            self.links.append(attributes)
        elif tag == "a":
            self.anchors.append(attributes)
        elif tag in {"script", "style"}:
            self._hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self._hidden_depth:
            self._hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._hidden_depth == 0 and data.strip():
            self.visible_text.append(data.strip())


def parse_document(path: Path) -> DocumentParser:
    if not path.is_file():
        raise AssertionError(f"Missing localized page: {path}")
    parser = DocumentParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def alternate_urls(parser: DocumentParser) -> dict[str, str]:
    return {
        link["hreflang"]: link["href"]
        for link in parser.links
        if link.get("rel") == "alternate" and "hreflang" in link
    }


def canonical_url(parser: DocumentParser) -> str | None:
    return next(
        (
            link.get("href")
            for link in parser.links
            if link.get("rel") == "canonical"
        ),
        None,
    )


class YorishiroLocalizationTests(unittest.TestCase):
    def test_every_japanese_page_has_an_english_counterpart(self) -> None:
        for page_name, page in PAGES.items():
            with self.subTest(page=page_name):
                self.assertTrue(page["en_file"].is_file())

    def test_each_locale_switch_opens_the_same_page_in_the_other_language(self) -> None:
        for page_name, page in PAGES.items():
            for locale in ("ja", "en"):
                with self.subTest(page=page_name, locale=locale):
                    parser = parse_document(page[f"{locale}_file"])
                    switches = [
                        anchor
                        for anchor in parser.anchors
                        if "locale-switch" in anchor.get("class", "").split()
                    ]
                    self.assertEqual(len(switches), 1)
                    target = urljoin(page[f"{locale}_url"], switches[0]["href"])
                    other_locale = "en" if locale == "ja" else "ja"
                    self.assertEqual(target, page[f"{other_locale}_url"])

    def test_each_locale_switch_has_an_accessible_english_label(self) -> None:
        expected_labels = {
            "ja": "View in English",
            "en": "View in Japanese",
        }
        for page_name, page in PAGES.items():
            for locale, expected_label in expected_labels.items():
                with self.subTest(page=page_name, locale=locale):
                    parser = parse_document(page[f"{locale}_file"])
                    switch = next(
                        anchor
                        for anchor in parser.anchors
                        if "locale-switch" in anchor.get("class", "").split()
                    )
                    self.assertEqual(switch.get("aria-label"), expected_label)

    def test_language_metadata_points_to_both_versions(self) -> None:
        for page_name, page in PAGES.items():
            for locale in ("ja", "en"):
                with self.subTest(page=page_name, locale=locale):
                    parser = parse_document(page[f"{locale}_file"])
                    self.assertEqual(parser.html_lang, locale)
                    self.assertEqual(canonical_url(parser), page[f"{locale}_url"])
                    alternates = alternate_urls(parser)
                    self.assertEqual(alternates.get("ja"), page["ja_url"])
                    self.assertEqual(alternates.get("en"), page["en_url"])
                    self.assertEqual(alternates.get("x-default"), page["ja_url"])

    def test_english_pages_keep_yorishiro_navigation_in_english(self) -> None:
        allowed_paths = {
            "/yorishiro/en/",
            "/yorishiro/en/privacy/",
            "/yorishiro/en/terms/",
            "/yorishiro/en/support/",
            "/yorishiro/en/legal-notice/",
        }
        for page_name, page in PAGES.items():
            with self.subTest(page=page_name):
                parser = parse_document(page["en_file"])
                for anchor in parser.anchors:
                    classes = anchor.get("class", "").split()
                    if "brand" in classes or "locale-switch" in classes:
                        continue
                    resolved = urljoin(page["en_url"], anchor.get("href", ""))
                    parsed = urlparse(resolved)
                    if parsed.netloc != "apps.yokoichi.jp":
                        continue
                    self.assertIn(parsed.path, allowed_paths)

    def test_english_pages_do_not_expose_untranslated_japanese_copy(self) -> None:
        japanese_characters = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
        for page_name, page in PAGES.items():
            with self.subTest(page=page_name):
                parser = parse_document(page["en_file"])
                visible_copy = " ".join(parser.visible_text)
                self.assertIsNone(japanese_characters.search(visible_copy))

    def test_support_pages_use_locale_specific_contact_forms(self) -> None:
        expected_urls = {
            "ja": "https://forms.gle/pXicWf8RznUk7daB9",
            "en": "https://forms.gle/gMsU8oPncFH6pjGZ6",
        }
        support_page = PAGES["support"]

        for locale, expected_url in expected_urls.items():
            with self.subTest(locale=locale):
                parser = parse_document(support_page[f"{locale}_file"])
                form_urls = [
                    anchor.get("href")
                    for anchor in parser.anchors
                    if urlparse(anchor.get("href", "")).netloc == "forms.gle"
                ]
                self.assertEqual(form_urls, [expected_url])


if __name__ == "__main__":
    unittest.main()
