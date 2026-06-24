# apps-portal Handoff Manual

This document is the handoff guide for adding and maintaining product pages on the public apps portal.

Use this when another project thread, such as a Chrome extension project, needs to update `https://apps.yokoichi.jp/`.

## Current State

- Public repository: `https://github.com/yokoichi/apps-portal`
- Local path: `/Users/yokoichi/claudeprojects/MetaCognitionJournal/apps-portal`
- Production domain: `https://apps.yokoichi.jp/`
- Git branch: `main`
- Hosting: GitHub Pages
- Pages source: repository root, `main` branch, `/`
- Custom domain file: `CNAME`
- Current `CNAME` value: `apps.yokoichi.jp`

This repository is public. Do not put app source code, private project notes, tokens, credentials, API keys, unpublished backend details, or user data in it.

## Purpose

`apps-portal` is a small static website for public-facing product pages.

It currently hosts:

- Portal top: `/`
- Yorishiro app page: `/yorishiro/`
- Yorishiro privacy policy: `/yorishiro/privacy/`
- Yorishiro terms: `/yorishiro/terms/`
- Yorishiro support: `/yorishiro/support/`
- Yorishiro legal notice: `/yorishiro/legal-notice/`
- Realtime Search Shortcut Chrome extension page: `/realtime-search-shortcut/`
- Realtime Search Shortcut privacy policy: `/realtime-search-shortcut/privacy/`

The original iOS app repository should stay private. Public website content belongs in this `apps-portal` repository.

## File Structure

```text
.
├── index.html
├── CNAME
├── .nojekyll
├── README.md
├── assets/
│   ├── app-icon.png
│   ├── realtime-search-shortcut-icon.png
│   └── styles.css
├── docs/
│   └── SITE_HANDOFF_MANUAL.md
├── yorishiro/
│   ├── index.html
│   ├── privacy/
│   │   └── index.html
│   ├── terms/
│   │   └── index.html
│   ├── support/
│   │   └── index.html
│   └── legal-notice/
│       └── index.html
├── realtime-search-shortcut/
│   ├── index.html
│   └── privacy/
│       └── index.html
├── privacy/
│   └── index.html
├── terms/
│   └── index.html
├── support/
│   └── index.html
└── legal-notice/
    └── index.html
```

The root `privacy/`, `terms/`, `support/`, and `legal-notice/` pages are lightweight redirects to the Yorishiro pages. They exist only to avoid dead links from older or generic URLs.

## Design System

All styles live in `assets/styles.css`.

The site uses a restrained editorial/product-support style:

- Off-white background: `--bg: #f7f3ee`
- Warm surface: `--surface: #fffdf9`
- Dark text: `--ink: #20242a`
- Muted text: `--muted: #66707a`
- Green accent: `--accent: #2f7d68`
- Strong green accent: `--accent-strong: #1f5f51`
- Borders: `--line: #ded7ce`

Do not add external font imports or analytics scripts unless explicitly requested.

Important reusable classes:

- `.site-header`: shared top navigation wrapper
- `.brand`: logo/title link in header
- `.nav`: shared navigation links
- `.hero`: top hero layout
- `.eyebrow`: small label above an H1
- `.content-section`: plain body copy section
- `.link-grid`: responsive card grid
- `.link-card`: repeated card links
- `.page`: narrow page container for support/legal pages
- `.legal-page`: long-form legal text styling
- `.contact-card`: framed support/contact details
- `.site-footer`: shared footer
- `.portal-hero`: large top section for the product portal index
- `.portal-hero__copy`: copy column in the portal hero
- `.portal-hero__meta`: category pills in the portal hero
- `.portal-hero__visual`: visual panel in the portal hero
- `.product-token`: floating product icon inside the portal hero
- `.product-section`: product list section on the portal top
- `.section-heading`: section title block
- `.product-grid`: responsive product card grid
- `.product-card`: richer product card used on the portal top
- `.product-card__icon`: icon well in a product card
- `.product-card__body`: text column in a product card
- `.product-card__label`: small product category label

Use `.product-card` on the portal top. Use `.link-card` inside product detail pages for related links such as App Store, Chrome Web Store, privacy, support, and legal pages.

## Current Page Patterns

### Portal Top

File: `index.html`

Purpose:

- Introduces `yokoichi Products`
- Lists product categories
- Shows featured iOS apps and Chrome extensions

Current Yorishiro product card example:

