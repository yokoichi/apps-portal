# apps-portal

GitHub Pages で公開するアプリポータル用の静的サイトです。

- Portal URL: https://apps.yokoichi.jp/
- Yorishiro URL: https://apps.yokoichi.jp/yorishiro/
- Realtime Search Shortcut URL: https://apps.yokoichi.jp/realtime-search-shortcut/
- Ichikeshi URL: https://apps.yokoichi.jp/ichikeshi/ (en: https://apps.yokoichi.jp/ichikeshi/en/)
- Xブックマークエクスポーター URL: https://apps.yokoichi.jp/x-bookmark-exporter/ (Chrome Web Store公開準備中)
- Xブックマークエクスポーター Privacy: https://apps.yokoichi.jp/x-bookmark-exporter/privacy/
- Privacy Policy URL: https://apps.yokoichi.jp/yorishiro/privacy/
- Terms URL: https://apps.yokoichi.jp/yorishiro/terms/
- Support URL: https://apps.yokoichi.jp/yorishiro/support/

## Structure

```text
.
├── index.html
├── CNAME
├── .nojekyll
├── assets/
│   ├── app-icon.png
│   └── styles.css
├── yorishiro/
│   ├── index.html
│   ├── privacy/
│   ├── terms/
│   ├── support/
│   └── legal-notice/
├── realtime-search-shortcut/
│   ├── index.html
│   └── privacy/
├── privacy/
├── terms/
├── support/
└── legal-notice/
```

The root legal paths (`/privacy/`, `/terms/`, `/support/`, `/legal-notice/`) are kept as lightweight redirects to the Yorishiro pages.

## Deployment

This repository is intended to be published directly with GitHub Pages from the repository root.

DNS should point `apps.yokoichi.jp` to `yokoichi.github.io` with a CNAME record.

## Handoff

For detailed instructions on adding another product page, read `docs/SITE_HANDOFF_MANUAL.md`.

## Xブックマークエクスポーター

紹介・プライバシーページとJA/ENホームの5番目の製品導線を用意しています。ストアURLが未発行のため、ストアや購入へのリンクは掲載していません。保存画面のJPEGは実装UIに合成サンプルデータを表示して撮影し、画像編集を行っていません。出典・寸法・SHA-256はassets/portal-media.jsonに記録しています。問い合わせ先はmain@yokoichi.jpです。
