# Ippodo Tea Collection Page Analysis
## Source: https://global.ippodo-tea.co.jp/collections/gyokuro
## Purpose: Visual effect & layout reference for zen_ea_tea clone

---

## 1. Page Layout (Top to Bottom)

```
┌─────────────────────────────────────┐
│  Announcement Bar (scrolling text)  │
├─────────────────────────────────────┤
│  Header (logo + nav + icons)        │
├─────────────────────────────────────┤
│  Hero Banner (image + overlay text) │
├──────────┬──────────────────────────┤
│  Filter  │  Collection Header       │
│  Sidebar │  (title + strength bar)  │
│          ├──────────────────────────┤
│  -Search │  Product Grid            │
│  -Filter │  (3-col desktop,         │
│   button │   2-col mobile,          │
│  -Sort   │   4-col ultra-wide)      │
│  dropdown│                          │
│          │  [Product] [Product] ... │
├──────────┴──────────────────────────┤
│  Footer                             │
└─────────────────────────────────────┘
```

---

## 2. Hero Banner

### HTML Structure
```html
<section class="o-hero">
  <div class="o-hero__content">
    <h2 class="o-hero__title">Gyokuro</h2>
    <p class="o-hero__text">
      Treat yourself to an elegant experience<br>with natural sweetness.
      <div class="p-tea-type__buttons">
        <a href="/blogs/tea-recipe/tagged/gyokuro"
           class="p-tea-type__button a-button--type01 a-button--outline-brown">
          Recipes
        </a>
      </div>
    </p>
  </div>
  <div class="o-hero__image"
       style="background-image: url('hero-image.png')">
  </div>
</section>
```

### Key CSS
```css
/* Desktop: two-column flex layout */
@media (min-width: 769px) {
  .o-hero {
    display: flex;
    align-items: center;
    border-bottom: solid 1px #c5c5c5;
  }
}

/* Mobile: stacked */
@media (max-width: 768px) {
  .o-hero { margin-top: 9px; }
}

/* Title: Japanese serif font */
.o-hero__title {
  font-family: yu-mincho-pr6, sans-serif;
  font-weight: 400;
}
@media (min-width: 769px) {
  font-size: 3.2rem;
  line-height: 4.8rem;
  letter-spacing: 0.2em;
}
@media (max-width: 768px) {
  font-size: 2.1rem;
  line-height: 2.4rem;
  letter-spacing: 0.2em;
}

/* Subtitle */
.o-hero__text { text-align: center; }
@media (min-width: 769px) {
  font-size: 1.8rem;
  line-height: 3.6rem;
  letter-spacing: 0.1em;
  margin-top: 40px;
}
/* Font: neuzeit-grotesk, weight 300 */

/* Hero image: CSS background-image on div, NOT <img> tag */
/* OG dimensions: 1300 x 750 */
```

---

## 3. Product Grid Layout

### Grid Container
```css
.t-collection__body { display: grid; }

/* Mobile: 2 columns */
@media (max-width: 768px) {
  .t-collection__body {
    grid-template-columns: 49.17% 49.17%;
    row-gap: 75px;
    column-gap: 1.67%;
    margin-bottom: 80px;
  }
}

/* Desktop: 3 columns */
@media (min-width: 769px) {
  .t-collection__body {
    grid-template-columns: 31.43% 31.43% 31.43%;
    row-gap: 80px;
    column-gap: 2.86%;
    margin-bottom: 32px;
  }
}

/* Wide (1298-1615px): 3 columns, slightly wider */
@media (min-width: 1298px) and (max-width: 1615px) {
  .t-collection__body {
    grid-template-columns: 32.02% 32.02% 32.02%;
    row-gap: 80px;
    column-gap: 2.13%;
  }
}

/* Ultra-wide (1612+): 4 columns */
@media (min-width: 1612px) {
  .t-collection__body {
    grid-template-columns: 24.08% 24.08% 24.08% 24.08%;
    column-gap: 1.2%;
  }
}
```