```html
<a class="product-card product-card--app" href="./yorishiro/">
  <span class="product-card__icon">
    <img src="./assets/app-icon.png" alt="" width="72" height="72">
  </span>
  <span class="product-card__body">
    <span class="product-card__label">iOS App</span>
    <strong>yorishiro</strong>
    <span>AIと振り返る、自己理解の記録。Yorishiro の公開ページです。</span>
  </span>
</a>
```

Current Chrome extension product card example:

```html
<a class="product-card" href="./realtime-search-shortcut/">
  <span class="product-card__icon">
    <img src="./assets/realtime-search-shortcut-icon.png" alt="" width="72" height="72">
  </span>
  <span class="product-card__body">
    <span class="product-card__label">Chrome Extension</span>
    <strong>選択テキストをYahoo!リアルタイム検索で開く（非公式）</strong>
    <span>選択したテキストをYahoo!リアルタイム検索で開くChrome拡張の公開ページです。</span>
  </span>
</a>
```

When adding another Chrome extension, add a new `a.product-card` inside the `section#extensions .product-grid`.

### App/Product Top Page

Example: `yorishiro/index.html`
Example: `realtime-search-shortcut/index.html`

Purpose:

- Product name and value proposition
- Short explanation
- Links to store/support/legal/privacy pages

The app page should use:

- Header with `yokoichi Apps` brand
- Product nav links
- `section.hero`
- Optional `section.content-section`
- `section.link-grid` for support/legal/store links
- Footer

### Chrome Extension Page Pattern

Example: `realtime-search-shortcut/index.html`

Current pattern:

- Product page has `section.hero`
- Chrome extension category label is written as `.eyebrow`
- Store link is a `link-card` with `target="_blank"` and `rel="noopener"`
- Privacy link is a local `link-card`
- Non-official tools should state clearly that they are unofficial

Current Chrome Web Store card pattern:

```html
<a class="link-card" href="https://chromewebstore.google.com/detail/..." target="_blank" rel="noopener">
  <strong>Chrome Web Store</strong>
  <span>公開中の拡張機能ページをChrome Web Storeで開きます。</span>
</a>
```

### Support Page

Example: `yorishiro/support/index.html`

Current support contact is a Google Form:

```html
<p>不具合、課金、データ、その他のご相談は問い合わせフォームにてご連絡ください。</p>
<p><a href="https://forms.gle/pXicWf8RznUk7daB9">https://forms.gle/pXicWf8RznUk7daB9</a></p>
```

For a Chrome extension, create a separate support page under its product folder if support details differ. The current Realtime Search Shortcut page only has a privacy page and Chrome Web Store link; add a support page only when needed.

## Adding a Chrome Extension Page

Choose a URL slug first. Use lowercase ASCII and hyphens.

Examples:

- `/chrome-extension-name/`
- `/x-auto-management/`
- `/bookmark-exporter/`

Do not use Japanese directory names.

### Minimum Recommended Structure

For a Chrome extension called `example-extension`, create:

```text
example-extension/
├── index.html
├── privacy/
│   └── index.html
└── support/
    └── index.html
```

Add `terms/` only if the extension needs a dedicated terms page.

Add `legal-notice/` only if there is paid functionality or a specific legal/commercial reason.

### Update Portal Top

Edit `index.html` and add a card inside the existing `section#extensions .product-grid`:

```html
<a class="product-card" href="./example-extension/">
  <span class="product-card__icon">
    <img src="./assets/example-extension-icon.png" alt="" width="72" height="72">
  </span>
  <span class="product-card__body">
    <span class="product-card__label">Chrome Extension</span>
    <strong>Extension Name</strong>
    <span>Chrome拡張の短い説明を1文で入れます。</span>
  </span>
</a>
```

Keep the card text short. The portal top should stay an index, not a full landing page.

### Product Page Template

Create `example-extension/index.html`:

