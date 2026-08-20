/**
 * zen-wishlist.js — Pure frontend wishlist with localStorage.
 *
 * Purpose:
 *   Toggle wishlist on products, display on wishlist.html.
 *   No backend. Data in localStorage key "zen_wishlist".
 *
 * Usage:
 *   Buttons with class "zen-add-to-wishlist" + data-product-id,
 *   data-product-name, data-product-image trigger toggle.
 *
 *   On wishlist.html, #zen-wishlist-container is populated.
 */

var ZenWishlist = (function () {
  var STORAGE_KEY = 'zen_wishlist';

  function getList() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch (e) {
      return [];
    }
  }

  function saveList(items) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    updateBadge();
  }

  function updateBadge() {
    var count = getList().length;
    document.querySelectorAll('a[href*="wishlist"], a[href="/pages/wishlist"]').forEach(function (el) {
      var badge = el.querySelector('.zen-wishlist-badge');
      if (!badge) {
        badge = document.createElement('span');
        badge.className = 'zen-wishlist-badge';
        badge.style.cssText = 'position:absolute;top:-4px;right:-4px;background:#c33;color:#fff;border-radius:10px;font-size:10px;min-width:16px;height:16px;display:flex;align-items:center;justify-content:center;padding:0 4px;';
        el.style.position = 'relative';
        el.appendChild(badge);
      }
      badge.textContent = count > 0 ? count : '';
      badge.style.display = count > 0 ? 'flex' : 'none';
    });
  }

  function toggle(id, name, image) {
    var items = getList();
    var idx = items.findIndex(function (i) { return i.id === id; });
    if (idx >= 0) {
      items.splice(idx, 1);
    } else {
      items.push({ id: id, name: name, image: image });
    }
    saveList(items);
    return idx < 0;
  }

  function remove(id) {
    saveList(getList().filter(function (i) { return i.id !== id; }));
    renderWishlistPage();
  }

  function renderWishlistPage() {
    var container = document.getElementById('zen-wishlist-container');
    if (!container) return;
    var items = getList();
    var empty = document.getElementById('zen-wishlist-empty');

    if (items.length === 0) {
      container.innerHTML = '<p id="zen-wishlist-empty" style="grid-column:1/-1;text-align:center;color:#888;font-size:16px;padding:60px 0;">目前沒有收藏的商品</p>';
      return;
    }

    container.innerHTML = items.map(function (item) {
      return '<div class="zen-wishlist-card" style="text-decoration:none;color:inherit;">' +
        '<a href="product-' + item.id + '.html" style="text-decoration:none;color:inherit;">' +
        '<img src="' + item.image + '" alt="' + item.name + '"/>' +
        '<p style="font-size:14px;color:#333;margin:8px 0 4px;">' + item.name + '</p>' +
        '</a>' +
        '<button class="zen-wishlist-remove" onclick="ZenWishlist.remove(\'' + item.id + '\')" style="color:#c33;cursor:pointer;border:none;background:none;font-size:13px;margin-top:6px;">移除收藏</button>' +
        '</div>';
    }).join('');
  }

  function init() {
    updateBadge();

    document.querySelectorAll('.zen-add-to-wishlist').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var added = toggle(
          this.dataset.productId,
          this.dataset.productName,
          this.dataset.productImage
        );
        this.innerHTML = added ? '♥ 已收藏' : '♡ 加入收藏';
      });
    });

    renderWishlistPage();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  return { toggle: toggle, remove: remove, init: init };
})();