### Wrapper (sidebar + main)
```css
@media (min-width: 769px) {
  .t-collection__wrapper {
    display: flex;
    justify-content: space-between;
    max-width: 980px;
    padding: 0 20px;
    margin: auto;
  }
}
@media (min-width: 1298px) and (max-width: 1615px) {
  .t-collection__wrapper { max-width: 1298px; }
}
@media (min-width: 1612px) {
  .t-collection__wrapper { max-width: 1612px; }
}

/* Sidebar width */
@media (min-width: 769px) { .t-collection__side { width: 23.6%; } }
@media (min-width: 1612px) { .t-collection__side { width: 19%; } }

/* Main content width */
@media (min-width: 769px) { .t-collection__main { width: 74.5%; } }
@media (min-width: 1612px) { .t-collection__main { width: 79.5%; } }
```

---

## 4. Product Card

### HTML Structure
```html
<li class="m-product-card js-product-card js-item-card"
    data-tags="Rich,Loose leaf,Available year round">

  <!-- IMAGE AREA -->
  <div class="m-product-card__image js-color m-product-card__rich">
    <a href="/products/xxx">
      <img src="product-image_640x.png" alt="Product Name" />
    </a>

    <!-- Taste label (top-left corner) -->
    <span class="m-product-card__label a-label-taste a-label-taste--rich">
      Rich
    </span>

    <!-- Wishlist heart button (top-right) -->
    <div class="wish-list-button-custom">
      <button class="swym-button swym-add-to-wishlist-view-product"
              data-swaction="addToWishlist">
      </button>
    </div>

    <!-- Add to Cart slide-in button (bottom) -->
    <div class="m-product-card-actions">
      <div class="m-product-card-actions__add">
        <div class="m-slidein-button">
          <!-- Icon (visible by default) -->
          <button class="m-product-card-actions__basket-icon
                         m-slidein-button__icon">
            <i class="a-icon--basket"></i>
          </button>
          <!-- Full button (slides in on hover) -->
          <form method="post" action="/cart/add">
            <button class="button quick-add__submit
                           m-product-card-actions__add-to-basket
                           m-slidein-button__action a-button">
              <i class="a-icon--basket"></i>
              <span>Add to Cart</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- BODY AREA -->
  <div class="m-product-card__body">
    <!-- Badge (optional) -->
    <div class="a-label--type01 is-orange m-product-card__recommend">
      Limited Supply
    </div>

    <!-- Short description -->
    <p class="m-product-card__cc">
      A refined taste with pleasant, lasting tones
    </p>

    <!-- Product name -->
    <div class="m-product-card__name">
      <a class="a-link-product--type01" href="/products/xxx">
        Premium Gyokuro 30g Bag
      </a>
    </div>

    <!-- Price -->
    <div class="m-product-card__price">¥4,000</div>
  </div>
</li>
```

### Product Card CSS
```css
/* Image container — aspect ratio via padding-top */
.m-product-card__image {
  position: relative;
  display: block;
  width: 100%;
  padding-top: 124%;          /* ~4:5 aspect ratio */
  overflow: hidden;
  background-color: #f5f6f7;
  border-radius: 6px;
}

/* Image — absolute fill */
.m-product-card__image img {
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
}

/* Hover overlay */
.m-product-card__image:before {
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  content: "";
  transition: all 0.4s cubic-bezier(0.19, 1, 0.22, 1);
}

/* Color-coded hover overlays by taste */
.is-hover .m-product-card__rich:before    { background: #4fb00033; }
.is-hover .m-product-card__balance:before { background: #82d90033; }
.is-hover .m-product-card__light:before   { background: #bae61c33; }
.is-hover .m-product-card__roast:before   { background: #d8823233; }

/* Card body */
@media (min-width: 769px) {
  .m-product-card__body { margin: 15px 16px 0; }
}
@media (max-width: 768px) {
  .m-product-card__body { padding: 0 24px 0 12px; margin-top: 16px; }
}

/* Short description */
.m-product-card__cc { color: #ba876a; }
@media (min-width: 769px) {
  font-size: 1.5rem; line-height: 2.6rem; letter-spacing: 0.1em;
}
@media (max-width: 768px) {
  font-size: 1.1rem; line-height: 1.6rem; letter-spacing: 0.1em;
}

/* Product name */
.m-product-card__name { margin-top: 8px; }
@media (min-width: 769px) {
  font-size: 2rem; line-height: 3rem; letter-spacing: 0.02em;
}
@media (max-width: 768px) {
  font-size: 1.6rem; line-height: 2.4rem; letter-spacing: 0.02em;
}
/* Font: neuzeit-grotesk, weight 400 */

/* Price */
.m-product-card__price { margin-top: 8px; }
@media (min-width: 769px) {
  font-size: 1.8rem; line-height: 3.6rem; letter-spacing: 0.02em;
}
/* Font: neuzeit-grotesk, weight 300 */

/* Product link hover */
.a-link-product--type01:hover,
.is-hover .a-link-product--type01 { color: #ba876a; }
```