```html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Extension Name | yokoichi Apps</title>
    <meta name="description" content="Chrome拡張の説明を100文字前後で入れます。">
    <link rel="stylesheet" href="../assets/styles.css">
  </head>
  <body>
    <header class="site-header">
      <a class="brand" href="../">
        <img src="../assets/app-icon.png" alt="" width="42" height="42">
        <span>yokoichi Apps</span>
      </a>
      <nav class="nav" aria-label="主要ページ">
        <a href="./" aria-current="page">Extension Name</a>
        <a href="./privacy/">プライバシーポリシー</a>
        <a href="./support/">サポート</a>
      </nav>
    </header>

    <main>
      <section class="hero">
        <div>
          <p class="eyebrow">Chrome拡張</p>
          <h1>Extension Name</h1>
          <p>
            Chrome拡張の価値を1〜2文で説明します。何を楽にするのか、誰向けなのかを明確にします。
          </p>
        </div>
        <div class="hero-visual" aria-hidden="true">
          <img src="../assets/app-icon.png" alt="" width="260" height="260">
        </div>
      </section>

      <section class="content-section" aria-label="Extension Nameについて">
        <h2>主な機能</h2>
        <p>機能説明を短く書きます。詳細説明が長くなる場合は段落を分けます。</p>
      </section>

      <section class="link-grid" aria-label="関連ページ">
        <a class="link-card" href="https://chromewebstore.google.com/detail/..." target="_blank" rel="noopener">
          <strong>Chrome Web Store</strong>
          <span>公開中の拡張機能ページをChrome Web Storeで開きます。</span>
        </a>
        <a class="link-card" href="./privacy/">
          <strong>プライバシーポリシー</strong>
          <span>Chrome Web Store掲載用のプライバシーポリシーです。</span>
        </a>
        <a class="link-card" href="./support/">
          <strong>サポート</strong>
          <span>お問い合わせはこちらから。</span>
        </a>
      </section>
    </main>

    <footer class="site-footer">
      <span>&copy; 2026 yokoichi</span>
      <div class="footer-links">
        <a href="./privacy/">Privacy</a>
        <a href="./support/">Support</a>
      </div>
    </footer>
  </body>
</html>
```

### Privacy Page Template

Create `example-extension/privacy/index.html`:

```html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>プライバシーポリシー | Extension Name</title>
    <meta name="description" content="Extension Name のプライバシーポリシーです。">
    <link rel="stylesheet" href="../../assets/styles.css">
  </head>
  <body>
    <header class="site-header">
      <a class="brand" href="../../">
        <img src="../../assets/app-icon.png" alt="" width="42" height="42">
        <span>yokoichi Apps</span>
      </a>
      <nav class="nav" aria-label="主要ページ">
        <a href="../">Extension Name</a>
        <a href="./" aria-current="page">プライバシーポリシー</a>
        <a href="../support/">サポート</a>
      </nav>
    </header>

    <main class="page legal-page">
      <h1>プライバシーポリシー</h1>
      <p class="page-meta">最終更新日: YYYY年M月D日</p>

      <section>
        <h2>取得する情報</h2>
        <p>Chrome拡張が取得・保存・送信する情報を具体的に記載します。</p>
      </section>

      <section>
        <h2>利用目的</h2>
        <p>取得した情報を何のために使うか記載します。</p>
      </section>

      <section>
        <h2>第三者提供</h2>
        <p>第三者提供の有無、外部サービス利用の有無を記載します。</p>
      </section>

      <section>
        <h2>お問い合わせ</h2>
        <p><a href="../support/">サポートページ</a>よりお問い合わせください。</p>
      </section>
    </main>

    <footer class="site-footer">
      <span>&copy; 2026 yokoichi</span>
      <div class="footer-links">
        <a href="./">Privacy</a>
        <a href="../support/">Support</a>
      </div>
    </footer>
  </body>
</html>
```

### Support Page Template

Create `example-extension/support/index.html`:

```html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>サポート | Extension Name</title>
    <meta name="description" content="Extension Name のサポートページです。">
    <link rel="stylesheet" href="../../assets/styles.css">
  </head>
  <body>
    <header class="site-header">
      <a class="brand" href="../../">
        <img src="../../assets/app-icon.png" alt="" width="42" height="42">
        <span>yokoichi Apps</span>
      </a>
      <nav class="nav" aria-label="主要ページ">
        <a href="../">Extension Name</a>
        <a href="../privacy/">プライバシーポリシー</a>
        <a href="./" aria-current="page">サポート</a>
      </nav>
    </header>

    <main class="page">
      <h1>サポート</h1>
      <p class="page-meta">Extension Name に関するお問い合わせ</p>
      <div class="contact-card">
        <strong>お問い合わせ</strong>
        <p>不具合、データ、その他のご相談は問い合わせフォームにてご連絡ください。</p>
        <p><a href="https://forms.gle/pXicWf8RznUk7daB9">https://forms.gle/pXicWf8RznUk7daB9</a></p>
      </div>
    </main>

    <footer class="site-footer">
      <span>&copy; 2026 yokoichi</span>
      <div class="footer-links">
        <a href="../privacy/">Privacy</a>
        <a href="./">Support</a>
      </div>
    </footer>
  </body>
</html>
```

