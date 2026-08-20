/**
 * zen-search.js — Pure frontend keyword search.
 *
 * Purpose:
 *   Provides a simple keyword match against a static array of
 *   pages/products. No backend, no full-text index.
 *
 * Usage:
 *   On search.html: reads ?q= param, displays results in #zen-search-results.
 *   Header search forms (action="/search") are intercepted to redirect
 *   to search.html?q=keyword.
 */

var ZenSearch = (function () {
  var SEARCHABLE = [
    { title: '蟬吃蜜香紅茶', type: '商品', url: 'product-honey-black.html', keywords: '蜜香 紅茶 honey black tea 紅' },
    { title: '蟬吃佳葉龍茶', type: '商品', url: 'product-gaba.html', keywords: '佳葉龍 gaba 茶 安眠 舒壓' },
    { title: '蟬吃鮮翠烏龍茶', type: '商品', url: 'product-fresh-oolong.html', keywords: '鮮翠 烏龍 oolong 清香' },
    { title: '蟬吃玉山烏龍茶', type: '商品', url: 'product-yushan-oolong.html', keywords: '玉山 烏龍 高山 oolong' },
    { title: '關於蟬吃茶', type: '頁面', url: 'about.html', keywords: '關於 品牌 故事 蟬吃茶 zeneatea' },
    { title: '門市資訊', type: '頁面', url: 'store.html', keywords: '門市 台北 信義 吳興街 地址 電話' },
    { title: '製茶師陳昭鳳', type: '頁面', url: 'tea-master.html', keywords: '製茶師 陳昭鳳 茶王 鹿鳴 獎項' },
    { title: '茶品介紹', type: '頁面', url: 'tea-intro.html', keywords: '茶品 介紹 茶葉 茶包 茶具 禮盒' },
    { title: '沖泡指南', type: '頁面', url: 'brewing.html', keywords: '沖泡 熱泡 冷泡 水溫 時間' },
    { title: '常見問答', type: '頁面', url: 'faq.html', keywords: 'faq 問答 問題 退貨 出貨 保存' },
    { title: '聯絡我們', type: '頁面', url: 'contact.html', keywords: '聯絡 客服 信箱 email' },
    { title: '蟬茶日誌', type: '文章', url: 'journal.html', keywords: '日誌 文章 部落格 最新消息' },
    { title: '玉山自然茶園', type: '文章', url: 'article-yushan-tea-garden.html', keywords: '玉山 茶園 產地 故事' },
    { title: '自然農法', type: '文章', url: 'article-natural-farming.html', keywords: '自然農法 無農藥 小綠葉蟬' },
    { title: 'GABA茶、佳葉龍茶介紹', type: '文章', url: 'article-gaba-intro.html', keywords: 'gaba 佳葉龍 介紹 低咖啡因' },
    { title: '冷泡茶泡茶方法', type: '文章', url: 'article-cold-brew.html', keywords: '冷泡 泡茶 方法 夏天' },
    { title: '各種茶的英文要怎麼說？', type: '文章', url: 'article-tea-english.html', keywords: '英文 茶 翻譯 oolong' },
    { title: '全國製茶武林大賽・榮獲茶王', type: '文章', url: 'article-tea-king-award.html', keywords: '茶王 獎項 武林大賽 陳昭鳳' },
    { title: '隱私權政策', type: '頁面', url: 'privacy.html', keywords: '隱私 政策 個資' },
    { title: '服務條款', type: '頁面', url: 'terms.html', keywords: '服務 條款' },
  ];

  function search(query) {
    if (!query || !query.trim()) return [];
    var q = query.trim().toLowerCase();
    return SEARCHABLE.filter(function (item) {
      return item.title.toLowerCase().indexOf(q) >= 0 ||
             item.keywords.toLowerCase().indexOf(q) >= 0;
    });
  }

  function renderResults(query) {
    var container = document.getElementById('zen-search-results');
    if (!container) return;
    var results = search(query);

    if (!query || !query.trim()) {
      container.innerHTML = '<p style="color:#888;font-size:15px;">請輸入搜尋關鍵字</p>';
      return;
    }

    if (results.length === 0) {
      container.innerHTML = '<p style="color:#888;font-size:15px;">找不到與「' + query + '」相關的結果</p>';
      return;
    }

    var html = '<p style="margin:0 0 20px;color:#888;font-size:14px;">找到 ' + results.length + ' 項結果</p>';
    html += '<div style="display:flex;flex-direction:column;gap:16px;">';
    results.forEach(function (r) {
      html += '<a href="' + r.url + '" style="display:block;padding:16px;background:#f9f8f6;border-radius:8px;text-decoration:none;color:inherit;">';
      html += '<span style="font-size:12px;color:#888;margin-right:8px;">' + r.type + '</span>';
      html += '<span style="font-size:16px;color:#333;">' + r.title + '</span>';
      html += '</a>';
    });
    html += '</div>';
    container.innerHTML = html;
  }

  function init() {
    var params = new URLSearchParams(window.location.search);
    var q = params.get('q') || '';
    var input = document.getElementById('zen-search-input');
    var form = document.getElementById('zen-search-form');

    if (input) input.value = q;
    if (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var val = input.value.trim();
        window.location.href = 'search.html?q=' + encodeURIComponent(val);
      });
    }

    if (input) renderResults(q);

    document.querySelectorAll('form[action="/search"], form[action="search"]').forEach(function (f) {
      f.addEventListener('submit', function (e) {
        e.preventDefault();
        var val = this.querySelector('input[name="q"]') ? this.querySelector('input[name="q"]').value : '';
        window.location.href = 'search.html?q=' + encodeURIComponent(val);
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  return { search: search, renderResults: renderResults };
})();