---

## 5. Taste Labels (Top-Left Badge on Image)

```css
.a-label-taste {
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  border-top: 1px solid;
  border-left: 1px solid;
  border-top-left-radius: 8px;
  position: absolute;
  top: 0; left: 0;
  text-align: center;
  /* Font: neuzeit-grotesk, weight 700 */
}
@media (min-width: 769px) { font-size: 1.4rem; width: 92px; height: 51px; }
@media (max-width: 768px) { font-size: 1rem;   width: 70px; height: 48px; }

/* Color variants */
.a-label-taste--rich    { color: #4fb000; border-color: #4fb000; }
.a-label-taste--balance { color: #82d900; border-color: #82d900; }
.a-label-taste--light   { color: #bae61c; border-color: #bae61c; }
.a-label-taste--roast   { color: #d88232; border-color: #d88232; }
.a-label-taste--rice    { color: #dfb23f; border-color: #dfb23f; }
.a-label-taste--clean   { color: #ffcb37; border-color: #ffcb37; }
```

---

## 6. Status Badges (Recommendation Labels)

```css
.a-label--type01 {
  display: inline-block;
  padding: 2px 16px;
  color: #fff;
  text-align: center;
  border-radius: 24px;
  /* Font: neuzeit-grotesk, weight 400 */
}
@media (min-width: 769px) { font-size: 1.8rem; line-height: 2.4rem; }
@media (max-width: 768px) { font-size: 1.3rem; line-height: 2.4rem; padding: 2px 8px; }

.a-label--type01.is-green        { background-color: #81b65d; }
.a-label--type01.is-blue         { background-color: #689fd7; }
.a-label--type01.is-yellow       { background-color: #dab95d; }
.a-label--type01.is-orange       { background-color: #ba876a; }
.a-label--type01.is-orange-light { background-color: #f1ae24; }
```

---

## 7. Quick-Add Slide-In Button

```css
/* Container positioning */
.m-product-card-actions__add,
.m-product-card-actions__favorite {
  position: absolute;
  width: 100%;
}
@media (min-width: 769px) { padding: 12px 8px; }
@media (max-width: 768px) { padding: 8px; }

.m-product-card-actions__favorite { top: 0; right: 0; }
.m-product-card-actions__add      { bottom: 0; left: 0; }

/* Slide-in animation */
.m-slidein-button__icon {
  position: absolute;
  cursor: pointer;
  opacity: 1;
}
.m-slidein-button__action {
  position: absolute;
  width: 0;
  overflow: hidden;
  opacity: 0;
  transition: all 0.3s 0s ease;
}
.a-button.m-slidein-button__action {
  max-width: 100%;
  color: #93806f;
  background-color: #fff;
  border-radius: 2px;
}

/* Hover triggers the slide */
.m-slidein-button:hover .m-slidein-button__icon  { opacity: 0; }
.m-slidein-button:hover .m-slidein-button__action { width: 100%; opacity: 1; }
```

---

## 8. Filter Panel

### Desktop Sidebar
```css
@media (min-width: 769px) {
  .o-filter__btn {
    font-size: 2rem;
    line-height: 2.6rem;
    padding: 0 0 14px 29px;
    margin-bottom: 13px;
    background: url(icon-filter.svg) -2px 3px no-repeat;
    background-size: 19px 18px;
    border-bottom: 1px solid #b7b7b7;
    color: #93806f;
  }
}

.o-filter__title {
  /* Font: goudy-old-style, serif */
}
@media (min-width: 769px) {
  font-size: 2.6rem;
  margin: 6px 0 42px;
}

/* Search input */
.o-filter__seach {
  position: relative;
  display: flex;
  align-items: center;
  color: #93806f;
}
@media (min-width: 769px) {
  font-size: 1.3rem;
  min-height: 60px;
  padding: 0 24px 0 80px;
  margin-bottom: 24px;
  background-color: #f5f6f7;
  border-radius: 40px;
}
```