## Assets

Current shared icon:

- `assets/app-icon.png`
- `assets/realtime-search-shortcut-icon.png`

If the Chrome extension has its own icon, add it under `assets/`.

Recommended naming:

- `assets/example-extension-icon.png`
- `assets/example-extension-screenshot.png`

When adding product-specific images, keep paths relative:

- From root page: `./assets/example-extension-icon.png`
- From product page: `../assets/example-extension-icon.png`
- From nested pages: `../../assets/example-extension-icon.png`

Do not hotlink images from external services unless there is a clear reason.

## Local Preview

From the repository root:

```bash
cd /Users/yokoichi/claudeprojects/MetaCognitionJournal/apps-portal
python3 -m http.server 8765
```

Then open:

- `http://127.0.0.1:8765/`
- `http://127.0.0.1:8765/example-extension/`
- `http://127.0.0.1:8765/example-extension/privacy/`
- `http://127.0.0.1:8765/example-extension/support/`

Stop the server with `Ctrl-C`.

## Validation Checklist

Before committing:

- `git status --short` shows only intended files.
- Every new page has `<!doctype html>`, `lang="ja"`, charset, viewport, title, and description.
- Links are relative and work from the page depth.
- Header nav uses `aria-current="page"` on the current page.
- Images load locally.
- Mobile layout does not horizontally overflow.
- No secrets, internal implementation notes, API keys, unpublished repository URLs, or private data are present.
- Legal/privacy text is product-specific and not copied blindly from Yorishiro unless applicable.

Optional quick checks:

```bash
rg -n "TODO|PLACEHOLDER|API_KEY|SECRET|TOKEN|localhost" .
rg -n "mailto:main@yokoichi.jp|forms.gle" .
git diff --check
```

## Git Workflow

Work in the public repository:

```bash
cd /Users/yokoichi/claudeprojects/MetaCognitionJournal/apps-portal
git status --short
git add .
git commit -m "Add Chrome extension page"
git push
```

Current remote:

```text
origin  https://github.com/yokoichi/apps-portal.git
```

GitHub Pages deploys automatically from `main`.

## Deployment

The site is served by GitHub Pages from the repository root.

The `CNAME` file must remain:

```text
apps.yokoichi.jp
```

Do not remove `.nojekyll`; it keeps GitHub Pages from applying Jekyll processing.

After pushing, GitHub Pages may take a short time to rebuild.

Check the public URL:

```text
https://apps.yokoichi.jp/
```

For a new Chrome extension page, expected URL format:

```text
https://apps.yokoichi.jp/example-extension/
```

## HTTPS Notes

If the browser says the connection is not secure:

- Confirm DNS has `apps.yokoichi.jp` as a `CNAME` to `yokoichi.github.io`.
- In GitHub repository settings for `apps-portal`, confirm Pages has custom domain `apps.yokoichi.jp`.
- Once GitHub validates DNS, enable `Enforce HTTPS`.

## Chrome Web Store Notes

Chrome Web Store may require clear privacy disclosures depending on extension permissions.

Before publishing a privacy page, review the extension manifest:

- `permissions`
- `host_permissions`
- `optional_permissions`
- `content_scripts`
- `externally_connectable`
- background/service worker network calls
- local storage usage
- sync storage usage

The privacy page should explicitly say:

- what data the extension reads
- whether data leaves the browser
- where data is sent, if any
- whether data is sold or shared
- how users can contact support

If the extension only stores data locally, say that clearly. If it calls an external API, name the API and explain the purpose.

## Source Of Truth

For public site edits, use:

```text
/Users/yokoichi/claudeprojects/MetaCognitionJournal/apps-portal
```

Do not treat the old `site/` directory inside the private `MetaCognitionJournal` app repository as the deployment source. The live public repository is `apps-portal`.

## Quick Task Prompt For Another Thread

Use this prompt in the Chrome extension project thread:

```text
Read /Users/yokoichi/claudeprojects/MetaCognitionJournal/apps-portal/docs/SITE_HANDOFF_MANUAL.md.
Then add a public product page for this Chrome extension to the apps-portal repository.
Use /Users/yokoichi/claudeprojects/MetaCognitionJournal/apps-portal as the public site repo.
Do not modify the private MetaCognitionJournal app source unless explicitly needed.
```
