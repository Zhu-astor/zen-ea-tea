/**
 * zen-cart.js — Pure frontend cart with localStorage + side drawer.
 *
 * Purpose:
 *   Provides add-to-cart, quantity adjust, remove, and a slide-in drawer
 *   for the ZenEaTea POC. No backend, no Shopify API. All data in
 *   localStorage key "zen_cart".
 *
 * Usage:
 *   Any button with class "zen-add-to-cart" and data-product-id,
 *   data-product-name, data-product-price, data-product-image will
 *   trigger add-to-cart on click.
 *
 *   The cart icon in the header (any <a href> containing "/cart" or
 *   href="cart.html") opens the drawer.
 *
 *   Call ZenCart.init() on page load (auto-called on DOMContentLoaded).
 */

var ZenCart = (function () {
  var STORAGE_KEY = 'zen_cart';
  var drawerEl = null;
  var overlayEl = null;

  function getCart() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch (e) {
      return [];
    }
  }

  function saveCart(items) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    updateBadge();
  }

  function updateBadge() {
    var items = getCart();
    var count = items.reduce(function (s, i) { return s + i.qty; }, 0);
    document.querySelectorAll('.c-unav-pc__bag-count, .c-unav-sp__bag-count, .c-unav__bag-count').forEach(function (el) {
      el.setAttribute('data-count', count);
      el.textContent = count > 0 ? count : '';
    });
  }

  function addItem(id, name, price, image) {
    var items = getCart();
    var existing = items.find(function (i) { return i.id === id; });
    if (existing) {
      existing.qty++;
    } else {
      items.push({ id: id, name: name, price: price, image: image, qty: 1 });
    }
    saveCart(items);
    renderDrawer();
    openDrawer();
  }

  function removeItem(id) {
    var items = getCart().filter(function (i) { return i.id !== id; });
    saveCart(items);
    renderDrawer();
  }

  function changeQty(id, delta) {
    var items = getCart();
    var item = items.find(function (i) { return i.id === id; });
    if (!item) return;
    item.qty = Math.max(1, item.qty + delta);
    saveCart(items);
    renderDrawer();
  }

  function createDrawer() {
    if (drawerEl) return;

    overlayEl = document.createElement('div');
    overlayEl.className = 'zen-cart-overlay';
    overlayEl.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.4);z-index:9998;opacity:0;visibility:hidden;transition:opacity 0.3s;';
    overlayEl.addEventListener('click', closeDrawer);
    document.body.appendChild(overlayEl);

    drawerEl = document.createElement('div');
    drawerEl.className = 'zen-cart-drawer';
    drawerEl.style.cssText = 'position:fixed;top:0;right:0;width:400px;max-width:90vw;height:100%;background:#fff;z-index:9999;transform:translateX(100%);transition:transform 0.3s;overflow-y:auto;box-shadow:-4px 0 20px rgba(0,0,0,0.15);';
    document.body.appendChild(drawerEl);
  }

  function renderDrawer() {
    if (!drawerEl) createDrawer();
    var items = getCart();
    var total = items.reduce(function (s, i) {
      var p = parseInt(i.price.replace(/[^0-9]/g, '')) || 0;
      return s + p * i.qty;
    }, 0);

    var html = '<div style="padding:20px;border-bottom:1px solid #eee;display:flex;justify-content:space-between;align-items:center;">';
    html += '<h2 style="font-size:18px;margin:0;color:#333;">購物車</h2>';
    html += '<button onclick="ZenCart.close()" style="background:none;border:none;font-size:24px;cursor:pointer;color:#888;">&times;</button>';
    html += '</div>';

    if (items.length === 0) {
      html += '<div style="padding:60px 20px;text-align:center;color:#888;font-size:15px;">購物車是空的</div>';
    } else {
      html += '<div style="padding:0 20px;">';
      items.forEach(function (item) {
        html += '<div style="display:flex;gap:12px;padding:16px 0;border-bottom:1px solid #f0f0f0;">';
        html += '<img src="' + item.image + '" alt="" style="width:60px;height:60px;object-fit:contain;background:#f5f6f7;border-radius:4px;flex-shrink:0;"/>';
        html += '<div style="flex:1;">';
        html += '<p style="font-size:14px;margin:0 0 4px;color:#333;">' + item.name + '</p>';
        html += '<p style="font-size:14px;margin:0 0 8px;color:#666;">' + item.price + '</p>';
        html += '<div style="display:flex;align-items:center;gap:8px;">';
        html += '<button onclick="ZenCart.changeQty(\'' + item.id + '\',-1)" style="width:24px;height:24px;border:1px solid #ddd;background:#fff;cursor:pointer;border-radius:3px;">-</button>';
        html += '<span style="font-size:14px;min-width:20px;text-align:center;">' + item.qty + '</span>';
        html += '<button onclick="ZenCart.changeQty(\'' + item.id + '\',1)" style="width:24px;height:24px;border:1px solid #ddd;background:#fff;cursor:pointer;border-radius:3px;">+</button>';
        html += '<button onclick="ZenCart.removeItem(\'' + item.id + '\')" style="margin-left:auto;color:#c33;background:none;border:none;cursor:pointer;font-size:13px;">移除</button>';
        html += '</div></div></div>';
      });
      html += '</div>';
      html += '<div style="padding:20px;border-top:1px solid #eee;">';
      html += '<div style="display:flex;justify-content:space-between;margin-bottom:16px;"><span style="font-size:15px;color:#666;">合計</span><span style="font-size:18px;color:#333;">NT$' + total.toLocaleString() + '</span></div>';
      html += '<button onclick="alert(\'敬請期待！結帳功能即將開放。\')" style="width:100%;padding:12px;background:#3a3a3a;color:#fff;border:none;border-radius:4px;cursor:pointer;font-size:15px;">前往結帳</button>';
      html += '</div>';
    }

    drawerEl.innerHTML = html;
  }

  function openDrawer() {
    renderDrawer();
    drawerEl.style.transform = 'translateX(0)';
    overlayEl.style.opacity = '1';
    overlayEl.style.visibility = 'visible';
  }

  function closeDrawer() {
    if (!drawerEl) return;
    drawerEl.style.transform = 'translateX(100%)';
    overlayEl.style.opacity = '0';
    overlayEl.style.visibility = 'hidden';
  }

  function init() {
    createDrawer();
    updateBadge();

    document.querySelectorAll('.zen-add-to-cart').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        addItem(
          this.dataset.productId,
          this.dataset.productName,
          this.dataset.productPrice,
          this.dataset.productImage
        );
      });
    });

    document.querySelectorAll('a[href*="cart"], a[href="/cart"], a[href="cart.html"]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        openDrawer();
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  return { init: init, open: openDrawer, close: closeDrawer, addItem: addItem, removeItem: removeItem, changeQty: changeQty };
})();