### Mobile Modal
```css
@media (max-width: 768px) {
  .o-filter__btn {
    display: inline-block;
    width: calc(50% - 8px);
    padding-left: 51px;
    font-size: 1.6rem;
    line-height: 3.9rem;
    border: solid 1px #93806f;
    border-radius: 24px;
    transition: 0.8s cubic-bezier(0.19, 1, 0.22, 1);
  }

  .o-filter__open-sp {
    display: none;
    max-width: 100%;
    padding: 16px;
    border: 1px solid #93806f;
    border-radius: 2px;
    animation: show 0.4s cubic-bezier(0.19, 1, 0.22, 1);
  }
  .o-filter__open-sp.is-active {
    position: fixed;
    top: 0; right: 0; bottom: 0; left: 0;
    display: block;
    width: 90%;
    max-height: 90vh;
    margin: auto;
    overflow-y: auto;
    background: #fff;
    opacity: 1;
  }
}
```

### Filter Tag Groups
| Group | Tags |
|-------|------|
| Strength | Rich, Balanced, Light |
| How to prepare | With boiling hot water, Standard preparation, Simple cold-brewing |
| How to enjoy | With snacks, With meals, For staying well-hydrated |
| Product type | Loose leaf, Stems, Konacha, Organic, Cans, Bags, Teabags |
| Availability | Available year round, Seasonal, Limited supply, Online Exclusive, Pre-order |

### Filter Logic (Client-side JS)
```
1. Each product card has data-tags="tag1,tag2,tag3"
2. Checkboxes grouped by data-group-tag
3. AND between groups, OR within a group
4. Toggle .hidden class on product cards
5. Show "No products found" when count = 0
6. "Clear" button resets all checkboxes
```

---

## 9. Sort Dropdown

```css
.o-sort-collection { position: relative; cursor: pointer; }

.o-sort-collection__title {
  transition: all 0.4s cubic-bezier(0.19, 1, 0.22, 1);
}
@media (min-width: 769px) {
  font-size: 2rem;
  line-height: 2.6rem;
  padding-left: 30px;
  color: #93806f;
  background: url(icon-sort.svg) left center no-repeat;
  background-size: 16px 19px;
}
.o-sort-collection__title:hover {
  color: #ba876a;
  text-decoration: underline;
}

@media (max-width: 768px) {
  font-size: 1.6rem;
  line-height: 3.9rem;
  padding-left: 51px;
  background: url(icon-sort.svg) 20px 9px no-repeat;
  background-size: 19px 18px;
}
```

### Sort Options
| Value | Label |
|-------|-------|
| best-selling | Best sellers |
| created-descending | New arrival |
| price-ascending | Price ascending |
| price-descending | Price Descending |

---

## 10. Strength Indicator Bar

```html
<div class="t-collection-header__feature m-product-feature">
  <div class="m-product-feature__heading">Strength</div>
  <ul class="m-product-feature__body">
    <li class="m-product-feature__item m-product-feature__item--rich">Rich</li>
    <li class="m-product-feature__item m-product-feature__item--balance">Balance</li>
    <li class="m-product-feature__item m-product-feature__item--light">Light</li>
  </ul>
</div>
```

---

## 11. Buttons

```css
/* Type 01 — Large rounded CTA */
.a-button--type01 {
  display: block;
  width: 100%;
  text-align: center;
  text-decoration: none;
  cursor: pointer;
  /* Font: goudy-old-style, serif */
}
@media (min-width: 769px) {
  font-size: 2rem; line-height: 5.8rem; border-radius: 60px;
}
@media (max-width: 768px) {
  font-size: 1.6rem; line-height: 4.8rem; border-radius: 50px;
}

/* Brown fill */
.a-button--brown {
  color: #fff;
  background-color: #93806f;
  border-color: #93806f;
}
.a-button--brown:hover {
  background-color: #ba876a;
  border-color: #ba876a;
}

/* Outline brown */
.a-button--outline-brown {
  color: #93806f;
  border: solid 1px #93806f;
}
.a-button--outline-brown:hover {
  color: #ba876a;
  border-color: #ba876a;
}
```

---

## 12. Wishlist Button (Heart Icon)

