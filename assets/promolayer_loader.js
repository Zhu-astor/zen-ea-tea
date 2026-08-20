;(function () {
  var oScript = document.createElement('script')
  oScript.type = 'module'
  oScript.src = 'https://modules.promolayer.io/index.js'
  oScript.dataset.pluid = window.Shopify.shop
  oScript.crossOrigin = 'anonymous'
  oScript.async = true
  document.currentScript.parentNode.insertBefore(
    oScript,
    document.currentScript
  )
})()

