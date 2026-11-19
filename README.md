# apps-portal

GitHub Pages で公開するアプリポータル用の静的サイトです。

- Portal URL: https://apps.yokoichi.jp/
- Yorishiro URL: https://apps.yokoichi.jp/yorishiro/
- Realtime Search Shortcut URL: https://apps.yokoichi.jp/realtime-search-shortcut/
- Ichikeshi URL: https://apps.yokoichi.jp/ichikeshi/ (en: https://apps.yokoichi.jp/ichikeshi/en/)
- Xブックマークエクスポーター URL: https://apps.yokoichi.jp/x-bookmark-exporter/ (Chrome Web Store公開中)
- Xブックマークエクスポーター Privacy: https://apps.yokoichi.jp/x-bookmark-exporter/privacy/
- まとめて非表示 for メルカリ（メルカリ非公式） URL: https://apps.yokoichi.jp/matomete-hihyoji/ (Chrome Web Store申請準備中)
- まとめて非表示 for メルカリ Privacy: https://apps.yokoichi.jp/matomete-hihyoji/privacy/
- kokomemo URL: https://apps.yokoichi.jp/kokomemo/ (en: https://apps.yokoichi.jp/kokomemo/en/) (App Store申請準備中)
- kokomemo Privacy: https://apps.yokoichi.jp/kokomemo/privacy/ (en: https://apps.yokoichi.jp/kokomemo/en/privacy/)
- kokomemo Support: https://apps.yokoichi.jp/kokomemo/support/ (en: https://apps.yokoichi.jp/kokomemo/en/support/)
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

紹介・プライバシーページとJA/ENホームの5番目の製品導線を用意しています。紹介ページの保存画面の下にChrome Web Storeへのリンクを掲載しています。保存画面のJPEGは実装UIに合成サンプルデータを表示して撮影し、画像編集を行っていません。出典・寸法・SHA-256はassets/portal-media.jsonに記録しています。問い合わせ先はmain@yokoichi.jpです。

## まとめて非表示 for メルカリ

メルカリの非公式Chrome拡張（株式会社メルカリとは無関係）の紹介・プライバシーページと、JA/ENホームの6番目の製品導線を用意しています。Chrome Web Storeは申請準備中のため、ストアリンクは公開後に追加します。確認ダイアログのJPEGは実装UIにダミーデータを表示して撮影し、画像編集を行っていません。出典・寸法・SHA-256はassets/portal-media.jsonに記録しています。問い合わせ先はmain@yokoichi.jpです。

## kokomemo

場所にメモを結び付け、到着時に通知するiOSアプリの紹介・プライバシー・サポートページ（日本語・英語）と、JA/ENホームの4番目の製品導線（位置消しの次）を用意しています。App Storeは申請準備中のため、ストアリンクは公開後に追加します。スクリーンショットは素材確定後に追加します。アイコンはkokomemoプロジェクトの独自描画アイコンを縮小したもので、出典・寸法・SHA-256はassets/portal-media.jsonに記録しています。問い合わせ先と運営者表記はOshiCamのページと同じ問い合わせフォームです。