```css
.wish-list-button-custom {
  position: absolute;
  top: 20px;
  right: 20px;
}

/* Empty heart (not wishlisted) */
.swym-button.swym-add-to-wishlist-view-product {
  background: url("icon-heart-o.svg") left top no-repeat;
  background-size: contain;
  width: 24px;
  height: 22px;
  opacity: 1;
}

/* Filled heart (wishlisted) */
.swym-button.swym-add-to-wishlist-view-product.swym-added {
  background: url("icon-heart.svg") left top no-repeat;
  background-size: contain;
}
```

---

## 13. Animations & Transitions

```css
/* Fade-in on scroll */
.o-episode.js-fadetarget {
  transition: all 0.8s ease 0s;
}
.o-episode.js-fadetarget:nth-child(2n) { transition-delay: 0.1s; }
.o-episode.js-fadetarget:nth-child(3n) { transition-delay: 0.2s; }

/* Highlight title slide-up */
.p-top-highlight__title {
  transition: all 2s cubic-bezier(0.215, 0.61, 0.355, 1) 0s;
  transform: translateY(10px);
}
.p-top-highlight__title.active { transform: none; }

/* Product card image hover */
.m-product-card__image:before {
  transition: all 0.4s cubic-bezier(0.19, 1, 0.22, 1);
}

/* Quick-add slide-in */
.m-slidein-button__action {
  transition: all 0.3s 0s ease;
}

/* Modal animations */
@keyframes fade { 0% { opacity: 0; } to { opacity: 1; } }
@keyframes show { /* opacity 0→1 + scale */ }

/* Filter mobile modal */
.o-filter__open-sp.is-active {
  animation: show 0.4s cubic-bezier(0.19, 1, 0.22, 1);
}
```

---

## 14. Design Tokens Summary

| Token | Value | Usage |
|-------|-------|-------|
| **Primary text** | `#4e4e4e` | Body text |
| **Accent brown** | `#93806f` | Buttons, links, borders |
| **Hover brown** | `#ba876a` | Hover states, descriptions |
| **Light accent** | `#f1ae24` | Orange-light badges |
| **Card bg** | `#f5f6f7` | Product image placeholder |
| **Border** | `#c5c5c5` / `#b7b7b7` | Section dividers |
| **Category text** | `#969696` | Category labels |
| **Rich green** | `#4fb000` | Rich taste label |
| **Balance green** | `#82d900` | Balanced taste label |
| **Light yellow-green** | `#bae61c` | Light taste label |
| **Roast orange** | `#d88232` | Roast taste label |
| **Heading font (JP)** | `yu-mincho-pr6, sans-serif` | Hero titles |
| **Heading font (EN)** | `goudy-old-style, serif` | Buttons, headings |
| **Body font** | `neuzeit-grotesk, sans-serif` | All body text |
| **Card image ratio** | `padding-top: 124%` | ~4:5 aspect ratio |
| **Card border-radius** | `6px` | Product images |
| **Badge border-radius** | `24px` | Status badges |
| **Button border-radius** | `60px` (type01) / `2px` (type02) | CTAs |
| **Common easing** | `cubic-bezier(0.19, 1, 0.22, 1)` | Most transitions |
| **Breakpoints** | `768px` / `769px` / `1280px` / `1298px` / `1612px` | Responsive |

---

## 15. Collection Header

```css
@media (min-width: 769px) {
  .t-collection-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 12px 12px 32px 2px;
  }
}

.t-collection--product { margin-top: 38px; }
```

---

## 16. Products on This Page (20 total, no pagination)

