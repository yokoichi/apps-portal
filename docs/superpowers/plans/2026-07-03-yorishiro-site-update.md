# Yorishiro Site Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the official App Store badge, official X and note links, and updated legal contact details on the Yorishiro site.

**Architecture:** Keep the static HTML architecture and existing shared CSS. Reuse the existing link-card component for the official-information links, adding only section and two-column layout rules. Verify required and removed content with repeatable shell assertions, then inspect desktop and mobile rendering in the browser.

**Tech Stack:** HTML5, shared CSS, GitHub Pages

---

### Task 1: Establish Failing Content Checks

**Files:**
- Test: `yorishiro/index.html`
- Test: `yorishiro/legal-notice/index.html`

- [ ] **Step 1: Run the required-content assertions before implementation**

```bash
errors=0
rg -q 'toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/ja-jp' yorishiro/index.html || { echo 'FAIL: official App Store badge missing'; errors=1; }
rg -q 'https://x.com/yorishirodiary' yorishiro/index.html || { echo 'FAIL: official X link missing'; errors=1; }
rg -q 'https://note.yokoichi.jp/m/m8af635716abc' yorishiro/index.html || { echo 'FAIL: official note link missing'; errors=1; }
rg -q '080-6395-1725' yorishiro/legal-notice/index.html || { echo 'FAIL: telephone missing'; errors=1; }
rg -q 'yorishiro@yokoichi.jp' yorishiro/legal-notice/index.html || { echo 'FAIL: email missing'; errors=1; }
exit "$errors"
```

Expected: exit 1 with all five `FAIL` messages because the requested content is not implemented.

### Task 2: Update The Yorishiro Landing Page

**Files:**
- Modify: `yorishiro/index.html`
- Modify: `assets/styles.css`

- [ ] **Step 1: Replace the hero App Store link with the supplied badge**

```html
<div class="hero-actions">
  <a href="https://apps.apple.com/jp/app/yorishiro-%E3%82%88%E3%82%8A%E3%81%97%E3%82%8D-ai%E8%87%AA%E5%B7%B1%E5%88%86%E6%9E%90%E6%97%A5%E8%A8%98/id6764608171?itscg=30200&amp;itsct=apps_box_badge&amp;mttnsubad=6764608171" style="display: inline-block;">
    <img src="https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/ja-jp?releaseDate=1782086400" alt="App Storeでダウンロード" style="width: 224px; height: 82px; vertical-align: middle; object-fit: contain;">
  </a>
</div>
```

- [ ] **Step 2: Remove the featured App Store card and add official-information links below the existing page-link grid**

```html
<section class="official-links" aria-labelledby="official-links-heading">
  <h2 id="official-links-heading">公式情報</h2>
  <div class="link-grid official-link-grid">
    <a class="link-card" href="https://x.com/yorishirodiary" target="_blank" rel="noopener">
      <strong>公式Xアカウント</strong>
      <span>Yorishiro公式Xアカウントを開きます。</span>
    </a>
    <a class="link-card" href="https://note.yokoichi.jp/m/m8af635716abc" target="_blank" rel="noopener">
      <strong>アプリ公式noteマガジン</strong>
      <span>Yorishiro公式noteマガジンを開きます。</span>
    </a>
  </div>
</section>
```

- [ ] **Step 3: Add scoped layout rules that preserve the existing card design**

```css
.official-links {
  margin-top: 40px;
}

.official-links h2 {
  margin: 0;
  font-size: 1.35rem;
}

.official-link-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  margin-top: 14px;
}

.official-link-grid .link-card {
  min-height: 120px;
}
```

Expected: two equal cards on desktop; the existing mobile `.link-grid` rule stacks them on narrow screens.

### Task 3: Update Legal Contact Details

**Files:**
- Modify: `yorishiro/legal-notice/index.html`

- [ ] **Step 1: Update the date, telephone, and email while preserving other legal copy**

```html
<p class="page-meta">最終更新日: 2026年7月3日</p>
<p><a href="tel:080-6395-1725">080-6395-1725</a></p>
<p><a href="mailto:yorishiro@yokoichi.jp">yorishiro@yokoichi.jp</a></p>
```

### Task 4: Verify Content And Responsive Layout

**Files:**
- Test: `yorishiro/index.html`
- Test: `yorishiro/legal-notice/index.html`
- Test: `assets/styles.css`

- [ ] **Step 1: Run the required-content and removed-content assertions**

```bash
errors=0
rg -q 'toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/ja-jp' yorishiro/index.html || errors=1
rg -q 'https://x.com/yorishirodiary' yorishiro/index.html || errors=1
rg -q 'https://note.yokoichi.jp/m/m8af635716abc' yorishiro/index.html || errors=1
rg -q 'tel:080-6395-1725' yorishiro/legal-notice/index.html || errors=1
rg -q 'mailto:yorishiro@yokoichi.jp' yorishiro/legal-notice/index.html || errors=1
! rg -q 'App Storeで見る|link-card--featured' yorishiro/index.html || errors=1
! rg -q 'main@yokoichi.jp|電話番号</h2>[[:space:]]*<p>請求があった場合' yorishiro/legal-notice/index.html || errors=1
exit "$errors"
```

Expected: exit 0.

- [ ] **Step 2: Check source formatting**

Run: `git diff --check`

Expected: exit 0 with no output.

- [ ] **Step 3: Inspect desktop and mobile layouts**

Serve the repository locally and inspect `/yorishiro/` at desktop and mobile viewport sizes. Confirm the badge is visible, the two official-information cards align and stack correctly, and no horizontal overflow or overlap occurs.

- [ ] **Step 4: Commit only implementation files**

```bash
git add yorishiro/index.html yorishiro/legal-notice/index.html assets/styles.css
git diff --cached --name-only
git commit -m "feat: update Yorishiro official links"
```