| # | Product | Price | Taste | Badge |
|---|---------|-------|-------|-------|
| 1 | Premium Gyokuro 30g Bag | ¥4,000 | — | Limited Supply |
| 2 | Tenka-ichi 50g Bag | ¥5,000 | Rich | — |
| 3 | Ippoen 50g Bag | ¥3,000 | Rich | — |
| 4 | Kanro 50g Bag | ¥2,000 | Rich | Try this first |
| 5 | Rimpo 50g Bag | ¥1,500 | Balanced | — |
| 6 | Tekiro 50g Bag | ¥1,300 | Light | — |
| 7 | Mantoku 50g Bag | ¥1,000 | Light | — |
| 8 | Kuki Gyokuro (Stems) 50g Bag | ¥900 | Light | — |
| 9 | Gyokuro-ko (Flakes) 50g Bag | ¥700 | Light | — |
| 10 | Drip Tea Bag Gyokuro (4g×6) | ¥1,200 | — | — |
| 11 | One-Cup Teabag (2g×25) | ¥1,800 | — | — |
| 12 | One-Cup Teabag (2g×108) | ¥6,800 | — | — |
| 13 | One-Pot Teabag (7g×6) | ¥1,200 | — | — |
| 14 | Tenka-ichi 160g Can w/box | ¥20,000 | Rich | — |
| 15 | Ippoen 160g Can w/box | ¥11,000 | Rich | — |
| 16 | Kanro 160g Can w/box | ¥8,000 | Rich | — |
| 17 | Rimpo 180g Can w/box | ¥6,000 | Balanced | — |
| 18 | Kakurei 160g Can w/box | ¥5,000 | Balanced | — |
| 19 | Tekiro 150g Can w/box | ¥3,500 | Light | — |
| 20 | Mantoku 150g Can w/box | ¥3,000 | Light | — |

---

## 17. Key Class Names Reference

| Class | Purpose |
|-------|---------|
| `o-hero` | Hero banner section |
| `o-hero__content` | Hero text container |
| `o-hero__title` | Hero heading |
| `o-hero__text` | Hero subtitle |
| `o-hero__image` | Hero background image (div, not img) |
| `t-collection__wrapper` | Flex container (sidebar + main) |
| `t-collection__side` | Filter sidebar |
| `t-collection__main` | Product grid area |
| `t-collection__body` | Product grid (CSS Grid) |
| `t-collection-header` | Header bar (title + sort) |
| `t-collection--product` | Collection type modifier |
| `m-product-card` | Individual product card |
| `m-product-card__image` | Image container (124% padding-top) |
| `m-product-card__body` | Card text area |
| `m-product-card__name` | Product name |
| `m-product-card__price` | Price display |
| `m-product-card__cc` | Short description |
| `m-product-card__label` | Taste label (positioned on image) |
| `m-product-card__recommend` | Status badge |
| `m-product-card__rich/balance/light` | Taste color modifier |
| `m-product-card-actions` | Add to cart area |
| `m-slidein-button` | Hover slide-in button container |
| `m-slidein-button__icon` | Icon (visible by default) |
| `m-slidein-button__action` | Full button (slides in on hover) |
| `a-label-taste` | Taste label badge |
| `a-label--type01` | Status badge |
| `a-button--type01` | Large rounded CTA |
| `a-button--type02` | Rectangular bold button |
| `a-button--brown` | Brown fill variant |
| `a-button--outline-brown` | Brown outline variant |
| `o-filter` | Filter panel |
| `o-filter__btn` | Filter trigger button |
| `o-filter__open-sp` | Mobile filter modal |
| `o-filter__seach` | Search input in filter |
| `o-sort-collection` | Sort dropdown |
| `m-product-feature` | Strength indicator bar |
| `wish-list-button-custom` | Wishlist heart container |
| `swym-add-to-wishlist-view-product` | Wishlist button |
| `is-hover` | Hover state class (added by JS) |
| `js-product-card` | Product card (JS target) |
| `js-item-card` | Item card (JS target) |
| `js-modal-trigger` | Modal open trigger |
| `js-modal-close` | Modal close trigger |
| `js-select-collection` | Sort select element |
| `js-filter-clear` | Clear filters button |

---

## 18. External Resources

| Resource | URL |
|----------|-----|
| Font Awesome 4.7 | `cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css` |
| jQuery 3.6.3 | Loaded from Shopify CDN |
| Adobe Fonts | `yu-mincho-pr6`, `goudy-old-style`, `neuzeit-grotesk` (via Typekit `lgg1nqr`) |
| Swiper | CDN (for other pages) |

---

## 19. Responsive Breakpoints

| Breakpoint | Layout |
|------------|--------|
| `≤ 768px` | Mobile: 2-col grid, stacked hero, modal filter |
| `769px+` | Desktop: 3-col grid, flex hero, sidebar filter |
| `1298px - 1615px` | Wide desktop: wider 3-col |
| `1612px+` | Ultra-wide: 4-col grid |

---

## 20. No Pagination

All 20 products rendered on a single page. No pagination controls exist.
